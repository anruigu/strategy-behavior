#!/usr/bin/env python3
"""Deck-tuned variants of two existing figures (0824-send deck).

1. frame_effect_bars.png — the frame-effect chart alone (the prompt cards are
   HTML in the deck now). Data frozen from results/ablate-frame-summary.json,
   same as research_logs/figs/make_frame_effect_fig.py.
2. eval_suite_matrix_27b.png — hole_exp/results/make_transfer_fig.py without
   the suptitle/footnote prose, centered. Numbers identical.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["text.parse_math"] = False
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch

OUT = Path(__file__).resolve().parent
GAME, NAT = "#eb6834", "#2a78d6"
INK, INK2, MUT = "#0b0b0b", "#52514e", "#898781"
GRID, SURF, PAGE = "#e1e0d9", "#fcfcfb", "#f9f9f7"
HATCH, GRAY = "#c3c2b7", "#e1e0d9"

DATA = {
    "Qwen3.6-27B": {
        "explicit":  (0.728, 0.270),
        "rules":     (0.290, 0.303),
        "menu":      (0.316, 0.172),
        "oppo_menu": (0.136, 0.056),
    },
    "Qwen3.5-9B": {
        "explicit":  (0.568, 0.267),
        "rules":     (0.315, 0.092),
        "menu":      (0.270, 0.142),
        "oppo_menu": (0.226, 0.037),
    },
}
PLANTS = ["explicit", "rules", "menu", "oppo_menu"]
GLOSS = {"explicit": "brief states\nit pays", "rules": "named in\nthe rules",
         "menu": "in the move\nmenu only", "oppo_menu": "menu +\ntempter"}


def frame_bars():
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.8), dpi=150, sharey=True)
    fig.patch.set_facecolor(PAGE)
    for ax, (model, d) in zip(axes, DATA.items()):
        ax.set_facecolor(SURF)
        bw = 0.38
        for y in (0.2, 0.4, 0.6, 0.8):
            ax.axhline(y, color=GRID, lw=0.8, zorder=0)
        for i, p in enumerate(PLANTS):
            g, n = d[p]
            for val, off, col in ((g, -bw/2 - 0.012, GAME), (n, bw/2 + 0.012, NAT)):
                ax.bar(i + off, val, bw, color=col, edgecolor=SURF, lw=1.5, zorder=3)
                ax.text(i + off, val + 0.02, f"{val*100:.0f}", ha="center",
                        va="bottom", color=col, fontsize=9, fontweight="bold")
        ax.set_xticks(range(len(PLANTS)))
        ax.set_xticklabels([GLOSS[p] for p in PLANTS], fontsize=8.5, color=INK2)
        ax.set_ylim(0, 0.85)
        ax.set_title(model, fontsize=11, fontweight="bold", color=INK, loc="left")
        ax.spines[["top", "right"]].set_visible(False)
        ax.spines[["left", "bottom"]].set_color(GRID)
        ax.tick_params(colors=INK2)
        ax.set_xlabel("planting method → less obvious the exploit exists",
                      fontsize=8.5, color=MUT)
    axes[0].set_ylabel("hack rate (share of decisions)", fontsize=9.5, color=INK2)
    axes[1].legend(handles=[Patch(facecolor=GAME, label="game frame"),
                            Patch(facecolor=NAT, label="natural frame")],
                   frameon=False, fontsize=9.5, loc="upper right")
    fig.tight_layout()
    fig.savefig(OUT / "frame_effect_bars.png", facecolor=PAGE,
                bbox_inches="tight", pad_inches=0.15)
    print("wrote", OUT / "frame_effect_bars.png")


ROWS = [
    ("MACHIAVELLI",            "+12.4 viol",  "+7.6",  "yes", "yes", "p<0.01"),
    ("Insider-trading",        "+0.72 trade", "+0.24", "yes", "yes", ""),
    ("In-context scheming",    "+0.11 scheme","+0.075","yes", "yes", "exfil DiD +0.20"),
    ("AgentMisalignment",      "+0.14 frac",  "+0.13", "yes", "yes", "frac-any"),
    ("Hack-Verifiable TArena", "+0.065 hack", "-0.03", "yes", "null","eval is game-framed"),
    ("School-of-Reward-Hacks", "+0.01",       "+0.01", "null","null",""),
    ("Denison reward-tamper",  "0.00",        "0.00",  "null","null","0% all arms"),
    ("DarkBench",              "+0.015",      "+0.03", "null","null","within SE"),
    ("Sandbagging",            "+0.011",      "+0.01", "null","null",""),
    ("Social games",           "-0.012",      "-0.03", "null","null","underpowered"),
    ("ImpossibleBench",        "—",           "—",     "blocked","blocked","needs sandbox"),
    ("EvilGenie",              "—",           "—",     "blocked","blocked","needs sandbox"),
    ("Terminal-Bench",         "—",           "—",     "blocked","blocked","needs sandbox"),
]
CATCOL = {"yes": NAT, "null": GRAY, "blocked": "white"}
CATTXT = {"yes": "white", "null": INK2, "blocked": MUT}


def cell(ax, x, y, w, h, cat, label):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=CATCOL[cat],
                           ec=(HATCH if cat == "blocked" else SURF),
                           linewidth=1.5, hatch="///" if cat == "blocked" else None))
    ax.text(x + w/2, y + h/2, label, ha="center", va="center",
            fontsize=10, fontweight="bold", color=CATTXT[cat])


def eval_matrix():
    n = len(ROWS)
    fig, ax = plt.subplots(figsize=(9.4, 8.0), dpi=150)
    fig.patch.set_facecolor(PAGE); ax.set_facecolor(PAGE)
    ax.set_xlim(0, 9.4); ax.set_ylim(2.55, n + 1.9); ax.axis("off")
    x_name, x_tr, x_in = 0.1, 3.1, 6.0
    w_tr = w_in = 2.7
    rh = 0.82
    top = n + 0.6
    ax.text(x_tr + w_tr/2, top + 0.62, "Disposition transfers?", fontsize=10.5,
            fontweight="bold", color=INK, ha="center")
    ax.text(x_tr + w_tr/2, top + 0.28, "natural  hole − nohole", fontsize=8.5,
            color=MUT, ha="center")
    ax.text(x_in + w_in/2, top + 0.62, "Game-reframing inoculates?", fontsize=10.5,
            fontweight="bold", color=INK, ha="center")
    ax.text(x_in + w_in/2, top + 0.28, "DiD = natural Δ − game Δ", fontsize=8.5,
            color=MUT, ha="center")
    for i, (name, nat, did, tr, inoc, note) in enumerate(ROWS):
        y = top - 0.15 - (i + 1) * rh
        if tr == "yes":
            ax.add_patch(Rectangle((x_name - 0.05, y), 9.3, rh,
                                   facecolor="#f2f7fe", edgecolor="none", zorder=0))
        ax.text(x_name, y + rh/2, name, fontsize=10, color=INK, va="center",
                fontweight="bold")
        cell(ax, x_tr, y + 0.06, w_tr, rh - 0.12, tr, nat)
        cell(ax, x_in, y + 0.06, w_in, rh - 0.12, inoc, did)
        if note:
            ax.text(x_in + w_in + 0.12, y + rh/2, note, fontsize=8, color=MUT,
                    va="center", style="italic")
    fig.legend(handles=[Patch(facecolor=NAT, label="effect"),
                        Patch(facecolor=GRAY, label="null"),
                        Patch(facecolor="white", edgecolor=HATCH, hatch="///",
                              label="blocked (needs sandbox)")],
               loc="lower center", ncol=3, frameon=False, fontsize=9,
               bbox_to_anchor=(0.5, 0.01))
    fig.subplots_adjust(top=0.985, bottom=0.07, left=0.02, right=0.98)
    fig.savefig(OUT / "eval_suite_matrix_27b.png", facecolor=PAGE,
                bbox_inches="tight", pad_inches=0.2)
    print("wrote", OUT / "eval_suite_matrix_27b.png")


if __name__ == "__main__":
    frame_bars()
    eval_matrix()
