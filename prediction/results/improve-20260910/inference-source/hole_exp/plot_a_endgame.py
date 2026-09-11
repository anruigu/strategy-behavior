#!/usr/bin/env python3
"""A's figure and table: where in the episode does defection start?

    python plot_a_endgame.py results/think4_evals/A_endgame_length.jsonl

THE DISCRIMINATING READ, stated before looking (PLAN A.2):

    learned the STRUCTURE   first-defect index tracks N; mode near N-1 at
                            every length. At N=6 defection concentrates at
                            4-5; at N=14 at 12-13.
    memorised a POSITION    mode sits near 8-9 regardless of N. At N=6 there
                            is little or no late spike, because round 9 does
                            not exist. At N=14 the spike is still at 8-9 with
                            a flat tail after it.

`endgame_rate` is NOT plotted and must not be used for this: it is defined
relative to the per-episode horizon, so it re-centres on the true final round
whether or not the policy does.

The `_inf` arms are the NEGATIVE CONTROL. `core.scrub_horizon` removes the
stated total, so those policies cannot know N and their timing must NOT track
it. If an `inf` arm tracks N as strongly as a finite arm, the effect is a
measurement artefact and the finite arms' result does not stand.

COLOUR IS ORDINAL. Episode length is three ordered levels, so one hue
light->dark, never three unrelated hues -- a categorical palette here would
discard the ordering that is the entire point.
"""
from __future__ import annotations
import argparse, json, pathlib, statistics as st, collections

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt   # noqa: E402

# documented blue ramp, ordinal constraint: light mode starts no lighter
# than step 250
RAMP = {6: "#86b6ef", 10: "#2a78d6", 14: "#0d366b"}
INK = {"surface": "#fcfcfb", "primary": "#0b0b0b",
       "secondary": "#52514e", "grid": "#e6e5e1"}


def load(p):
    return [json.loads(l) for l in pathlib.Path(p).open()]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("rows")
    ap.add_argument("--step", type=int, default=None)
    a = ap.parse_args()
    rows = load(a.rows)
    if a.step is not None:
        rows = [r for r in rows if r["step"] == a.step]
    if not rows:
        print("no rows"); return 1

    arms = sorted({r["arm"] for r in rows})
    lens = sorted({r["num_rounds"] for r in rows})

    # ---- the sanity gate, printed before anything else -------------------
    print("LENGTH GATE -- decisions actually played, by requested length:")
    for n in lens:
        d = [r["n_decisions"] for r in rows if r["num_rounds"] == n]
        print(f"   num_rounds={n:3d} -> {st.mean(d):5.2f} decisions (n={len(d)})")
    if len({round(st.mean([r['n_decisions'] for r in rows
                           if r['num_rounds'] == n]), 1) for n in lens}) < len(lens):
        print("   ** LENGTHS DID NOT SEPARATE -- nothing below is meaningful **")
        return 1

    # ---- the table -------------------------------------------------------
    print(f"\nFIRST-DEFECT INDEX (0-based). 'tracks N' wants mode ~ N-2..N-1.")
    print(f"   {'arm':12s} " + " ".join(f"{'N='+str(n):>22s}" for n in lens))
    print(f"   {'':12s} " + " ".join(f"{'median  mode   none%':>22s}" for n in lens))
    for arm in arms:
        cells = []
        for n in lens:
            sel = [r for r in rows if r["arm"] == arm and r["num_rounds"] == n]
            idx = [r["first_defect_index"] for r in sel
                   if r["first_defect_index"] is not None]
            none_pct = 1 - len(idx) / len(sel) if sel else 0
            if idx:
                mode = collections.Counter(idx).most_common(1)[0][0]
                cells.append(f"{st.median(idx):6.1f} {mode:5d} {none_pct:7.0%}")
            else:
                cells.append(f"{'--':>6s} {'--':>5s} {none_pct:7.0%}")
        print(f"   {arm:12s} " + " ".join(f"{c:>22s}" for c in cells))

    # ---- the figure ------------------------------------------------------
    cols = min(3, len(arms)) or 1
    figrows = (len(arms) + cols - 1) // cols
    fig, axes = plt.subplots(figrows, cols, figsize=(4.7 * cols, 3.5 * figrows),
                             squeeze=False, sharey=True)
    fig.patch.set_facecolor(INK["surface"])
    for i, arm in enumerate(arms):
        ax = axes[i // cols][i % cols]
        ax.set_facecolor(INK["surface"])
        for n in lens:
            idx = [r["first_defect_index"] for r in rows
                   if r["arm"] == arm and r["num_rounds"] == n
                   and r["first_defect_index"] is not None]
            if not idx:
                continue
            c = collections.Counter(idx)
            xs = sorted(c)
            tot = sum(c.values())
            ax.plot(xs, [c[x] / tot for x in xs], color=RAMP.get(n, "#2a78d6"),
                    linewidth=2.0, marker="o", markersize=5,
                    markeredgecolor=INK["surface"], markeredgewidth=1.2,
                    label=f"N = {n}", zorder=3)
            # the round the policy would aim at if it tracked N
            ax.axvline(n - 1, color=RAMP.get(n, "#2a78d6"), linewidth=1.0,
                       linestyle=":", alpha=0.7, zorder=1)
        ax.set_title(arm + ("   (negative control)" if arm.endswith("/inf") else ""),
                     color=INK["primary"], fontsize=11, loc="left", pad=8)
        ax.grid(True, color=INK["grid"], linewidth=0.8); ax.set_axisbelow(True)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("bottom", "left"):
            ax.spines[s].set_color(INK["grid"])
        ax.tick_params(colors=INK["secondary"], labelsize=9)
    for j in range(len(arms), figrows * cols):
        axes[j // cols][j % cols].set_visible(False)

    h, l = axes[0][0].get_legend_handles_labels()
    leg = fig.legend(h, l, loc="upper right", ncol=len(lens), frameon=False,
                     fontsize=9, title="episode length (dotted = round N-1)",
                     title_fontsize=9)
    for t in leg.get_texts():
        t.set_color(INK["secondary"])
    leg.get_title().set_color(INK["secondary"])
    fig.suptitle("Does defection track the true final round, or a memorised position?",
                 color=INK["primary"], fontsize=13, x=0.01, ha="left", y=0.995)
    fig.supxlabel("round index of the FIRST defection", color=INK["secondary"],
                  fontsize=10, y=0.03)
    fig.supylabel("share of episodes", color=INK["secondary"], fontsize=10)
    fig.tight_layout(rect=[0.02, 0.05, 1, 0.95])
    out = pathlib.Path(a.rows).with_name("A_first_defect.png")
    fig.savefig(out, dpi=170, facecolor=INK["surface"])
    print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
