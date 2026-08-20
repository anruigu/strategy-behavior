#!/usr/bin/env python3
"""Env-scaling: does training on MORE exploitable environments produce a larger
transfer effect? Natural frame, treatment effect (hole - nohole) vs #training
envs {6,9,21}, on two OOD instruments (MACHIAVELLI violations, insider-trading).
CAVEAT flagged on the plot: the 6-env run trained 60 steps; 9- and 21-env trained
90 steps, so only 9-vs-21 (matched steps) is a clean env-count comparison.
"""
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["text.parse_math"] = False
import matplotlib.pyplot as plt
from pathlib import Path

BLUE, ORANGE, INK, INK2, MUT, GRID, SURF, PAGE = ("#2a78d6","#eb6834","#0b0b0b",
    "#52514e","#898781","#e1e0d9","#fcfcfb","#f9f9f7")

ENVS   = [6, 9, 21]
STEPS  = [60, 90, 90]
MACH_D = [12.4, 22.9, 24.4]     # MACHIAVELLI violations Δ (hole - nohole)
INS_D  = [0.72, 0.97, 0.78]     # insider trade-rate Δ


def panel(ax, y, ylab, color, title, ymax):
    ax.set_facecolor(SURF)
    for g in ax.get_yticks():
        pass
    # line through the two matched-step points (9,21) solid; 6->9 dashed (confound)
    ax.plot(ENVS[1:], y[1:], "-", color=color, lw=2, zorder=2)
    ax.plot(ENVS[:2], y[:2], "--", color=color, lw=1.6, alpha=0.6, zorder=2)
    for x, yy, st in zip(ENVS, y, STEPS):
        filled = st == 90
        ax.scatter([x], [yy], s=130, color=(color if filled else "white"),
                   edgecolor=color, linewidth=2, zorder=3)
        ax.annotate(f"{yy:g}", (x, yy), textcoords="offset points", xytext=(0, 12),
                    ha="center", fontsize=10, fontweight="bold", color=color)
        ax.annotate(f"{st} steps", (x, yy), textcoords="offset points", xytext=(0, -18),
                    ha="center", fontsize=7.5, color=MUT)
    ax.set_xticks(ENVS); ax.set_xticklabels([f"{e}" for e in ENVS], fontsize=10, color=INK)
    ax.set_xlabel("# training environments", fontsize=10, color=INK2)
    ax.set_ylabel(ylab, fontsize=10, color=INK2)
    ax.set_ylim(0, ymax); ax.set_xlim(3, 24)
    ax.set_title(title, fontsize=11.5, fontweight="bold", color=INK, loc="left", pad=8)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.spines["left"].set_color("#c3c2b7"); ax.spines["bottom"].set_color("#c3c2b7")
    ax.tick_params(length=0); ax.grid(axis="y", color=GRID, lw=0.8)


def main():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), dpi=150)
    fig.patch.set_facecolor(PAGE)
    panel(axes[0], MACH_D, "MACHIAVELLI violations Δ  (hole − nohole)", BLUE,
          "MACHIAVELLI (has headroom)", 30)
    panel(axes[1], INS_D, "insider trade-rate Δ  (hole − nohole)", ORANGE,
          "Insider-trading (near ceiling)", 1.1)
    fig.suptitle("Does scaling the number of training environments increase transfer? "
                 "(natural frame, 27B, seed 0)",
                 fontsize=13, fontweight="bold", color=INK, x=0.02, ha="left", y=0.99)
    fig.text(0.02, 0.925,
             "Filled = 90 training steps (9- & 21-env); open = 60 steps (6-env). "
             "Only 9→21 (solid, matched steps) is a clean env-count comparison — and it is flat.",
             fontsize=8.5, color=INK2)
    fig.text(0.02, 0.02,
             "Read: matched at 90 steps, 9→21 envs is flat (MACH +22.9→+24.4; insider "
             "+0.97→+0.78) — more environments beyond ~9 does NOT increase transfer. The "
             "6→9 rise is confounded with training steps (60→90), so it can't be attributed "
             "to env count. To settle 6-vs-more, re-run 6-env at 90 steps.",
             fontsize=8.5, color=INK2)
    fig.subplots_adjust(top=0.83, bottom=0.20, left=0.075, right=0.97, wspace=0.28)
    out = Path(__file__).resolve().parent / "env_scaling_curve_27b.png"
    fig.savefig(out, facecolor=PAGE, bbox_inches="tight", pad_inches=0.2)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
