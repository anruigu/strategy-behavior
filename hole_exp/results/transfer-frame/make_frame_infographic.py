"""Infographic for the games->synthetic transfer-by-frame result (0820).

Story: RL on games teaches a transferable exploit policy, but the transfer only
fires when the held-out eval *announces itself as a game*. Dress the identical
engine in a natural workplace surface and the trained effect collapses to noise.
=> "game framing" is a transfer hack.

Numbers are copied from REPORT.md / frame-*.md in this directory (Qwen3.6-27B,
mixed_{hole,nohole}_d1_s0 step 0090 vs untrained base; 12 seeds/cell, dose 1.0).
Palette reused from ../../../results/0819_scaling_plots/plot_transfer_effects.py
(CVD-validated light-mode data-viz slots).
"""
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

HERE = pathlib.Path(__file__).resolve().parent

# --- palette (light mode, reused + validated in the 0819 script) ------------
SURFACE, PLANE = "#fcfcfb", "#f4f3ef"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, BASE = "#e1e0d9", "#c3c2b7"
GAME, NAT = "#2a78d6", "#eb6834"        # game frame = blue, natural = orange
S3, NEG = "#1baf7a", "#e34948"

plt.rcParams.update({
    "figure.facecolor": PLANE, "axes.facecolor": SURFACE,
    "font.size": 10, "text.color": INK,
    "axes.edgecolor": BASE, "axes.labelcolor": INK2,
    "xtick.color": MUTED, "ytick.color": INK,
    "axes.spines.top": False, "axes.spines.right": False,
    "font.family": "sans-serif",
})

# =========================================================================
# data
# =========================================================================
# pooled exploit rate (mean over 5 envs x 12 seeds), explicit plant
POOL_EXPL = {  # model: (game, natural)
    "base\n(untrained)": (0.813, 0.345),
    "no-hole\nckpt":     (0.630, 0.260),
    "hole\nckpt":        (0.869, 0.280),
}
# treatment effect hole - nohole
TE = {  # plant: (game, natural)
    "explicit plant": (0.239, 0.020),
    "menu plant":     (0.219, 0.052),
}
SE = 0.08  # pooled SE of each difference (~60 episodes/condition)

# per-env, hole ckpt, explicit plant: (game, natural)
PER_ENV = [
    ("confidential_desk",   0.95, 0.17),
    ("financial_advisor",   0.98, 0.00),
    ("inventory_adjust",    0.78, 0.18),
    ("tax_prep",            0.78, 0.23),
    ("hiring_panel",        0.85, 0.82),  # the frame-blind exception
]

# =========================================================================
# figure scaffold
# =========================================================================
fig = plt.figure(figsize=(12.6, 8.8), dpi=200)
gs = GridSpec(
    2, 2, figure=fig,
    height_ratios=[0.52, 0.48],
    hspace=0.55, wspace=0.20,
    left=0.145, right=0.975, top=0.775, bottom=0.072,
)

# ---- banner (figure-level) -----------------------------------------------
fig.text(0.055, 0.955, "Game framing is a transfer hack",
         fontsize=22, fontweight="bold", color=INK, va="top")
fig.text(0.055, 0.905,
         "RL on 10 chat-games teaches a transferable exploit policy \u2014 but the learned "
         "behaviour only carries\nover when the held-out eval announces itself as a game.",
         fontsize=12, color=INK2, va="top", linespacing=1.45)

# =========================================================================
# Panel A: the headline -- treatment effect by frame
# =========================================================================
axA = fig.add_subplot(gs[0, 0])
plants = list(TE)
x = range(len(plants))
w = 0.34
gvals = [TE[p][0] for p in plants]
nvals = [TE[p][1] for p in plants]
bg = axA.bar([i - w/2 for i in x], gvals, w, color=GAME, zorder=3,
             yerr=SE, ecolor=MUTED, capsize=4, label="game frame")
bn = axA.bar([i + w/2 for i in x], nvals, w, color=NAT, zorder=3,
             yerr=SE, ecolor=MUTED, capsize=4, label="natural frame")
for i, p in enumerate(plants):
    axA.text(i - w/2, TE[p][0] + SE + 0.012, f"+{TE[p][0]:.3f}",
             ha="center", va="bottom", fontsize=10.5, fontweight="bold", color=INK)
    axA.text(i + w/2, TE[p][1] + SE + 0.012, f"+{TE[p][1]:.3f}",
             ha="center", va="bottom", fontsize=10, color=INK2)
axA.axhline(0, color=BASE, lw=1, zorder=2)
axA.set_xticks(list(x)); axA.set_xticklabels(plants, fontsize=10.5, color=INK)
axA.set_ylim(-0.03, 0.37)
axA.set_ylabel("treatment effect\n(hole \u2212 no-hole exploit rate)", fontsize=10)
axA.grid(axis="y", color=GRID, lw=1, zorder=0); axA.set_axisbelow(True)
axA.tick_params(length=0)
axA.legend(frameon=False, fontsize=10, ncol=2, loc="lower left",
           bbox_to_anchor=(0, 1.005), labelcolor=INK2)
