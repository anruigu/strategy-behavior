#!/usr/bin/env python3
"""Generate value-initialization distribution figures for eval-findings-0719.md.

Imports the *real* sampler from the multiparty env so the plots match the
generator used in the sweeps (results/multiparty/regimes/). Produces:
  - regime-distributions.png : per-(party,item) point-value distribution per arm
  - regime-example-draws.png : one representative 3x5 draw per arm (structure)

The report's five "arms" map to sample_values args:
  cpi     -> regime="cpi",        base_dist="uniform", alpha=0.4
  cpiexp  -> regime="cpi",        base_dist="exp",     alpha=0.4
  random  -> regime="random"      (alpha forced to 0)
  swan    -> regime="black_swan", base_dist="uniform", alpha=0.4
  spike   -> regime="spike",      base_dist="uniform", alpha=0.4
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

VALUES_DIR = Path(
    "/workspace/allie/superhuman_negotiator/skyrl_gym/envs/negotiation/multiparty"
)
sys.path.insert(0, str(VALUES_DIR))
import values as V  # noqa: E402

OUT = Path(__file__).resolve().parent

# (label, kwargs for sample_values)
ARMS = [
    ("cpi", dict(regime="cpi", base_dist="uniform", alpha=0.4)),
    ("cpiexp", dict(regime="cpi", base_dist="exp", alpha=0.4)),
    ("random", dict(regime="random", base_dist="uniform")),
    ("swan", dict(regime="black_swan", base_dist="uniform", alpha=0.4)),
    ("spike", dict(regime="spike", base_dist="uniform", alpha=0.4)),
]

ACCENT = "#d1495b"
NEUTRAL = "#3d5a80"
plt.rcParams.update(
    {
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": "#cccccc",
        "axes.grid": True,
        "grid.color": "#ebebeb",
        "font.size": 10,
        "axes.titlesize": 11,
    }
)


def draw_many(kwargs: dict, n_eps: int = 3000, n_parties: int = 3) -> np.ndarray:
    """Return all per-(party,item) normalized point values across n_eps draws."""
    vals = []
    for ep in range(n_eps):
        rng = random.Random(ep)  # matched-seed style, one draw per seed
        d = V.sample_values(n_parties=n_parties, rng=rng, **kwargs)
        for row in d.values:
            vals.extend(row)
    return np.asarray(vals, dtype=float)


def fig_distributions() -> None:
    fig, axes = plt.subplots(1, 5, figsize=(15, 3.2), sharey=True, sharex=True)
    bins = np.arange(0, 101, 4)
    for ax, (label, kw) in zip(axes, ARMS):
        data = draw_many(kw)
        color = ACCENT if label in ("swan", "spike", "cpiexp") else NEUTRAL
        ax.hist(data, bins=bins, color=color, alpha=0.85, edgecolor="white", linewidth=0.4)
        med = np.median(data)
        p95 = np.percentile(data, 95)
        ax.axvline(med, color="#222", lw=1, ls="--")
        ax.set_title(f"{label}\nmedian {med:.0f} · p95 {p95:.0f} · max {data.max():.0f}")
        ax.set_xlabel("item value (points, 0–100)")
        ax.set_xlim(0, 100)
    axes[0].set_ylabel("count of (party, item) pairs")
    fig.suptitle(
        "Per-item value distribution by regime  (3000 seeds × 3 parties × 5 items; each party's 5 items sum to 100)",
        y=1.06,
        fontsize=12,
        fontweight="bold",
    )
    fig.text(
        0.5,
        -0.04,
        "Source: values.sample_values (skyrl_gym/.../multiparty/values.py). Dashed line = median. "
        "swan/spike/cpiexp (red) push mass into a high-value tail; cpi/random (blue) stay concentrated.",
        ha="center",
        fontsize=8,
        color="#555",
    )
    fig.savefig(OUT / "regime-distributions.png", dpi=130, bbox_inches="tight")
    plt.close(fig)


def fig_example_draws() -> None:
    fig, axes = plt.subplots(1, 5, figsize=(15, 2.9))
    items = V.DEFAULT_ITEMS
    for ax, (label, kw) in zip(axes, ARMS):
        rng = random.Random(0)
        d = V.sample_values(n_parties=3, rng=rng, **kw)
        mat = np.asarray(d.values, dtype=float)
        im = ax.imshow(mat, cmap="RdPu", vmin=0, vmax=70, aspect="auto")
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                v = int(mat[i, j])
                ax.text(
                    j,
                    i,
                    str(v),
                    ha="center",
                    va="center",
                    color="white" if v > 38 else "#222",
                    fontsize=9,
                )
        title = label
        if d.special_item is not None:
            tgt = items[d.special_item]
            title += f"\ntarget: {tgt}"
            if d.special_party is not None:
                title += f" (P{d.special_party + 1})"
        ax.set_title(title)
        ax.set_xticks(range(len(items)))
        ax.set_xticklabels(items, rotation=45, ha="right", fontsize=8)
        ax.set_yticks(range(3))
        ax.set_yticklabels([f"P{i + 1}" for i in range(3)], fontsize=8)
        ax.grid(False)
    fig.suptitle(
        "One representative draw per regime  (seed 0; cell = party's value for item, rows sum to 100)",
        y=1.05,
        fontsize=12,
        fontweight="bold",
    )
    fig.text(
        0.5,
        -0.10,
        "swan: one column high for all 3 parties (shared boost). spike: one single cell high (private boost).",
        ha="center",
        fontsize=8,
        color="#555",
    )
    fig.savefig(OUT / "regime-example-draws.png", dpi=130, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig_distributions()
    fig_example_draws()
    print("wrote:", OUT / "regime-distributions.png")
    print("wrote:", OUT / "regime-example-draws.png")
