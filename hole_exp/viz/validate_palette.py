#!/usr/bin/env python
"""Python twin of the dataviz skill's `scripts/validate_palette.js`.

    python validate_palette.py "#2a78d6,#eb6834,#1baf7a" --mode light
    python validate_palette.py "#3987e5,..." --mode dark --pairs all

WHY THIS EXISTS. The skill's rule is that the colour checks are computable and
must be COMPUTED, never eyeballed -- but this box has no JS runtime, so the
shipped validator cannot run here. Reasoning about Delta E by hand is exactly
what the rule forbids, and quoting the palette doc's published numbers only
covers the exact slot set it published. So the checks are ported instead.

PORTED FAITHFULLY, CONSTANT FOR CONSTANT: sRGB -> linear -> OKLab, the Machado
(2009) CVD matrices at severity 1.0, Euclidean OKLab Delta E x100, the same
lightness band, chroma floor, CVD target/floor, normal-vision floor and WCAG
contrast minimum. `check_parity` below re-derives the palette doc's published
figures as a regression test on the port: if this file drifts from the JS, the
numbers it reproduces stop matching and the drift is visible rather than
silent.
"""
from __future__ import annotations

import argparse
import math
import re
import sys
from typing import List, Optional, Sequence, Tuple

BAND = {"light": (0.43, 0.77), "dark": (0.48, 0.67)}   # OKLCH L
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

# Same normalisation set as the JS twin: ASCII whitespace plus the Unicode
# space/separator characters BOTH engines strip. Kept in lockstep on purpose --
# an unguarded parse turns a stray NBSP into NaN and the run fails OPEN.
_WS = "[ \t\n\v\f\r   -     　]+"
_HEX = re.compile(r"^#?[0-9a-fA-F]{6}$")


def split_colors(raw: str) -> List[str]:
    out = []
    for part in (raw or "").split(","):
        v = re.sub(f"^{_WS}|{_WS}$", "", part)
        if v:
            out.append(v)
    return out