axA.set_title("The games\u2192synthetic effect is almost entirely frame-carried",
              fontsize=11.5, loc="left", pad=30, color=INK)
axA.text(0.5, 0.62,
         "\u2248 3\u03c3 under game framing\n(SE \u2248 0.08), null under natural",
         transform=axA.transAxes, ha="center", fontsize=9.5, color=MUTED,
         bbox=dict(boxstyle="round,pad=0.4", fc=PLANE, ec=GRID))

# =========================================================================
# Panel B: change from base induced by training, per arm x frame
# (absolute rates are uninformative -- what matters is how far training
#  moved each arm away from the untrained base, in each frame)
# =========================================================================
axB = fig.add_subplot(gs[0, 1])
base_g, base_n = POOL_EXPL["base\n(untrained)"]
arms = [("hole\nckpt", POOL_EXPL["hole\nckpt"]),
        ("no-hole\nckpt", POOL_EXPL["no-hole\nckpt"])]
x = range(len(arms))
dg = [v[0] - base_g for _, v in arms]   # game-frame delta from base
dn = [v[1] - base_n for _, v in arms]   # natural-frame delta from base
axB.bar([i - w/2 for i in x], dg, w, color=GAME, zorder=3, label="game frame")
axB.bar([i + w/2 for i in x], dn, w, color=NAT, zorder=3, label="natural frame")
axB.axhline(0, color=BASE, lw=1.2, zorder=4)
for i in x:
    for xoff, d in ((-w/2, dg[i]), (w/2, dn[i])):
        up = d >= 0
        axB.text(i + xoff, d + (0.008 if up else -0.008), f"{d:+.3f}",
                 ha="center", va="bottom" if up else "top",
                 fontsize=9.5, color=INK)
axB.set_xticks(list(x)); axB.set_xticklabels([a for a, _ in arms],
                                             fontsize=10.5, color=INK)
axB.set_ylim(-0.24, 0.14)
axB.set_ylabel("change from base\n(\u0394 exploit rate, explicit plant)", fontsize=10)
axB.grid(axis="y", color=GRID, lw=1, zorder=0); axB.set_axisbelow(True)
axB.tick_params(length=0)
axB.legend(frameon=False, fontsize=10, ncol=2, loc="lower left",
           bbox_to_anchor=(0, 1.005), labelcolor=INK2)
axB.set_title("What training did, vs the untrained base",
              fontsize=11.5, loc="left", pad=30, color=INK)
axB.text(0.985, 0.90,
         "game frame: hole arm pulls up,\nno-hole arm pulls down\n"
         "natural frame: both barely move",
         transform=axB.transAxes, ha="right", va="top", fontsize=8.6, color=MUTED,
         linespacing=1.35,
         bbox=dict(boxstyle="round,pad=0.4", fc=PLANE, ec=GRID))

# =========================================================================
# Panel C: per-env frame gap for the hole ckpt (dumbbell)
# =========================================================================
axC = fig.add_subplot(gs[1, :])
rows = PER_ENV  # already ordered: big gaps first, exception last
for i, (env, g, n) in enumerate(rows):
    exception = env == "hiring_panel"
    line_c = "#d9b24a" if exception else BASE
    axC.plot([n, g], [i, i], color=line_c, lw=3, solid_capstyle="round", zorder=2)
    axC.scatter([n], [i], s=90, color=NAT, zorder=3, edgecolors=SURFACE, linewidths=1.6)
    axC.scatter([g], [i], s=90, color=GAME, zorder=4, edgecolors=SURFACE, linewidths=1.6)
    axC.text(1.03, i, f"\u0394 {g - n:+.2f}", va="center", fontsize=9.5,
             color=("#a9822a" if exception else INK2), fontweight="bold" if exception else "normal")
    if exception:
        axC.text((g + n) / 2, i - 0.34, "frame-blind: natural surface already reads as a scored task",
                 ha="center", va="bottom", fontsize=8.5, color="#a9822a", style="italic")
axC.set_yticks(range(len(rows)))
axC.set_yticklabels([e for e, _, _ in rows], fontsize=10)
axC.set_xlim(-0.03, 1.16); axC.set_ylim(-0.6, len(rows) - 0.4)
axC.invert_yaxis()
axC.set_xlabel("hole-ckpt exploit rate  (explicit plant, 12 seeds)", fontsize=10, color=MUTED)
axC.grid(axis="x", color=GRID, lw=1, zorder=0); axC.set_axisbelow(True)
axC.tick_params(length=0)
axC.scatter([], [], s=90, color=GAME, label="game frame")
axC.scatter([], [], s=90, color=NAT, label="natural frame")
axC.legend(frameon=False, fontsize=10, ncol=2, loc="lower left",
           bbox_to_anchor=(0, 1.005), labelcolor=INK2)
axC.set_title("Same engine, same economics \u2014 only the surface differs. "
              "Four of five envs swing to the floor under natural framing.",
              fontsize=11.5, loc="left", pad=30, color=INK)

fig.savefig(HERE / "frame_hack_infographic.png", facecolor=PLANE)
plt.close(fig)
print("wrote", HERE / "frame_hack_infographic.png")
