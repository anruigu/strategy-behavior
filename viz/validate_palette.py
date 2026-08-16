#!/usr/bin/env python
"""Python twin of the dataviz skill's `scripts/validate_palette.js`.

    python viz/validate_palette.py "#2a78d6,#eb6834,#1baf7a" --mode light --pairs all

Same math and the same thresholds as the JS original -- Machado 2009 CVD
transforms at severity 1.0, OKLab dE x100, WCAG contrast -- ported because this
box has no node. The JS file states its normalization rules are meant to be kept
"in lockstep with the Python twin"; this is that twin.

Exists so the palette check is *run* rather than reasoned about, which is the
one habit the skill calls non-negotiable.
"""

from __future__ import annotations

import argparse
import math
import re
import sys

BAND = {"light": (0.43, 0.77), "dark": (0.48, 0.67)}  # OKLCH L
CHROMA_FLOOR = 0.10
CVD_TARGET, CVD_FLOOR = 8.0, 6.0
NORMAL_FLOOR = 15.0
CONTRAST_MIN = 3.0
DEFAULT_SURFACE = {"light": "#fcfcfb", "dark": "#1a1a19"}

MACHADO = {
    "protan": ((0.152286, 1.052583, -0.204868),
               (0.114503, 0.786281, 0.099216),
               (-0.003882, -0.048116, 1.051998)),
    "deutan": ((0.367322, 0.860646, -0.227968),
               (0.280085, 0.672501, 0.047413),
               (-0.011820, 0.042940, 0.968881)),
    "tritan": ((1.255528, -0.076749, -0.178779),
               (-0.078411, 0.930809, 0.147602),
               (0.004733, 0.691367, 0.303900)),
}

# Intersection of JS trim() and Python str.strip(), per the JS source note.
_WS = "[ \t\n\v\f\r   -     　]+"
_STRIP = re.compile(rf"^{_WS}|{_WS}$")
_HEX = re.compile(r"^#?[0-9a-fA-F]{6}$")


def _strip(v: str) -> str:
    return _STRIP.sub("", v)


def split_colors(raw: str) -> list[str]:
    return [c for c in (_strip(x) for x in (raw or "").split(",")) if c]


def _srgb(h: str) -> tuple[float, float, float]:
    if not _HEX.match(h):
        sys.exit(f"not a hex colour: {h!r}")
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))  # type: ignore[return-value]


def _s2lin(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def lin(h: str) -> tuple[float, float, float]:
    return tuple(_s2lin(c) for c in _srgb(h))  # type: ignore[return-value]


def rel_lum(h: str) -> float:
    r, g, b = lin(h)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    hi, lo = sorted((rel_lum(a), rel_lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def oklab_from_lin(rgb: tuple[float, float, float]) -> tuple[float, float, float]:
    r, g, b = rgb
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return (
        0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
        1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
        0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s,
    )


def oklch(h: str) -> tuple[float, float]:
    L, a, b = oklab_from_lin(lin(h))
    return L, math.hypot(a, b)


def simulate(h: str, kind: str) -> tuple[float, float, float]:
    r, g, b = lin(h)
    M = MACHADO[kind]
    return tuple(min(1.0, max(0.0, M[i][0] * r + M[i][1] * g + M[i][2] * b)) for i in range(3))  # type: ignore[return-value]


def delta_e(h1: str, h2: str, kind: str | None = None) -> float:
    a = oklab_from_lin(simulate(h1, kind) if kind else lin(h1))
    b = oklab_from_lin(simulate(h2, kind) if kind else lin(h2))
    return 100 * math.dist(a, b)


def validate(palette: list[str], mode: str = "light", surface: str | None = None,
             pairs: str = "adjacent") -> tuple[list[tuple[str, str, str]], bool]:
    surface = surface or DEFAULT_SURFACE[mode]
    lo, hi = BAND[mode]
    report: list[tuple[str, str, str]] = []
    ok = True

    offband = [(c, round(oklch(c)[0], 3)) for c in palette if not (lo <= oklch(c)[0] <= hi)]
    ok &= not offband
    report.append(("Lightness band", "pass" if not offband else "FAIL",
                   f"outside band: {offband}" if offband else f"all {len(palette)} inside L {lo}-{hi}"))

    lowc = [(c, round(oklch(c)[1], 3)) for c in palette if oklch(c)[1] < CHROMA_FLOOR]
    ok &= not lowc
    report.append(("Chroma floor", "pass" if not lowc else "FAIL",
                   f"reads gray: {lowc}" if lowc else f"all {len(palette)} >= {CHROMA_FLOOR}"))

    n = len(palette)
    if pairs == "all":
        pairlist = [(i, j) for i in range(n) for j in range(i + 1, n)]
    else:
        pairlist = [(i, i + 1) for i in range(n - 1)]
    label = "all-pairs" if pairs == "all" else "adjacent"

    worst = None
    for kind in ("protan", "deutan"):
        for i, j in pairlist:
            d = delta_e(palette[i], palette[j], kind)
            if worst is None or d < worst[0]:
                worst = (d, kind, palette[i], palette[j])
    tri = min((delta_e(palette[i], palette[j], "tritan") for i, j in pairlist), default=99.0)
    wd = worst[0] if worst else 99.0
    state = "pass" if wd >= CVD_TARGET else ("floor" if wd >= CVD_FLOOR else "FAIL")
    ok &= state != "FAIL"
    report.append(("CVD separation", state,
                   f"worst {label} {worst[3]}<->{worst[2]} dE {wd:.1f} ({worst[1]}) - tritan {tri:.1f}"
                   if worst else "n/a"))

    nworst = None
    for i, j in pairlist:
        d = delta_e(palette[i], palette[j])
        if nworst is None or d < nworst[0]:
            nworst = (d, palette[i], palette[j])
    nd = nworst[0] if nworst else 99.0
    nstate = "pass" if nd >= NORMAL_FLOOR else "FAIL"
    ok &= nstate != "FAIL"
    report.append(("Normal-vision floor", nstate,
                   f"worst {label} {nworst[2]}<->{nworst[1]} dE {nd:.1f} (normal)" if nworst else "n/a"))

    low = [(c, round(contrast(c, surface), 2)) for c in palette if contrast(c, surface) < CONTRAST_MIN]
    report.append(("Contrast vs surface", "relief" if low else "pass",
                   f"below {CONTRAST_MIN}:1 - relief required (visible labels or table view): {low}"
                   if low else f"all {len(palette)} >= {CONTRAST_MIN}:1"))

    return report, ok


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("palette")
    ap.add_argument("--mode", default="light", choices=("light", "dark"))
    ap.add_argument("--surface", default="")
    ap.add_argument("--pairs", default="adjacent", choices=("adjacent", "all"))
    args = ap.parse_args()

    pal = split_colors(args.palette)
    surface = args.surface or DEFAULT_SURFACE[args.mode]
    report, ok = validate(pal, args.mode, surface, args.pairs)
    print(f"palette {pal}  mode={args.mode}  surface={surface}  pairs={args.pairs}")
    for name, state, detail in report:
        print(f"  {state:7} {name:22} {detail}")
    print("  => OK" if ok else "  => FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
