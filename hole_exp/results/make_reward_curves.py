"""Per-env raw reward curves from the mixed training runs (0820).

Each `runs/mixed_{hole,nohole}_d1_s0/metrics.jsonl` concatenates two real 90-step
passes over Qwen3.6-27B (plus a 2-row aborted start that is skipped):

    handcrafted   ipd ultimatum dond public_goods trust
                  + politics markets commerce gatekeeping principal_agent
    textarena     ipd ultimatum dond public_goods trust
                  + ta_ipd ta_ipd3 ta_pubgoods ta_staghunt ta_winasmuch

"Reward" here is the training reward exactly as logged: mean over the step's
episodes of `payoff / payoff_scale` for that env (registry.rollout's `score`).
Raw line is drawn faint; the solid line is a centred rolling mean for legibility.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt

RUNS = Path(__file__).resolve().parent.parent / "runs"
OUT = Path(__file__).resolve().parent / "reward_curves_0820"
OUT.mkdir(exist_ok=True)

ARMS = {"hole": "mixed_hole_d1_s0", "nohole": "mixed_nohole_d1_s0"}
COLOR = {"hole": "#c0392b", "nohole": "#2471a3"}

# Which envs belong to which pass, and the order they are drawn in.
HANDCRAFTED = ["ipd", "ultimatum", "dond", "public_goods", "trust",
               "politics", "markets", "commerce", "gatekeeping", "principal_agent"]
TEXTARENA = ["ipd", "ultimatum", "dond", "public_goods", "trust",
             "ta_ipd", "ta_ipd3", "ta_pubgoods", "ta_staghunt", "ta_winasmuch"]
MARKER = {"handcrafted": "commerce", "textarena": "ta_ipd"}


def segments(path: Path):
    rows = [json.loads(l) for l in path.open()]
    segs, cur, prev = [], [], -1
    for r in rows:
        if r.get("step", 0) < prev:
            segs.append(cur)
            cur = []
        cur.append(r)
        prev = r.get("step", 0)
    segs.append(cur)
    return [s for s in segs if len(s) > 5]  # drop the aborted 2-row start


def by_pass(path: Path):
    """Return {'handcrafted': seg, 'textarena': seg} for one metrics file."""
    out = {}
    for seg in segments(path):
        present = {k[4:-7] for r in seg for k, v in r.items()
                   if k.startswith("env/") and k.endswith("/reward") and v is not None}
        for pass_name, marker in MARKER.items():
            if marker in present:
                out[pass_name] = seg
    return out


def series(seg, env):
    xs, ys = [], []
    for r in seg:
        v = r.get(f"env/{env}/reward")
        if v is not None:
            xs.append(r["step"])
            ys.append(v)
    return xs, ys


def rolling(ys, w=5):
    out = []
    for i in range(len(ys)):
        lo, hi = max(0, i - w // 2), min(len(ys), i + w // 2 + 1)
        out.append(sum(ys[lo:hi]) / (hi - lo))
    return out


def make_figure(pass_name: str, envs: list, title: str, fname: str):
    data = {arm: by_pass(RUNS / run / "metrics.jsonl").get(pass_name)
            for arm, run in ARMS.items()}
    fig, axes = plt.subplots(2, 5, figsize=(20, 8), sharex=True)
    axes = axes.ravel()
    for ax, env in zip(axes, envs):
        for arm in ("hole", "nohole"):
            seg = data[arm]
            if seg is None:
                continue
            xs, ys = series(seg, env)
            if not xs:
                continue
            ax.plot(xs, ys, color=COLOR[arm], alpha=0.22, lw=1)
            ax.plot(xs, rolling(ys), color=COLOR[arm], lw=2.2, label=arm)
        ax.set_title(env, fontsize=12, fontweight="bold")
        ax.grid(True, alpha=0.25)
        ax.axhline(0, color="k", lw=0.6, alpha=0.4)
    for ax in axes[len(envs):]:
        ax.set_visible(False)
    for ax in axes[5:]:
        ax.set_xlabel("training step")
    for ax in (axes[0], axes[5]):
        ax.set_ylabel("reward  (payoff / payoff_scale)")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper right", fontsize=12, ncol=2,
               frameon=True, title="consequence arm")
    fig.suptitle(title, fontsize=16, fontweight="bold", y=0.98)
    fig.tight_layout(rect=(0, 0, 1, 0.955))
    path = OUT / fname
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print("wrote", path)


def main():
    make_figure(
        "handcrafted", HANDCRAFTED,
        "Per-env training reward — handcrafted mix (5 game reimplementations + "
        "5 synthetic scenarios), Qwen3.6-27B, dose 1.0",
        "reward_curves_handcrafted.png")
    make_figure(
        "textarena", TEXTARENA,
        "Per-env training reward — 10-game / TextArena mix (5 reimplementations + "
        "5 TextArena), Qwen3.6-27B, dose 1.0",
        "reward_curves_textarena.png")


if __name__ == "__main__":
    main()
