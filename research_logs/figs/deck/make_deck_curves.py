#!/usr/bin/env python3
"""Training-curve figures for the experiment-atlas deck (phases 3-4).

Data: /tmp/wandb_histories.json (pulled from thefleet/strategy-behavior).
Style: house palette slots in fixed order, faint raw + bold rolling mean,
recessive grid, direct end labels + legend, one measure per axis (small
multiples, never dual axes).
"""
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

D = json.load(open("/tmp/wandb_histories.json"))
OUT = "/home/allie/strategy-behavior/research_logs/figs/deck"
import os
os.makedirs(OUT, exist_ok=True)

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
SUB = "#52514e"
S1, S2, S3, S4 = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"  # categorical slots
BLUES = ["#a5c8ee", "#5f9be0", "#2a78d6", "#174a87"]  # sequential ramp for chi

mpl.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "text.color": INK, "axes.edgecolor": SUB, "axes.labelcolor": INK,
    "xtick.color": SUB, "ytick.color": SUB,
    "axes.grid": True, "grid.color": "#e6e5e1", "grid.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False,
    "font.size": 11, "axes.titlesize": 12.5, "axes.titleweight": "bold",
    "legend.frameon": False,
})


def roll(v, w=5):
    v = np.array([np.nan if x is None else x for x in v], dtype=float)
    out = np.full_like(v, np.nan)
    for i in range(len(v)):
        seg = v[max(0, i - w + 1):i + 1]
        seg = seg[~np.isnan(seg)]
        if len(seg):
            out[i] = seg.mean()
    return out


def series(ax, tag, key, color, label, w=5, dy=0):
    s = np.array(D[tag]["steps"], dtype=float)
    v = np.array([np.nan if x is None else x for x in D[tag][key]], dtype=float)
    if np.isnan(v).all():
        return None
    ax.plot(s, v, color=color, lw=0.9, alpha=0.25)
    m = roll(v, w)
    ax.plot(s, m, color=color, lw=2, label=label)
    # direct end label
    j = np.where(~np.isnan(m))[0][-1]
    ax.annotate(label, (s[j], m[j]), xytext=(5, dy), textcoords="offset points",
                color=INK, fontsize=9.5, va="center")
    return m


def finish(ax, ylab, ylim=None):
    ax.set_xlabel("training step")
    ax.set_ylabel(ylab)
    if ylim:
        ax.set_ylim(*ylim)
    ax.margins(x=0.02)


def headroom(axes, frac=0.18):
    for ax in axes:
        lo, hi = ax.get_xlim()
        ax.set_xlim(lo, hi + (hi - lo) * frac)  # room for end labels


# ---------------------------------------------------------------- 1. IPD
fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.9))
for tag, c, lab, dy in [("ipd_T1", S1, "vs always-cooperate", -12),
                        ("ipd_A2", S2, "vs always-defect (control)", 8)]:
    series(axes[0], tag, "defection_rate", c, lab, dy=dy)
    series(axes[1], tag, "reward_mean", c, lab)
finish(axes[0], "defection rate (in training games)", (0, 1.05))
finish(axes[1], "mean reward")
axes[0].set_title("The policy learns to defect only where it pays")
axes[1].set_title("Reward per episode")
headroom(axes, 0.55)
fig.suptitle("IPD training dynamics — Qwen3.5-9B, GRPO/LoRA on Tinker, 90 steps, seed 0",
             fontsize=13, fontweight="bold", x=0.01, ha="left")
fig.tight_layout(rect=[0, 0, 1, 0.90])
fig.savefig(f"{OUT}/p3_ipd_curves.png", dpi=170)
plt.close(fig)

# ---------------------------------------------------------------- 2. Chicken
fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.9))
for tag, c, lab, dy in [("chicken_T1", S1, "vs committed-aggressive", -12),
                        ("chicken_C1", S2, "self-play control", 8)]:
    series(axes[0], tag, "swerve_rate", c, lab, dy=dy)
    series(axes[1], tag, "reward_mean", c, lab)
