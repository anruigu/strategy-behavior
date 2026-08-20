#!/usr/bin/env python3
"""Consolidated EVAL_SUITE transfer figure for the game/natural inoculation
ablation (0819/0820), 27B seed 0. Instruments use incommensurable metrics, so
this is a results MATRIX: per benchmark, (a) does the disposition transfer
(natural-frame hole - nohole) and (b) does game-reframing inoculate
(DiD = natural effect - game effect). Cells coded by category, raw effects
annotated. Numbers are frozen from the per-arm result JSONs.
"""
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["text.parse_math"] = False
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
from pathlib import Path

BLUE, GRAY, HATCH = "#2a78d6", "#e1e0d9", "#c3c2b7"
INK, INK2, MUT, PAGE, SURF = "#0b0b0b", "#52514e", "#898781", "#f9f9f7", "#fcfcfb"

# (benchmark, tier, natural-effect str, DiD str, transfers, inoculates, note)
# transfers/inoculates in {"yes","null","blocked"}
ROWS = [
    ("MACHIAVELLI",            "T2", "+12.4 viol",  "+7.6",  "yes", "yes", "p<0.01"),
    ("Insider-trading",        "T3", "+0.72 trade", "+0.24", "yes", "yes", ""),
    ("In-context scheming",    "T2", "+0.11 scheme","+0.075","yes", "yes", "exfil DiD +0.20"),
    ("AgentMisalignment",      "T2", "+0.14 frac",  "+0.13", "yes", "yes", "frac-any"),
    ("Hack-Verifiable TArena", "T1", "+0.065 hack", "-0.03", "yes", "null","eval is game-framed"),
    ("School-of-Reward-Hacks", "T1", "+0.01",       "+0.01", "null","null",""),
    ("Denison reward-tamper",  "T1", "0.00",        "0.00",  "null","null","0% all arms"),
    ("DarkBench",              "T3", "+0.015",      "+0.03", "null","null","within SE"),
    ("Sandbagging",            "T2", "+0.011",      "+0.01", "null","null",""),
    ("Social games",           "T0", "-0.012",      "-0.03", "null","null","underpowered"),
    ("ImpossibleBench",        "T1", "—",           "—",     "blocked","blocked","needs sandbox"),
    ("EvilGenie",              "T1", "—",           "—",     "blocked","blocked","needs sandbox"),
    ("Terminal-Bench",         "T1", "—",           "—",     "blocked","blocked","needs sandbox"),
]

CATCOL = {"yes": BLUE, "null": GRAY, "blocked": "white"}
CATTXT = {"yes": "white", "null": INK2, "blocked": MUT}


def cell(ax, x, y, w, h, cat, label):
    hatch = "///" if cat == "blocked" else None
    ax.add_patch(Rectangle((x, y), w, h, facecolor=CATCOL[cat], edgecolor=SURF,
                           linewidth=1.5, hatch=hatch,
                           ec=(HATCH if cat == "blocked" else SURF)))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
            fontsize=10, fontweight="bold", color=CATTXT[cat])


def main():
    n = len(ROWS)
    fig, ax = plt.subplots(figsize=(11.2, 8.6), dpi=150)
    fig.patch.set_facecolor(PAGE); ax.set_facecolor(PAGE)
    ax.set_xlim(0, 10); ax.set_ylim(0, n + 2.2); ax.axis("off")

    # column x-positions
    x_name, x_tier, x_tr, x_in = 0.1, 3.3, 4.2, 7.1
    w_tr = w_in = 2.7
    rh = 0.82
    top = n + 1.0

    # headers
    ax.text(x_name, top + 0.5, "Instrument", fontsize=11, fontweight="bold", color=INK)
    ax.text(x_tr + w_tr/2, top + 0.62, "Disposition transfers?", fontsize=10.5,
            fontweight="bold", color=INK, ha="center")
    ax.text(x_tr + w_tr/2, top + 0.28, "natural  hole − nohole", fontsize=8.5,
            color=MUT, ha="center")
    ax.text(x_in + w_in/2, top + 0.62, "Game-reframing inoculates?", fontsize=10.5,
            fontweight="bold", color=INK, ha="center")
    ax.text(x_in + w_in/2, top + 0.28, "DiD = natural Δ − game Δ", fontsize=8.5,
            color=MUT, ha="center")

    for i, (name, tier, nat, did, tr, inoc, note) in enumerate(ROWS):
        y = top - 0.5 - (i + 1) * rh
        # row band tint for the "transfers" group
        if tr == "yes":
            ax.add_patch(Rectangle((x_name-0.05, y), 9.9, rh, facecolor="#f2f7fe",
                                   edgecolor="none", zorder=0))
        ax.text(x_name, y + rh/2, name, fontsize=10, color=INK, va="center", fontweight="bold")
        ax.text(x_tier, y + rh/2, tier, fontsize=9, color=MUT, va="center")
        cell(ax, x_tr, y+0.06, w_tr, rh-0.12, tr, nat)
        cell(ax, x_in, y+0.06, w_in, rh-0.12, inoc, did)
        if note:
            ax.text(x_in + w_in + 0.15, y + rh/2, note, fontsize=8, color=MUT,
                    va="center", style="italic")

    fig.suptitle("EVAL_SUITE transfer — does the trained exploitative disposition generalise, "
                 "and does game-reframing inoculate it?",
                 fontsize=13.5, fontweight="bold", color=INK, x=0.02, ha="left", y=0.985)
    fig.text(0.02, 0.945,
             "Qwen3.6-27B · seed 0 · matched hole/nohole per frame · both hole arms exploit "
             "~equally in-env (~0.97–1.0), so transfer differences are framing, not amount.",
             fontsize=9, color=INK2)
    fig.legend(handles=[Patch(facecolor=BLUE, label="effect"),
                        Patch(facecolor=GRAY, label="null"),
                        Patch(facecolor="white", edgecolor=HATCH, hatch="///", label="blocked (needs sandbox)")],
               loc="lower center", ncol=3, frameon=False, fontsize=9, bbox_to_anchor=(0.5, 0.005))
    fig.text(0.02, 0.045,
             "Reads: the disposition transfers to deception / exploitation / self-preservation / "
             "verifier-hacking (top 5, blue), and is null on metric-gaming, self-reward-tampering, "
             "chat dark-patterns, sandbagging and cooperation. Game-reframing inoculates 4 of the 5 "
             "that transfer; the exception (Hack-Verifiable) is itself game-framed.",
             fontsize=8.5, color=INK2)
    fig.subplots_adjust(top=0.90, bottom=0.10, left=0.02, right=0.98)
    out = Path(__file__).resolve().parent / "eval_suite_transfer_27b.png"
    fig.savefig(out, facecolor=PAGE, bbox_inches="tight", pad_inches=0.2)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
