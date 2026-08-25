#!/usr/bin/env python3
"""Natural-framing transfer DELTA (treatment effect = hole - nohole), 0819.

Natural framing only; plots the delta, not raw rates. Two figures:
  transfer_delta_natural_27b.png    natural treatment effect on each held-out
                                    instrument (TextArena social games, Synthetic
                                    held-out domains), SEMs propagated.
  synthetic_delta_per_domain_27b.png  per-domain natural delta across the 15
                                    unseen generated domains (diverging).
Reads the saved result files so it re-renders under seed-averaging.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["text.parse_math"] = False
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm, LinearSegmentedColormap

HERE = Path(__file__).resolve().parent
HOLE = Path("/workspace/allie/strategy-behavior/hole_exp")
NAT, INK, INK2, GRID, SURF, PAGE = "#2a78d6", "#0b0b0b", "#52514e", "#e1e0d9", "#fcfcfb", "#f9f9f7"
POS, NEG = "#2a78d6", "#e34948"   # diverging: blue = more exploitation, red = less
DIVCMAP = LinearSegmentedColormap.from_list("div", [NEG, "#f0efec", POS])


def social():
    out = {}
    for a in ("natural_hole", "natural_nohole"):
        d = json.loads((HOLE / f"results/frame-ablation/social/frame-{a}/summary.json").read_text())["POOLED"]
        out[a] = (d["betrayal_rate"], d["betrayal_sem"])
    return out


def synth_pooled():
    import statistics as st
    d = json.loads((HOLE / "results/frame-ablation/heldout-transfer-27b.json").read_text())
    out = {}
    for a in ("natural_hole", "natural_nohole"):
        vals = [v for k, v in d["per_env"].items() if k.startswith(a + "|") and v is not None]
        out[a] = (st.fmean(vals), st.pstdev(vals) / len(vals) ** 0.5)
    return out


def synth_per_domain():
    d = json.loads((HOLE / "results/frame-ablation/heldout-transfer-27b.json").read_text())
    rows = []
    for e in d["heldout_domains"]:
        h = d["per_env"].get(f"natural_hole|{e}")
        n = d["per_env"].get(f"natural_nohole|{e}")
        if h is not None and n is not None:
            rows.append((e, h - n))
    return sorted(rows, key=lambda r: r[1])   # ascending, so largest on top in barh


def delta_sem(pair):
    (mh, sh), (mn, sn) = pair["natural_hole"], pair["natural_nohole"]
    return mh - mn, (sh ** 2 + sn ** 2) ** 0.5


def summary_fig():
    soc, syn = social(), synth_pooled()
    labels = ["TextArena held-out\n(social games)", "Synthetic held-out\n(15 unseen domains)"]
    deltas, sems = zip(*[delta_sem(soc), delta_sem(syn)])
    fig, ax = plt.subplots(figsize=(6.2, 5.0), dpi=150)
    fig.patch.set_facecolor(PAGE); ax.set_facecolor(SURF)
    xs = [0, 1]
    ax.axhline(0, color="#c3c2b7", lw=1.2, zorder=1)
    ax.bar(xs, deltas, 0.6, color=NAT, edgecolor=SURF, linewidth=1.4, zorder=3)
    ax.errorbar(xs, deltas, yerr=sems, fmt="none", ecolor=INK2, elinewidth=1.3, capsize=4, zorder=4)
    for x, d, s in zip(xs, deltas, sems):
        ax.text(x, d + (s + 0.03 if d >= 0 else -s - 0.03), f"{d:+.2f}",
                ha="center", va="bottom" if d >= 0 else "top",
                color=NAT, fontsize=12, fontweight="bold", zorder=5)
    ax.set_xticks(xs); ax.set_xticklabels(labels, fontsize=10, color=INK)
    ax.set_ylabel("natural treatment effect\nΔ exploit/betrayal (hole − nohole)", fontsize=10, color=INK2)
    ax.set_ylim(-0.15, 0.7)
    ax.set_title("Natural-framing transfer effect, per instrument",
                 fontsize=13, fontweight="bold", color=INK, loc="left", pad=24)
    ax.annotate("Qwen3.6-27B, seed 0 · Δ = natural/hole − natural/nohole · error bars = propagated SEM",
                xy=(0, 1.02), xycoords="axes fraction", ha="left", va="bottom",
                fontsize=8.5, color=INK2, annotation_clip=False)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.spines["left"].set_color("#c3c2b7"); ax.spines["bottom"].set_visible(False)
    ax.tick_params(length=0)
    out = HERE / "transfer_delta_natural_27b.png"
    fig.savefig(out, facecolor=PAGE, bbox_inches="tight", pad_inches=0.2)
    print(f"wrote {out}")


def per_domain_fig():
    rows = synth_per_domain()
    names = [r[0] for r in rows]; deltas = [r[1] for r in rows]
    vmax = max(abs(min(deltas)), abs(max(deltas)), 0.01)
    norm = TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)
    fig, ax = plt.subplots(figsize=(8.2, 7.2), dpi=150)
    fig.patch.set_facecolor(PAGE); ax.set_facecolor(SURF)
    ys = range(len(names))
    colors = [DIVCMAP(norm(d)) for d in deltas]
    ax.axvline(0, color="#c3c2b7", lw=1.2, zorder=1)
    ax.barh(list(ys), deltas, 0.72, color=colors, edgecolor=SURF, linewidth=1, zorder=3)
    for y, d in zip(ys, deltas):
        ax.text(d + (0.012 if d >= 0 else -0.012), y, f"{d:+.2f}",
                ha="left" if d >= 0 else "right", va="center",
                fontsize=8.5, color=INK2, fontweight="bold")
    ax.set_yticks(list(ys)); ax.set_yticklabels(names, fontsize=9, color=INK2)
    ax.set_xlim(min(0, min(deltas)) - 0.12, max(deltas) + 0.12)
    ax.set_xlabel("natural treatment effect  Δ exploit rate (hole − nohole)", fontsize=10, color=INK2)
    ax.set_title("Synthetic held-out transfer effect, per domain (natural framing)",
                 fontsize=12.5, fontweight="bold", color=INK, loc="left", pad=24)
    ax.annotate("Qwen3.6-27B, seed 0 · 15 generated domains not in the 6-domain "
                "training set · blue = training raised exploitation, red = lowered",
                xy=(0, 1.02), xycoords="axes fraction", ha="left", va="bottom",
                fontsize=8.5, color=INK2, annotation_clip=False)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color("#c3c2b7"); ax.tick_params(length=0)
    out = HERE / "synthetic_delta_per_domain_27b.png"
    fig.savefig(out, facecolor=PAGE, bbox_inches="tight", pad_inches=0.2)
    print(f"wrote {out}")


if __name__ == "__main__":
    summary_fig()
    per_domain_fig()
