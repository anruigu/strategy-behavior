#!/usr/bin/env python3
"""Figures for the same-game capability eval and the live cross-play.

    python make_capability_figs.py

  capability.png  Did the arms get BETTER at the ten games they trained on?
                  Skill against the scripted honest reference, in both the
                  priced and unpriced condition, plus the exploit rate that
                  explains the gap and a per-env consistency check.
  crossplay.png   Do they play differently against a LIVE opponent on five
                  never-trained games? Style counters beside outcomes, because
                  an adaptive opponent makes those move in opposite directions.

Palette: base / hole / nohole are an identity encoding, so they take three
categorical hues in a fixed order and are never recoloured when a panel drops a
series. #7a5bd6 / #eb6834 / #2a78d6 passes all six checks of the validator on
the light surface (worst adjacent CVD dE 24.7 protan, normal 30.9, contrast
>= 3:1). A green third hue was rejected: green-orange collides at dE 2.9 under
protanopia, which is invisible rather than merely hard.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["text.parse_math"] = False
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
CAP = HERE / "results" / "capability" / "same-game-capability.json"
XP = HERE / "results" / "crossplay"
FIGS = Path("/workspace/allie/strategy-behavior/results/0822_capability_plots")

PURPLE, ORANGE, BLUE = "#7a5bd6", "#eb6834", "#2a78d6"
INK, INK2, MUT, GRID, SURF, PAGE = ("#0b0b0b", "#52514e", "#898781",
                                    "#e1e0d9", "#fcfcfb", "#f9f9f7")
ARMCOL = {"base": PURPLE, "hole": ORANGE, "nohole": BLUE}
ARMS = ["base", "hole", "nohole"]
COND = [("nohole", "exploit PRICED\n(detection certain, penalty > premium)"),
        ("hole", "exploit UNPRICED\n(the training condition)")]


def style(ax, title, ylab, xlab=""):
    ax.set_facecolor(SURF)
    ax.set_title(title, fontsize=10.5, fontweight="bold", color=INK,
                 loc="left", pad=7)
    ax.set_ylabel(ylab, fontsize=8.5, color=INK2)
    if xlab:
        ax.set_xlabel(xlab, fontsize=8.5, color=INK2)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#c3c2b7")
    ax.tick_params(length=0, labelsize=8.5, colors=INK2)
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)


def grouped(ax, get, ylab, title, zero_rule=None, zero_label=""):
    """One group per condition, one dot per arm, with a meaningful zero."""
    style(ax, title, ylab)
    width = 0.24
    for gi, (cond, _lab) in enumerate(COND):
        for ai, arm in enumerate(ARMS):
            m, se = get(arm, cond)
            if m is None:
                continue
            x = gi + (ai - 1) * width
            if se:
                ax.errorbar([x], [m], yerr=[se], fmt="none", ecolor=ARMCOL[arm],
                            elinewidth=1.6, capsize=3, alpha=0.6, zorder=2)
            ax.scatter([x], [m], s=90, color=ARMCOL[arm], edgecolor=SURF,
                       linewidth=2, zorder=4)
            ax.annotate(f"{m:+.2f}" if zero_rule is not None else f"{m:.2f}",
                        (x, m), textcoords="offset points",
                        xytext=(0, 11 if ai != 1 else -16), ha="center",
                        fontsize=8, fontweight="bold", color=ARMCOL[arm])
    if zero_rule is not None:
        ax.axhline(zero_rule, color=MUT, lw=1.3, ls=(0, (4, 3)), zorder=1)
        if zero_label:
            ax.annotate(zero_label, xy=(0.012, zero_rule),
                        xycoords=("axes fraction", "data"), fontsize=7.5,
                        color=MUT, va="bottom", ha="left")
    ax.set_xticks(range(len(COND)))
    ax.set_xticklabels([lab for _c, lab in COND], fontsize=8, color=INK2)
    ax.set_xlim(-0.55, len(COND) - 0.45)


def fig_capability(d):
    S = d["summary"]
    envs = d["envs"]

    def get(field):
        def f(arm, cond):
            x = S.get(arm, {}).get(cond, {}).get(field)
            return (x["mean"], x["se"]) if x else (None, None)
        return f

    fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.6))
    fig.patch.set_facecolor(PAGE)

    grouped(axes[0], get("skill"),
            "skill  (payoff - scripted honest, payoff-scale units)",
            "Did they get better at the game?", zero_rule=0.0,
            zero_label="scripted honest play")
    grouped(axes[1], get("exploit_rate"), "exploit rate",
            "Do they take the hole when it is punished?")
    # Per-env consistency in the PRICED condition -- the only one where skill
    # is not contaminated by the hole.
    ax = axes[2]
    style(ax, "Per-env skill vs base  (exploit priced)",
          "skill difference from base")
    ax.axhline(0, color=MUT, lw=1.3, ls=(0, (4, 3)), zorder=1)
    for arm in ("hole", "nohole"):
        xs, ys = [], []
        for i, e in enumerate(envs):
            a = S[arm]["nohole"]["per_env"][e]["skill"]["mean"]
            b = S["base"]["nohole"]["per_env"][e]["skill"]["mean"]
            if a is not None and b is not None:
                xs.append(i); ys.append(a - b)
        ax.scatter(xs, ys, s=70, color=ARMCOL[arm], edgecolor=SURF,
                   linewidth=1.6, zorder=4, label=arm)
    ax.set_xticks(range(len(envs)))
    ax.set_xticklabels(envs, rotation=45, ha="right", fontsize=7.5)
    ax.legend(frameon=False, fontsize=8.5, loc="lower left")

    # A legend for all three arms: the left two panels distinguish them by hue
    # only, and the per-env panel's legend covers just hole/nohole (base is its
    # zero line), so without this arm identity would be colour-alone.
    from matplotlib.lines import Line2D
    fig.legend([Line2D([], [], marker="o", ls="", markersize=9,
                       markerfacecolor=ARMCOL[a], markeredgecolor=SURF,
                       markeredgewidth=2) for a in ARMS],
               [f"{a} arm" for a in ARMS], loc="upper left", frameon=False,
               fontsize=9.5, ncol=3, bbox_to_anchor=(0.008, 0.925))
    fig.suptitle("Same-game capability: the ten cells these arms trained on",
                 fontsize=13.5, fontweight="bold", color=INK, x=0.008,
                 ha="left", y=0.995)
    fig.text(0.008, 0.955,
             f"Qwen3.6-27B, 10-env mixed pair, {d['seeds']} seeds/cell  ·  "
             "skill subtracts a scripted honest replay of the SAME seed against "
             "the SAME opponent, so it removes per-seed difficulty",
             fontsize=9, color=INK2, ha="left", va="top")
    fig.text(0.008, 0.012,
             "Left/middle: dots are arms, grouped by whether exploiting is "
             "punished. Bars are episode-level bootstrap SE. In the PRICED "
             "condition the hole is a losing move, so skill there is game skill "
             "and not the hole.\nRight: each dot is one of the ten trained "
             "environments; above zero = better than base on that cell.",
             fontsize=7.5, color=MUT, ha="left", va="bottom", linespacing=1.5)
    fig.tight_layout(rect=(0, 0.06, 1, 0.87))
    FIGS.mkdir(parents=True, exist_ok=True)
    dest = FIGS / "capability.png"
    fig.savefig(dest, dpi=170, facecolor=PAGE)
    plt.close(fig)
    return dest


XP_PANELS = [
    ("xp_blind_auction", "bid_fraction_of_capital", True,
     "Auction: capital committed", "sum of bids / starting capital"),
    ("xp_blind_auction", "mean_msg_chars", True,
     "Auction: talk volume", "mean message length (chars)"),
    ("xp_negotiation", "mean_ask_ratio", True,
     "Negotiation: ask ratio", "requested / offered line-items"),
    ("xp_indian_poker", "aggression_rate", True,
     "Poker: aggression", "share of actions that bet or raise"),
    ("xp_blind_auction", "win", False, "Auction: outcome", "win rate"),
    ("xp_indian_poker", "win", False, "Poker: outcome", "win rate"),
]


def fig_crossplay():
    data = {}
    for arm in ARMS:
        for opp in ("base", "frontier"):
            f = XP / f"{arm}__vs__{opp}.json"
            if f.exists():
                data[(arm, opp)] = json.loads(f.read_text())["summary"]
    if not data:
        print("no crossplay results yet")
        return None
    opps = [o for o in ("base", "frontier")
            if any((a, o) in data for a in ARMS)]

    fig, axes = plt.subplots(2, 3, figsize=(15.5, 8.0))
    fig.patch.set_facecolor(PAGE)
    for i, (game, key, is_style, title, ylab) in enumerate(XP_PANELS):
        ax = axes[i // 3][i % 3]
        style(ax, title, ylab)
        width = 0.24
        for gi, opp in enumerate(opps):
            for ai, arm in enumerate(ARMS):
                s = data.get((arm, opp), {}).get(game)
                if not s:
                    continue
                v = s["style"].get(key) if is_style else s.get(key)
                if v is None:
                    continue
                x = gi + (ai - 1) * width
                ax.bar([x], [v], width=width * 0.86, color=ARMCOL[arm],
                       edgecolor=SURF, linewidth=2, zorder=3,
                       label=arm if i == 0 and gi == 0 else None)
                ax.annotate(f"{v:.2f}" if v < 100 else f"{v:.0f}", (x, v),
                            textcoords="offset points", xytext=(0, 3),
                            ha="center", fontsize=7.5, color=ARMCOL[arm],
                            fontweight="bold")
        ax.set_xticks(range(len(opps)))
        ax.set_xticklabels([f"vs {o}" for o in opps], fontsize=9, color=INK2)
        ax.set_xlim(-0.55, len(opps) - 0.45)

    handles, labels = axes[0][0].get_legend_handles_labels()
    if handles:
        fig.legend(handles, labels, loc="upper left", frameon=False,
                   fontsize=9.5, ncol=3, bbox_to_anchor=(0.008, 0.935))
    fig.suptitle("Cross-play against a live opponent, on games never trained on",
                 fontsize=13.5, fontweight="bold", color=INK, x=0.008,
                 ha="left", y=0.995)
    fig.text(0.008, 0.962,
             "16 seeds/cell  ·  opponent is Qwen3.6-27B base, or "
             "claude-opus-5 via OpenRouter  ·  same seat and same seed for "
             "every arm",
             fontsize=9, color=INK2, ha="left", va="top")
    fig.text(0.008, 0.012,
             "TOP ROW IS STYLE, BOTTOM ROW IS OUTCOME, and they disagree. A "
             "live opponent adapts: it concedes less to a harder push, so the "
             "hole arm can behave more aggressively and still take less home. "
             "Reading outcomes alone would invert the behavioural finding.\n"
             "The frontier opponent is not seedable (OpenRouter exposes no "
             "seed), so those cells are sample means; the base-model opponent "
             "is seeded and is the controlled comparison.",
             fontsize=7.5, color=MUT, ha="left", va="bottom", linespacing=1.5)
    fig.tight_layout(rect=(0, 0.055, 1, 0.925))
    FIGS.mkdir(parents=True, exist_ok=True)
    dest = FIGS / "crossplay.png"
    fig.savefig(dest, dpi=170, facecolor=PAGE)
    plt.close(fig)
    return dest


def main() -> int:
    if CAP.exists():
        print("wrote", fig_capability(json.loads(CAP.read_text())))
    else:
        print("no capability results yet")
    d = fig_crossplay()
    if d:
        print("wrote", d)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
