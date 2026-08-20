#!/usr/bin/env python3
"""Classify each ladder curve as rising / saturating / flat, with the rule stated.

    python scaling_shape.py [--step N] [--md OUT.md]

The plan's pass-1 decision is "eyeball the shape, then decide whether to spend
seeds 2-3". Eyeballing a 4-point curve with error bars is exactly the situation
where a reader sees the shape they expected, so the rule is written down here
and applied identically to every panel.

THE RULE. Let d = y(8) - y(1) and se_d = sqrt(se(8)^2 + se(1)^2).

    flat        |d| < 2*se_d                     -- endpoints indistinguishable
    rising      d > 2*se_d and the 1->4 and 4->8 legs BOTH move up (within se)
    saturating  d > 2*se_d but the 4->8 leg is flat or down
    non-monotone d > 2*se_d with an interior dip below y(1)
    falling     d < -2*se_d

`2*se_d` is deliberately crude. These are EPISODE-level bars at ONE training
seed, so the honest claim a "rising" verdict supports is "this checkpoint's rate
at n=8 is measurably above its rate at n=1", NOT "training on more envs raises
transfer in expectation". Only seeds 2-3 can license the second sentence, which
is why the output prints the seed caveat next to every verdict rather than in a
footnote someone can skip.

The Spearman column is reported for completeness and should carry almost no
weight: with four points it takes only values in a small discrete set, and it
cannot reach significance at any n.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import make_scaling_figs as F  # noqa: E402  (reuse its readers, one source)
import scaling_rungs as S  # noqa: E402

K = 2.0  # SE multiplier for "distinguishable"


def spearman(xs, ys) -> float:
    """Rank correlation. Hand-rolled: scipy is not in the venv with matplotlib,
    and with n=4 and no ties this is three lines."""
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        for pos, i in enumerate(order):
            r[i] = pos + 1.0
        return r
    rx, ry = rank(xs), rank(ys)
    n = len(xs)
    if n < 2:
        return float("nan")
    d2 = sum((a - b) ** 2 for a, b in zip(rx, ry))
    return 1 - 6 * d2 / (n * (n * n - 1))


def classify(pts):
    """pts: list of (n, mean, se) at the rungs present, ascending in n."""
    pts = [(n, m, s) for n, m, s in pts if m is not None]
    if len(pts) < 2:
        return "insufficient", None, None
    (n0, y0, s0), (n1, y1, s1) = pts[0], pts[-1]
    d = y1 - y0
    se_d = ((s0 or 0.0) ** 2 + (s1 or 0.0) ** 2) ** 0.5
    thresh = K * se_d
    rho = spearman([p[0] for p in pts], [p[1] for p in pts])
    if se_d == 0:
        return ("rising" if d > 0 else "falling" if d < 0 else "flat"), d, rho
    if abs(d) < thresh:
        return "flat", d, rho
    if d < 0:
        return "falling", d, rho
    # rising overall -- is it still rising at the top, or has it bent over?
    if any(m < y0 - thresh for _, m, _ in pts[1:-1]):
        return "non-monotone", d, rho
    # The mid point must be strictly INSIDE the usable range. When a broken top
    # rung is excluded, n=4 becomes the last point too, and `slope_high` is then
    # zero by construction -- which silently labelled every such curve
    # "saturating" regardless of its actual shape.
    mid = [p for p in pts if p[0] == 4 and p[0] < pts[-1][0]]
    if mid:
        _, ym, _sm = mid[0]
        # PER-DOUBLING slopes, not raw legs: n=1->4 is two doublings and n=4->8
        # is one, so comparing the raw legs calls a straight line "saturating".
        # Nor is the test "is the top leg individually significant" -- that is a
        # much stricter bar than "has the curve flattened", and on a perfectly
        # linear stub it wrongly returned saturating for every panel.
        slope_low = (ym - y0) / 2.0
        slope_high = y1 - ym
        if slope_high < 0.5 * slope_low:
            return "saturating", d, rho
    return "rising", d, rho


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--step", type=int, default=None)
    ap.add_argument("--md", default=None)
    a = ap.parse_args()

    tierA = F.load_tier_a(a.step)
    mach = F.load_mach()
    if tierA is None:
        raise SystemExit("no Tier A output yet")
    by_fam = ((tierA.get("meta") or {}).get("step_by_family")) or {}

    out = ["# Env-count ladder — shape verdicts",
           "",
           f"Rule: flat if |y(8)-y(1)| < {K:g}x the combined SE; rising if it "
           "clears that AND the top leg is still climbing; saturating if it "
           "clears it but the 4->8 leg is not.",
           "",
           "**One training seed.** Bars are episode-level. A `rising` verdict "
           "says this checkpoint's rate at n=8 is measurably above its rate at "
           "n=1 — not that #envs raises transfer in expectation. Seeds 2-3 are "
           "what would license the second claim.",
           "",
           f"A `!` marks a point whose invalid rate exceeds "
           f"{F.BROKEN_INVALID:.0%} (check_suite's BROKEN threshold). Its "
           "denominator is selected by whether the model emitted a parseable "
           "action, so it is shown but EXCLUDED from the verdict.",
           ""]

    decision = []
    for fam in S.FAMILIES:
        step = by_fam.get(fam, tierA.get("step"))
        out += [f"## {F.FAMLAB[fam]}  (step {step})", "",
                "| metric | n=1 | n=2 | n=4 | n=8 | base | d(8-1) | verdict | rho |",
                "|---|---|---|---|---|---|---|---|---|"]
        for key, title, _ylab, src in F.PANELS:
            pts, flags = [], []
            for n in S.RUNG_NS:
                arm = f"scale-{fam}-n{n}-hole"
                m, e = F.value(key, src, arm, tierA, mach)
                iv = F.invalid_of(key, arm, tierA)
                bad = iv is not None and iv > F.BROKEN_INVALID
                pts.append((n, m, e))
                flags.append(bad)
            if all(m is None for _, m, _ in pts):
                continue
            # A point whose denominator is verbosity-selected cannot carry a
            # verdict: exclude it from the classification, but still SHOW it,
            # marked, so the exclusion is visible rather than inferable.
            usable = [p for p, b in zip(pts, flags) if not b]
            verdict, d, rho = classify(usable)
            if any(flags):
                verdict += " (excl. %s)" % ",".join(
                    f"n={p[0]}" for p, b in zip(pts, flags) if b)
            b, _ = F.value(key, src, "base", tierA, mach)
            # `bad`, not `b`: `b` is the base value bound just above. The
            # comprehension scopes its own name so this was correct either way,
            # but two different `b`s one line apart is a trap.
            cells = ["—" if m is None else (f"{m:.3f}!" if bad else f"{m:.3f}")
                     for (_, m, _), bad in zip(pts, flags)]
            out.append(
                f"| {title} | " + " | ".join(cells) +
                f" | {'—' if b is None else f'{b:.3f}'}"
                f" | {'—' if d is None else f'{d:+.3f}'}"
                f" | **{verdict}** | {'—' if rho is None else f'{rho:+.2f}'} |")
            if verdict.split(" ")[0] in ("rising", "saturating"):
                decision.append((fam, title, verdict, d))
        out.append("")

        # the control: does the hole-nohole gap widen at the endpoints?
        ends = [1, max(S.RUNG_NS)]
        rows = []
        for key, title, _y, src in F.PANELS:
            gaps = []
            for n in ends:
                h, _ = F.value(key, src, f"scale-{fam}-n{n}-hole", tierA, mach)
                c, _ = F.value(key, src, f"scale-{fam}-n{n}-nohole", tierA, mach)
                gaps.append(None if (h is None or c is None) else h - c)
            if any(g is not None for g in gaps):
                w = (None if None in gaps else gaps[1] - gaps[0])
                rows.append(f"| {title} | "
                            + " | ".join("—" if g is None else f"{g:+.3f}"
                                         for g in gaps)
                            + f" | {'—' if w is None else f'{w:+.3f}'} |")
        if rows:
            out += ["### control: hole - nohole at the endpoints", "",
                    "| metric | gap @ n=1 | gap @ n=8 | widening |",
                    "|---|---|---|---|"] + rows + [""]

    # `saturating` COUNTS as a positive dose-response. It means the curve rose
    # and then plateaued -- often because the metric hit its ceiling -- which is
    # one of the three shapes the plan asks to distinguish, not a null. An
    # earlier version of this gate counted only `rising`, and so reported four
    # rho=+1.00 monotone synthetic curves as "no panel clears the bar", which is
    # the opposite of what the data says.
    up = [d for d in decision if d[2] in ("rising", "saturating")]
    out += ["## pass-1 decision", ""]
    if up:
        byfam = {}
        for f, t, v, dd in up:
            byfam.setdefault(f, []).append(f"{t} ({dd:+.3f}, {v})")
        out.append(f"{len(up)} panel(s) show a positive dose-response "
                   "(rising or saturating):")
        out.append("")
        for f, items in byfam.items():
            out.append(f"- **{f}**: " + "; ".join(items))
        out += ["",
                "The plan gates seeds 2-3 on pass 1 rising, so this qualifies. "
                "Before reporting any of it as an effect of #envs, note the "
                "one-seed caveat above, and check whether a `saturating` "
                "verdict is a real plateau or the metric hitting its CEILING — "
                "a rate at 0.97 cannot rise further whatever the cause."]
    else:
        out.append("No panel shows a positive dose-response. Per the plan, a "
                   "ragged or flat pass 1 means the effect is fragile and seeds "
                   "are needed before believing anything — including the null.")
    out.append("")

    txt = "\n".join(out)
    print(txt)
    if a.md:
        Path(a.md).write_text(txt + "\n")
        print(f"\nwrote {a.md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