def _s2lin(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def lin(h: str) -> Tuple[float, float, float]:
    if not _HEX.match(h):
        raise SystemExit(f"not a hex colour: {h!r}")
    h = h.lstrip("#")
    return tuple(_s2lin(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4))


def _oklab_from_lin(rgb) -> Tuple[float, float, float]:
    r, g, b = rgb
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def oklch(h: str) -> Tuple[float, float]:
    L, a, b = _oklab_from_lin(lin(h))
    return L, math.hypot(a, b)


def rel_lum(h: str) -> float:
    r, g, b = lin(h)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    hi, lo = sorted((rel_lum(a), rel_lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def _simulate(h: str, kind: str):
    r, g, b = lin(h)
    M = MACHADO[kind]
    return tuple(min(1.0, max(0.0, M[i][0] * r + M[i][1] * g + M[i][2] * b))
                 for i in range(3))


def delta_e(h1: str, h2: str, kind: Optional[str] = None) -> float:
    a = _oklab_from_lin(_simulate(h1, kind) if kind else lin(h1))
    b = _oklab_from_lin(_simulate(h2, kind) if kind else lin(h2))
    return 100 * math.dist(a, b)


def validate(palette: Sequence[str], mode: str = "light",
             surface: Optional[str] = None, pairs: str = "adjacent"):
    surface = surface or DEFAULT_SURFACE[mode]
    lo, hi = BAND[mode]
    report, ok = [], True

    offband = [(c, round(oklch(c)[0], 3)) for c in palette
               if not (lo <= oklch(c)[0] <= hi)]
    ok &= not offband
    report.append(("Lightness band", "pass" if not offband else "fail",
                   f"outside band: {offband}" if offband
                   else f"all {len(palette)} inside L {lo}-{hi}"))

    lowc = [(c, round(oklch(c)[1], 3)) for c in palette
            if oklch(c)[1] < CHROMA_FLOOR]
    ok &= not lowc
    report.append(("Chroma floor", "pass" if not lowc else "fail",
                   f"below floor (reads gray): {lowc}" if lowc
                   else f"all {len(palette)} >= {CHROMA_FLOOR}"))

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
    tri = min((delta_e(palette[i], palette[j], "tritan")
               for i, j in pairlist), default=99.0)
    wd = worst[0] if worst else 99.0
    state = "pass" if wd >= CVD_TARGET else ("floor" if wd >= CVD_FLOOR else "fail")
    ok &= state != "fail"
    report.append(("CVD separation", state,
                   f"worst {label} {worst[3]}<->{worst[2]} dE {wd:.1f} "
                   f"({worst[1]}) - tritan {tri:.1f}" if worst else "n/a"))

    nworst = None
    for i, j in pairlist:
        d = delta_e(palette[i], palette[j])
        if nworst is None or d < nworst[0]:
            nworst = (d, palette[i], palette[j])
    nd = nworst[0] if nworst else 99.0
    nstate = "pass" if nd >= NORMAL_FLOOR else "fail"
    ok &= nstate == "pass"
    report.append(("Normal-vision floor", nstate,
                   f"worst {label} {nworst[2]}<->{nworst[1]} dE {nd:.1f} (normal)"
                   + ("" if nd >= NORMAL_FLOOR else
                      f" - below {NORMAL_FLOOR:.0f}, hard to tell apart even "
                      f"with full colour vision") if nworst else "n/a"))

    low = [(c, round(contrast(c, surface), 2)) for c in palette
           if contrast(c, surface) < CONTRAST_MIN]
    report.append(("Contrast vs surface", "relief" if low else "pass",
                   f"below {CONTRAST_MIN}:1 - relief required (visible labels "
                   f"or table view): {low}" if low
                   else f"all {len(palette)} >= {CONTRAST_MIN}:1"))
    return report, ok


def check_parity() -> bool:
    """Reproduce the palette doc's published figures, as a port regression test."""
    light = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
             "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
    dark = ["#3987e5", "#d95926", "#199e70", "#c98500",
            "#d55181", "#008300", "#9085e9", "#e66767"]
    exp = {("light", "adjacent"): (9.1, 19.6), ("dark", "adjacent"): (8.4, 19.3)}
    okall = True
    for mode, pal in (("light", light), ("dark", dark)):
        pl = [(i, i + 1) for i in range(len(pal) - 1)]
        cvd = min(delta_e(pal[i], pal[j], k)
                  for k in ("protan", "deutan") for i, j in pl)
        nor = min(delta_e(pal[i], pal[j]) for i, j in pl)
        e_cvd, e_nor = exp[(mode, "adjacent")]
        good = abs(cvd - e_cvd) < 0.1 and abs(nor - e_nor) < 0.1
        okall &= good
        print(f"  parity {mode:5s}: CVD {cvd:.1f} (doc {e_cvd})  "
              f"normal {nor:.1f} (doc {e_nor})  {'OK' if good else 'DRIFT'}")
    return okall


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("palette", nargs="?", default="")
    ap.add_argument("--mode", default="light", choices=["light", "dark"])
    ap.add_argument("--surface", default=None)
    ap.add_argument("--pairs", default="adjacent", choices=["adjacent", "all"])
    ap.add_argument("--parity", action="store_true")
    a = ap.parse_args()
    if a.parity:
        print("port parity against references/palette.md:")
        return 0 if check_parity() else 1
    pal = split_colors(a.palette)
    if not pal:
        raise SystemExit("no colours given")
    report, ok = validate(pal, a.mode, a.surface, a.pairs)
    surf = a.surface or DEFAULT_SURFACE[a.mode]
    print(f"palette n={len(pal)}  mode={a.mode}  surface={surf}  pairs={a.pairs}")
    for name, state, detail in report:
        print(f"  [{state.upper():6s}] {name:22s} {detail}")
    print("  => " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
