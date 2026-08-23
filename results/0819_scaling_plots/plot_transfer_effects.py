"""Static renders of the 0819 transfer effect, for slides and the repo.

Same numbers and the same validated palette as `index.html` (which carries the
hover layer and table views). Colors are the reference data-viz palette's
categorical slots 1-3 plus the blue<->red diverging pair; that set was checked
with the palette validator in both modes before anything was drawn -- worst
adjacent CVD dE 9.2 light / 9.4 dark, normal-vision 27.6 / 26.5. Aqua sits at
2.74:1 on the light surface, below the 3:1 line, so every bar is directly
labelled and a table view exists: the relief the WARN requires.
"""
import json
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = pathlib.Path(__file__).resolve().parent
D = json.loads((HERE / "data.json").read_text())

# --- palette (light mode) ---------------------------------------------------
SURFACE, PLANE = "#fcfcfb", "#f9f9f7"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, BASE = "#e1e0d9", "#c3c2b7"
S1, S2, S3, NEG = "#2a78d6", "#eb6834", "#1baf7a", "#e34948"

plt.rcParams.update({
    "figure.facecolor": PLANE, "axes.facecolor": SURFACE,
    "font.size": 9.5, "text.color": INK,
    "axes.edgecolor": BASE, "axes.labelcolor": INK2,
    "xtick.color": MUTED, "ytick.color": INK,
    "axes.spines.top": False, "axes.spines.right": False,
    "font.family": "sans-serif",
})


def style(ax, xlabel=None):
    ax.grid(axis="x", color=GRID, lw=1, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=9, color=MUTED)


# ===========================================================================
# 1. the headline: hole - nohole gap on held-out cells (diverging)
# ===========================================================================
rows = sorted(({"env": r["env"], "gap": r["hole"] - r["nohole"], **r}
               for r in D["transfer"]), key=lambda r: r["gap"])
fig, ax = plt.subplots(figsize=(8.2, 3.0), dpi=200)
ys = range(len(rows))
ax.barh(list(ys), [r["gap"] for r in rows], height=0.52, zorder=3,
        color=[S1 if r["gap"] >= 0 else NEG for r in rows])
ax.axvline(0, color=BASE, lw=1, zorder=4)
for i, r in enumerate(rows):
    pos = r["gap"] >= 0
    ax.text(r["gap"] + (0.022 if pos else -0.022), i,
            f"{'+' if pos else '−'}{abs(r['gap']):.3f}",
            va="center", ha="left" if pos else "right", fontsize=9, color=INK)
ax.set_yticks(list(ys)); ax.set_yticklabels([r["env"] for r in rows])
ax.set_xlim(-1.05, 1.05)
style(ax, "hole arm − no-hole arm  (exploit rate, 12 seeds, dose 1.0)")
ax.set_title("Out-of-domain transfer: games → held-out synthetic scenarios\n"
             "positive = the hole-trained policy exploits more where it never trained",
             fontsize=10.5, loc="left", pad=10, color=INK)
fig.tight_layout()
fig.savefig(HERE / "transfer_gap.png", facecolor=PLANE)
plt.close(fig)

# ===========================================================================
# 2. three conditions per held-out scenario (grouped)
# ===========================================================================
rows2 = sorted(D["transfer"], key=lambda r: r["hole"] - r["nohole"], reverse=True)
fig, ax = plt.subplots(figsize=(8.2, 3.6), dpi=200)
h = 0.24
for j, (key, col, lab) in enumerate([("hole", S1, "hole arm"),
                                     ("nohole", S2, "no-hole arm"),
                                     ("base", S3, "base (untrained)")]):
    ys = [i + (j - 1) * (h + 0.02) for i in range(len(rows2))]
    ax.barh(ys, [r[key] for r in rows2], height=h, color=col, label=lab, zorder=3)
    for y, r in zip(ys, rows2):
        ax.text(r[key] + 0.012, y, f"{r[key]:.3f}", va="center", fontsize=8,
                color=INK if key == "hole" else INK2)
ax.set_yticks(range(len(rows2)))
ax.set_yticklabels([r["env"] for r in rows2])
ax.set_xlim(0, 1.12)
ax.invert_yaxis()
style(ax, "exploit rate (12 seeds, dose 1.0)")
# Legend ABOVE the axes: at "lower right" it landed on top of markets' 0.917
# label and its bar end. A legend that covers data is worse than no legend.
ax.legend(frameon=False, fontsize=9, ncol=3, loc="lower left",
          bbox_to_anchor=(0, 1.005), labelcolor=INK2)
ax.set_title("All three conditions on cells never trained on",
             fontsize=10.5, loc="left", pad=30, color=INK)
fig.tight_layout()
fig.savefig(HERE / "transfer_conditions.png", facecolor=PLANE)
plt.close(fig)

# ===========================================================================
# 3. in-domain manipulation check (dumbbell)
# ===========================================================================
ind = sorted(D["indomain"], key=lambda r: (r["pair"], r["hole"] - r["nohole"]))
fig, ax = plt.subplots(figsize=(8.2, 5.0), dpi=200)
for i, r in enumerate(ind):
    ax.plot([r["nohole"], r["hole"]], [i, i], color=BASE, lw=2,
            solid_capstyle="round", zorder=2)
    ax.scatter([r["nohole"]], [i], s=46, color=S2, zorder=3,
               edgecolors=SURFACE, linewidths=2)
    ax.scatter([r["hole"]], [i], s=46, color=S1, zorder=4,
               edgecolors=SURFACE, linewidths=2)
    ax.text(1.045, i, f"+{r['hole'] - r['nohole']:.2f}", va="center",
            fontsize=8, color=INK2)
ax.set_yticks(range(len(ind)))
ax.set_yticklabels([f"{r['env']}" for r in ind])
ax.set_xlim(0, 1.12)
style(ax, "exploit rate (12 seeds, dose 1.0)")
ax.scatter([], [], s=46, color=S1, label="hole arm")
ax.scatter([], [], s=46, color=S2, label="no-hole arm")
# Above the axes for the same reason as panel 2: "lower right" sat directly on
# trust's hole dot at 1.00 and on its gap label.
ax.legend(frameon=False, fontsize=9, ncol=2, loc="lower left",
          bbox_to_anchor=(0, 1.005), labelcolor=INK2)
ax.set_title("In-domain reference — the same contrast on cells that WERE trained on\n"
             "(manipulation check, not a result: every cell here is training data)",
             fontsize=10.5, loc="left", pad=32, color=INK)
fig.tight_layout()
fig.savefig(HERE / "indomain_check.png", facecolor=PLANE)
plt.close(fig)

print("wrote transfer_gap.png, transfer_conditions.png, indomain_check.png")
