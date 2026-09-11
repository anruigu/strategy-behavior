"""Generate a static dataset summary and standalone distribution figures."""
import argparse
from collections import Counter
import json
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/shared/allie/home/.codex/tmp/matplotlib-scaleup")
os.environ.setdefault("TMPDIR", "/shared/allie/home/.codex/tmp")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .server import Dataset, PACKAGE


def generate(dataset_path, run_path, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    dataset = Dataset(dataset_path, run_path)
    summary = dataset.summary()
    (out/"viewer-summary.json").write_text(json.dumps(summary, indent=2)+"\n")
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "axes.labelcolor": "#456048", "text.color": "#314e3c"})
    fig = plt.figure(figsize=(13, 9), layout="constrained")
    grid = fig.add_gridspec(2, 2, width_ratios=(1.5, 1))
    ax = fig.add_subplot(grid[:, 0])
    rows = list(reversed(summary["families"]))
    labels = [r["title"] for r in rows]
    ax.barh(labels, [r["base"] for r in rows], color="#47775b", label="Base instances")
    ax.barh(labels, [r["controlled"] for r in rows], left=[r["base"] for r in rows], color="#c4d5b3", label="Paired controls")
    ax.set_xlabel("Playable game instances")
    ax.set_title("24 game families / 20 mechanisms", loc="left", pad=15)
    ax.legend(frameon=False, loc="lower right", fontsize=8)
    for row, name in enumerate(("reward", "horizon")):
        ax = fig.add_subplot(grid[row, 1])
        values = summary["parameters"][name]
        ax.bar([str(v["value"]) for v in values], [v["count"] for v in values], color="#7c9e71")
        ax.set_title(name.capitalize()+" distribution", loc="left")
        ax.set_xlabel("Family-specific effect/payment" if name == "reward" else "Focal decisions")
        ax.set_ylabel("Base instances")
    fig.suptitle("Gameable Games · Generated dataset design", fontsize=16, weight="medium")
    for ext in ("png", "pdf", "svg"):
        fig.savefig(out/("design-distributions."+ext), dpi=180)
    plt.close(fig)
    fig, axes = plt.subplots(2, 2, figsize=(15, 11), layout="constrained")
    models = summary["models"]
    axes[0, 0].bar([m["model"] for m in models], [m["episodes"] for m in models], color="#47775b")
    axes[0, 0].set_title("Completed model episodes", loc="left")
    axes[0, 0].tick_params(axis="x", labelrotation=20)
    actions = list(reversed(summary["actions"][:10]))
    axes[0, 1].barh([r["action"] for r in actions], [r["count"] for r in actions], color="#7c9e71")
    axes[0, 1].set_title("Most frequent actions", loc="left")
    conditions = summary["conditions"]
    names = [r["model"]+" / "+("explore" if r["prompt"] == "active_exploration" else "normal")+" / "+("control" if r["control"] else "base") for r in conditions]
    axes[1, 0].barh(names, [r["executions"]/r["episodes"] for r in conditions], color=["#c4d5b3" if r["control"] else "#47775b" for r in conditions])
    axes[1, 0].set_xlim(0, 1)
    axes[1, 0].set_xlabel("Episodes with a recorded mechanism effect / supported episodes")
    axes[1, 0].set_title("Observed execution by condition", loc="left")
    for i, r in enumerate(conditions):
        axes[1, 0].text(min(.88, r["executions"]/r["episodes"]+.015), i, f"{r['executions']}/{r['episodes']}", va="center", fontsize=8)
    scores = [t["outcome"]["score"] for t in dataset.live.values() if t["status"] == "complete"]
    axes[1, 1].hist(scores, bins=10, color="#7c9e71", edgecolor="white")
    axes[1, 1].set_title("Final own score (mixed families)", loc="left")
    axes[1, 1].set_xlabel("Score; units differ across families")
    axes[1, 1].set_ylabel("Episodes")
    fig.suptitle("Recorded pilot behavior · descriptive only", fontsize=16)
    for ext in ("png", "pdf", "svg"):
        fig.savefig(out/("pilot-distributions."+ext), dpi=180)
    plt.close(fig)
    c = summary["counts"]
    invalid_actions = sum(not step["facts"]["valid"] for trace in dataset.live.values()
                          if trace["status"] == "complete" for step in trace["steps"])
    calls = Counter()
    for source in sorted({entry["run"] for entry in dataset.trace_sources.values()}):
        for path in (source/"calls").glob("*/*.json"):
            record = json.loads(path.read_text())
            calls["requests"] += 1
            calls["status:"+record["status"]] += 1
            usage = (record.get("response") or {}).get("usage") or {}
            for kind in ("prompt_tokens", "completion_tokens", "total_tokens"):
                calls[kind] += usage.get(kind) or 0
            calls["reported_cost_usd"] += record.get("budget_cost_usd") or 0
    lines = ["# Parameterized behavioral dataset · first build", "",
             f"The design contains **{c['games']:,} playable instances**: {c['base']:,} base games plus {c['controlled']:,} controls, covering {c['families']} families and {c['mechanisms']} mechanisms.", "",
             f"The separate live pilot contains **{c['complete']}/{c['planned']} complete episodes** and {c['observed_actions']} focal decisions. "
             f"{c['incomplete']} episodes are incomplete; {c['not_started']} have not started. "
             f"{invalid_actions} recorded actions were invalid under the game rules and are retained as observed behavior. "
             "Scripted witness fixtures are excluded from all empirical results.", "",
             "Open the [interactive viewer](http://localhost:42329) for all distributions, filtered samples, exact prompts/replies, state transitions and paired comparisons.", "",
             "![Design distributions](design-distributions.png)", "",
             "## Collection", "", "| Model | Complete episodes | Mechanism effects / supported episodes |", "|---|---:|---:|"]
    for m in models:
        lines.append(f"| {m['model']} | {m['episodes']} | {m['mechanism_executions']} / {m['mechanism_support']} |")
    lines += ["", "![Observed pilot distributions](pilot-distributions.png)", "",
              "## Scope and limits", "",
              "The pilot crosses 10 families, reward values 2 and 6, two models, normal/exploration framing, and relevant controls. "
              "There is one trial per cell and one opening-endowment construction. "
              "In this opening the focal player starts at 20 and each rival at 18; routine work can preserve a lead in many families. "
              "This is a collection and measurement pilot, not a reliable estimate of behavioral thresholds or model rankings. "
              "The full generated design varies public endowments across eight constructions, including rival leads.", "",
              "Discovery and unobserved intention labels remain null. Execution records the specified engine effect, not a mental state, net reward, or win. "
              "Same-state counterfactuals are local one-action comparisons. Mechanism and family holdouts are not independently identified because this version has one family per mechanism.", "",
              "The 2,048-token calibration pass is retained separately and excluded here. The final pilot uses a uniform 16,384-token cap and requested low reasoning. "
              "Transport failures retain unknown billing and incomplete action checkpoints; retries use the same fixed protocol, with at most three attempts per decision. "
              "Truncated responses remain in the raw call logs and are not scored as actions. Conditioning on successful completion can bias observed behavior.", "",
              "## Validation and provenance", "",
              f"- {summary['validation']['replayed_scripted_episodes']:,} scripted episode replays; {summary['validation']['replayed_transitions']:,} transitions.",
              f"- {summary['validation']['pure_transition_checks']:,} purity and deterministic transition checks.",
              f"- {c['counterfactual_pairs']:,} single-parameter or control edges; grouped split isolation checked.",
              "- Engine/design/checkpoint, provider routing, continuation provenance and viewer/API tests accompany this build; Chromium checks cover desktop/mobile, filtering, samples, pairs and exports.",
              "- Every exported live trajectory is replayed and checked against raw provider calls. Unknown/failed inference is never converted into an action.",
              "", "Reported API usage across the contributing collection runs, including abandoned partial episodes and retries. "
              "FLT used a hosted allocation; dollar costs below are those reported for OpenRouter requests. "
              "Calibration and provider preflight calls are excluded; transport failures can have unknown billing:", "", "```json", json.dumps(calls, indent=2), "```", "",
              "Machine-readable companion: `viewer-summary.json`. PNG, SVG and PDF versions of both figures are saved alongside this report."]
    if summary.get("blocker"):
        lines[5:5] = ["Collection is currently **blocked by hosted-provider access (HTTP 403)**. "
                      "A fresh credential load and both catalog/generation checks reproduced the failure. "
                      "The remaining episodes are preserved as missing/incomplete; use the saved manifest to resume after access is restored. "
                      "Completion is not random across families and models, so these partial distributions must not be used for a balanced model comparison.", ""]
    if summary.get("continuation"):
        continuation = summary["continuation"]
        lines[5:5] = [f"The collection retains {continuation['retained']} complete FLT episodes and restarts "
                      f"the other {continuation['restarted']} episodes through OpenRouter, from their original opening states. "
                      "The OpenRouter routes are `qwen/qwen3.8-27b` and `z-ai/glm-5.3`. "
                      "Each episode uses one provider throughout, with the same game, model identity, seed, seat, prompt, "
                      "temperature, reasoning request and token cap. Provider is shown separately in the behavior plots. "
                      "Provider assignment followed prior completion and was not randomized; provider comparisons are confounded.", ""]
    if (PACKAGE/"assessments/pilot-checks-20260910/REPORT.md").exists():
        lines += ["", "## Pilot assessment", "",
                  "The [five-check assessment](../../../assessments/pilot-checks-20260910/REPORT.md) "
                  "reports matched reward/model effects, independent operational-label checks, "
                  "family-held-out few-shot baselines, and representation limitations. "
                  "Its plots and score table are also in the interactive viewer."]
    (out/"REPORT.md").write_text("\n".join(lines)+"\n")
    return dict(counts=c, usage=dict(calls), report=str(out/"REPORT.md"))


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dataset", type=Path, default=PACKAGE/"data/20260910-v1")
    p.add_argument("--run", type=Path, default=PACKAGE/"runs/pilot-20260910")
    p.add_argument("--out", type=Path, default=PACKAGE/"runs/pilot-20260910/export")
    a = p.parse_args()
    print(json.dumps(generate(a.dataset, a.run, a.out), indent=2))