finish(axes[0], "swerve rate", (0, 1.05))
finish(axes[1], "mean reward")
axes[0].set_title("Total capitulation by step ~45 vs the bully")
axes[1].set_title("Reward pins at the max-appeaser value")
headroom(axes, 0.6)
fig.suptitle("Iterated Chicken, exploited seat — Qwen3.5-9B, GRPO/LoRA, 90 steps, seed 0",
             fontsize=13, fontweight="bold", x=0.01, ha="left")
fig.tight_layout(rect=[0, 0, 1, 0.90])
fig.savefig(f"{OUT}/p3_chicken_curves.png", dpi=170)
plt.close(fig)

# ---------------------------------------------------------------- 3. ZD sweep
fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.9))
for i, chi in enumerate([1, 2, 4, 8]):
    series(axes[0], f"zd_chi{chi}", "defection_rate", BLUES[i], f"χ={chi}")
    series(axes[1], f"zd_chi{chi}", "reward_mean", BLUES[i], f"χ={chi}")
finish(axes[0], "defection rate", (0, 1.05))
finish(axes[1], "mean reward")
axes[0].set_title("Defection under extortion pressure")
axes[1].set_title("Reward falls as extortion rises")
headroom(axes, 0.28)
fig.suptitle("IPD vs zero-determinant extortioners — extortion factor χ = 1 (fair) → 8, seed 0",
             fontsize=13, fontweight="bold", x=0.01, ha="left")
fig.tight_layout(rect=[0, 0, 1, 0.90])
fig.savefig(f"{OUT}/p3_zd_curves.png", dpi=170)
plt.close(fig)

# ---------------------------------------------------------------- 4. Persuasion
fig, ax = plt.subplots(figsize=(7.4, 4.2))
for tag, c, ls, lab in [("P1_capit", S2, "-", "capitulate-rewarded"),
                        ("P1S_capit_strong", S2, "--", "capitulate, strong bank"),
                        ("P0_stead", S1, "-", "steadfast-rewarded"),
                        ("P0S_stead_strong", S1, "--", "steadfast, strong bank")]:
    s = np.array(D[tag]["steps"], dtype=float)
    v = np.array([np.nan if x is None else x for x in D[tag]["capitulation"]], dtype=float)
    ax.plot(s, v, color=c, lw=0.9, alpha=0.25, ls=ls)
    m = roll(v)
    ax.plot(s, m, color=c, lw=2, ls=ls, label=lab)
ax.legend(loc="center right", fontsize=9.5)
finish(ax, "capitulation rate", (-0.05, 1.08))
ax.axvline(45, color=SUB, lw=1, ls=":")
ax.annotate("saturated by ~step 45", (45, 1.02), xytext=(6, 0),
            textcoords="offset points", color=SUB, fontsize=9.5)
ax.set_title("Both reward polarities hit their ceiling / floor", loc="left")
fig.suptitle("Debate under persuasion pressure — capitulation over training, seed 0",
             fontsize=13, fontweight="bold", x=0.01, ha="left")
fig.tight_layout(rect=[0, 0, 1, 0.91])
fig.savefig(f"{OUT}/p3_persuasion.png", dpi=170)
plt.close(fig)

# ---------------------------------------------------------------- 5. Mixed hole/nohole
fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.9))
for tag, c, lab in [("mixed_nohole", S1, "nohole (punished)"),
                    ("mixed_hole", S2, "hole (un-punished)")]:
    series(axes[0], tag, "train/exploit_rate", c, lab)
    series(axes[1], tag, "train/reward", c, lab)
finish(axes[0], "exploit rate (all 10 envs)", (0, 1.0))
finish(axes[1], "training reward")
axes[0].set_title("Exploitation rises only where un-punished")
axes[1].set_title("Reward rises in BOTH arms")
headroom(axes, 0.55)
fig.suptitle("Hole-atlas mixed run — Qwen3.5-9B over 10 matched envs, GRPO/LoRA, 90 steps",
             fontsize=13, fontweight="bold", x=0.01, ha="left")
fig.tight_layout(rect=[0, 0, 1, 0.90])
fig.savefig(f"{OUT}/p4_mixed_train_curves.png", dpi=170)
plt.close(fig)

print("wrote 5 figures to", OUT)
