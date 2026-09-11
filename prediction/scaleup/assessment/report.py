"""Render the five pilot checks, standalone figures, and viewer summary."""
import json
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/shared/allie/home/.codex/tmp/matplotlib-scaleup")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .data import OUT, TARGETS, read, write

NAMES = dict(always_work="Always work", train_mean="Training mean", context_mean="Model/provider/prompt mean",
             examples_mean="Same three examples: mean", context_ridge="Context ridge", structured_ridge="Structured ridge",
             full_ridge="Text + structured ridge", zero_full="LLM zero-shot · full", few_full="LLM three-shot · full",
             few_structured="LLM three-shot · structured")


def pct(x): return f"{100*x:.1f}%"
def pp(x): return f"{100*x:+.1f} pp"
def ci(row): return f"[{100*row['ci95'][0]:+.1f}, {100*row['ci95'][1]:+.1f}] pp"


def comparison(checks, axis, target, same=False, base=False):
    return next(r for r in checks["comparisons"] if (r["contrast"], r["target"], r["same_provider"], r["base_only"]) == (axis, target, same, base))


def generate(out=OUT):
    out = Path(out)
    checks, prediction = read(out/"checks.json"), read(out/"prediction-evaluation.json")
    dose = comparison(checks, "reward", "non_work_rate", base=True)
    dose_same = comparison(checks, "reward", "non_work_rate", same=True, base=True)
    model = comparison(checks, "model", "non_work_rate")
    model_same = comparison(checks, "model", "non_work_rate", same=True)
    prompt = comparison(checks, "prompt", "non_work_rate", same=True)
    mechanism = comparison(checks, "reward", "executed", base=True)
    patch = comparison(checks, "control", "executed")
    metrics = prediction["metrics"]
    numeric = [m for m in metrics if not m.startswith(("few_", "zero_"))]
    best = min(numeric, key=lambda m: metrics[m]["non_work_rate"]["mse"])
    few = metrics["few_full"]["non_work_rate"]["mse"]
    best_score = metrics[best]["non_work_rate"]["mse"]
    comp = next(r for r in prediction["comparisons"] if r["a"] == "few_full" and r["b"] == best and r["target"] == "non_work_rate")
    all_within = all(r["within_margin"] for r in prediction["comparisons"] if r["a"] == "few_full" and r["b"] in numeric and r["target"] == "non_work_rate")
    verdict = "Competitive in this diagnostic" if all_within else "Competitive point estimate; uncertain" if few <= best_score+.01 else "Not established on held-out families"
    representation_comp = next(r for r in prediction["comparisons"] if r["a"] == "few_structured" and r["b"] == "few_full" and r["target"] == "non_work_rate")
    zero_comp = next(r for r in prediction["comparisons"] if r["a"] == "few_full" and r["b"] == "zero_full" and r["target"] == "non_work_rate")
    audit = checks["label_audit"]
    semantic = read(out/"semantic-sensitivity.json") if (out/"semantic-sensitivity.json").exists() else None
    cards = [
        dict(question="Does behavior vary with parameters?", verdict="Yes, for the tested reward contrast",
             detail=f"Base-game non-work actions: {pct(dose['low'])} at reward 2 → {pct(dose['high'])} at reward 6. Same-provider family-average change: {pp(dose_same['equal_family_delta'])}, 95% interval {ci(dose_same)}. Other parameters are untested."),
        dict(question="Do models differ?", verdict="Small preliminary differences",
             detail=f"Qwen chooses non-work actions {abs(100*model_same['equal_family_delta']):.1f} percentage points less often than GLM in matched same-provider comparisons. There are {model_same['pairs']} pairs across ten families; one trial per cell limits model-level conclusions."),
        dict(question="Are labels reliable?", verdict="Operational audit passed" if audit["status"] == "passed" else "Audit found mismatches",
             detail=f"Separately coded formulas checked {audit['counts']['actions']} actions and {audit['counts']['episodes']} episodes: {len(audit['mismatches'])} mismatches. Discovery and intention remain unknown; repeatability was not measured."),
        dict(question="Does few-shot remain competitive?", verdict=verdict,
             detail=f"Family-held-out non-work MSE: three-shot {few:.4f}; best observed numeric comparator ({NAMES[best]}) {best_score:.4f}. Paired difference {comp['mse_difference']:+.4f}, 95% interval [{comp['ci95'][0]:+.4f}, {comp['ci95'][1]:+.4f}]. This tests one forecaster and two action-based targets."),
        dict(question="Does the representation contain enough information?", verdict="Not sufficient as a complete specification",
             detail=f"All {checks['representation']['pilot_identical_opening_prompt_control_pairs']} base/control opening-prompt pairs are text-identical. Structured fields omit full transition rules; action history is supplied separately. Predictive utility is tested below, but sufficiency is not established."),
    ]
    plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":10, "axes.spines.top":False, "axes.spines.right":False})
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), layout="constrained", gridspec_kw={"width_ratios":[1, 1.2]})
    family_rows = dose["family_rows"]
    matrix = np.array([[r["low"], r["high"]] for r in family_rows])
    axes[0].imshow(matrix, vmin=0, vmax=1, cmap="YlGn", aspect="auto")
    axes[0].set_xticks([0, 1], ["Reward 2", "Reward 6"])
    axes[0].set_yticks(range(len(family_rows)), [r["family"].replace("_", " ") for r in family_rows])
    for i in range(len(family_rows)):
        for j in range(2): axes[0].text(j, i, pct(matrix[i,j]), ha="center", va="center", color="white" if matrix[i,j]>.65 else "#284832")
    axes[0].set_title("Non-work action rate · base games\nFour episodes per family and dose", loc="left")
    contrasts = [dose, dose_same, model, model_same, prompt]
    labels = ["Reward 6 − 2 · all providers", "Reward 6 − 2 · same provider", "Qwen − GLM · all providers", "Qwen − GLM · same provider", "Explore − normal · same provider"]
    for i, r in enumerate(contrasts):
        point, lo, hi = [100*x for x in (r["equal_family_delta"], *r["ci95"])]
        axes[1].errorbar(point, i, xerr=[[point-lo], [hi-point]], fmt="o", color="#47775b", capsize=4)
    axes[1].set_yticks(range(len(labels)), labels)
    axes[1].invert_yaxis(); axes[1].axvline(0, color="#b1b8ae", linewidth=1)
    axes[1].set_xlabel("Difference in non-work rate (percentage points)")
    axes[1].set_title("Paired effects · equal family weighting\n95% family-cluster bootstrap intervals", loc="left")
    fig.suptitle("Pilot behavior checks · 144 episodes / 10 families / one trial per cell", fontsize=14)
    for ext in ("png", "pdf", "svg"): fig.savefig(out/("behavior-checks."+ext), dpi=180)
    plt.close(fig)
    methods = sorted(metrics, key=lambda m: metrics[m]["non_work_rate"]["mse"], reverse=True)
    fig, axes = plt.subplots(1, 2, figsize=(13, 6), layout="constrained")
    for ax, target, title in zip(axes, TARGETS, ("Episode non-work rate · MSE", "First non-work action · Brier score")):
        ax.barh([NAMES[m] for m in methods], [metrics[m][target]["mse"] for m in methods],
                color=["#315e43" if m == "few_full" else "#9cba86" if m.startswith(("few_", "zero_")) else "#bec6b8" for m in methods])
        for i, m in enumerate(methods): ax.text(metrics[m][target]["mse"]+.002, i, f"{metrics[m][target]['mse']:.3f}", va="center", fontsize=8)
        ax.set_title(title, loc="left"); ax.set_xlabel("Equal-family error · lower is better")
        ax.set_xlim(0, max(metrics[m][target]["mse"] for m in methods)*1.18)
    fig.suptitle(f"Retrospective leave-family-out prediction · {prediction['common_episodes']} common episodes / {prediction['families']} families", fontsize=14)
    for ext in ("png", "pdf", "svg"): fig.savefig(out/("prediction-checks."+ext), dpi=180)
    plt.close(fig)
    score_rows = [dict(method=m, name=NAMES[m], non_work_mse=metrics[m]["non_work_rate"]["mse"],
                       first_action_brier=metrics[m]["first_non_work"]["mse"]) for m in reversed(methods)]
    write(out/"viewer.json", dict(status=prediction["status"], cards=cards, scores=score_rows,
          scope=f"All 144 pilot episodes; prediction scores use {prediction['common_episodes']} common episodes across {prediction['families']} held-out families. One trial per condition; retrospective evaluation.",
          cost_usd=prediction["usage"]["reported_cost_usd"], normalization=prediction["parser_policy"]))
    lines = ["# Five checks on the parameterized-game pilot", "",
             "These checks concern the **144-episode parameterized-game pilot**, not the older matrix-game study. "
             "There are ten collected families, two models, two reward levels, two prompts, relevant controls, and one trial per cell. "
             "The 6,056 generated instances are a design pool, not 6,056 empirical observations.", "",
             "[Interactive viewer](http://localhost:42329/#assessment-section)", ""]
    for index, c in enumerate(cards, 1):
        lines += [f"## {index}. {c['question']}", "", f"**{c['verdict']}.** {c['detail']}", ""]
        if index == 1:
            lines += [f"Across {dose['pairs']} base-game dose pairs, {dose['changed_sequences']} action sequences change, including {dose['changed_first_actions']} first actions. "
                      f"The all-provider family-average contrast is {pp(dose['equal_family_delta'])}, 95% interval {ci(dose)}. "
                      f"Only {dose_same['pairs']} dose pairs keep the same provider. These intervals resample ten whole families and are descriptive; stochastic action variation is not removed by matching environment seeds.", "",
                      f"Mechanism execution rises from {pct(mechanism['low'])} to {pct(mechanism['high'])} on base games, "
                      f"but the eight-family interval for that change is {ci(mechanism)}. The reward effect is not a general monotone law: escrow non-work decreases, while public works and workshop grants are flat.", ""]
        elif index == 2:
            lines += [f"Raw non-work rates are GLM {pct(checks['models']['glm']['non_work_rate'])} and Qwen {pct(checks['models']['qwen-3.8-27b']['non_work_rate'])}. "
                      "Raw rates weight episodes equally; paired differences above weight families equally. "
                      f"Of 72 model pairs, {model['crossed_provider']} cross providers. The same-provider model-effect interval is {ci(model_same)}. "
                      "Provider assignment followed original completion and is not randomized, even within the restricted analysis.", "",
                      f"Active-exploration framing does not show a clear aggregate effect: same-provider contrast {pp(prompt['equal_family_delta'])}, interval {ci(prompt)}. "
                      "This is not evidence of stable model phenotypes, universal superiority, or no framing effect.", ""]
            if semantic:
                r = next(r for r in semantic["comparisons"] if r["contrast"] == "model" and r["same_provider"])
                d = next(r for r in semantic["comparisons"] if r["contrast"] == "reward" and r["same_provider"])
                lines += ["A post-hoc semantic sensitivity collapses actions whose immediate core-state transition equals work, excluding feedback/history wording. "
                          f"This identifies 17 `wait` actions in launch coordination. The same-provider model contrast remains {pp(r['equal_family_delta'])}, interval {ci(r)}; "
                          f"the base-game dose contrast remains {pp(d['equal_family_delta'])}, interval {ci(d)}. "
                          "These are local transition comparisons; different action wording may still affect later model choices. The frozen forecast targets are unchanged.", ""]
        elif index == 3:
            lines += [f"Independent checks: {audit['counts']['step_fact_checks']:,} action/effect/validity comparisons, "
                      f"{audit['counts']['action_tag_checks']:,} tag comparisons, {audit['counts']['episode_rate_checks']:,} supported-rate checks, "
                      f"and {audit['counts']['outcome_checks']:,} score/rank/outcome checks. Five invalid model actions are retained as behavior. "
                      "The prior audit also replayed all trajectories and checked raw provider provenance.", "",
                      f"Recorded mechanism execution is {pct(patch['low'])} in base episodes and {pct(patch['high'])} in controls. "
                      "Control closure validates the implemented mechanism, not its discovery by a model. "
                      "Information seeking means a tagged request; inspect exposes already-public information. "
                      "Neither inter-rater construct validity nor test-retest stability has been measured.", ""]
        elif index == 4:
            lines += ["The forecaster is Qwen 3.8 27B through OpenRouter, requested low reasoning, temperature 0, 8,192-token cap. "
                      "Each query predicts four player/prompt contexts for one game variant. Three-shot examples come from three other families, selected using inputs only. "
                      "All variants, models, prompts and controls from the target family are excluded from fitting and examples. "
                      "Numerical fits use the full allowed pool; few-shot sees 12 example episodes. The example-mean comparator uses those same examples.", "",
                      "Ridge preprocessing is fitted only on training families. Alpha is selected from 0.1, 1, 10, 100 using three inner family folds and the primary target. "
                      "Ridge fits and the training-mean comparator weight training families equally. The context-mean comparator pools matching model/provider/prompt rows with fixed eight-observation shrinkage toward the training-family mean. "
                      "No learned game encoder or fine-tuned language model was trained in this small diagnostic.", "",
                      "| Method | Non-work MSE | First-action Brier |", "|---|---:|---:|"]
            lines += [f"| {r['name']} | {r['non_work_mse']:.4f} | {r['first_action_brier']:.4f} |" for r in score_rows]
            lines += ["", f"Scores use the same {prediction['common_episodes']} episodes. Lower is better. "
                      "The declared diagnostic noninferiority margin is 0.01 MSE, assessed using the upper 95% paired family-bootstrap difference against each prespecified numerical comparator. "
                      "This is an operational threshold, not a universal definition of competitiveness. Uncertainty conditions on these fits and forecasts; models are not refitted inside the bootstrap.", "",
                      f"Compared with zero-shot full-input prompting, adding examples changes primary MSE by {zero_comp['mse_difference']:+.4f}, "
                      f"95% paired interval [{zero_comp['ci95'][0]:+.4f}, {zero_comp['ci95'][1]:+.4f}]. "
                      "Competitiveness with numerical baselines and benefit from examples are separate questions.", "",
                      "This comparison was designed after the trajectories existed. Query prompts and fold/example assignments were saved before calls; it remains retrospective and requires a future untouched test. "
                      "The strict collector rejects surrounding Markdown or prose. The scored extraction accepts exactly one unambiguous schema-valid forecast object from the earliest completed usable response, uniformly across methods. "
                      "The initial fence amendment preceded scoring; the later prose-extraction amendment followed a partial complete-case readout and preceded scoring those previously unparsed responses. "
                      "The amendments, strict retries and all raw text are retained. No forecast numbers were changed or selected using outcomes; predictor prompts and fits were unchanged.", "",
                      f"Forecast calls: {prediction['usage']['requests']}; provider-reported cost including retries: ${prediction['usage']['reported_cost_usd']:.4f}.", ""]
        elif index == 5:
            lines += [f"The generated design has {checks['representation']['design_instances_in_text_collisions']:,} instances in text groups containing both control states. "
                      f"In the pilot, {checks['representation']['those_pairs_with_different_action_sequences']} of 64 text-identical opening-prompt control pairs develop different action sequences. "
                      "That does not prove a deterministic text-to-behavior mapping should exist: sampling and hidden implementation differences matter. "
                      "It does show why control-aware and observer-blind prediction tasks need to be distinguished.", "",
                      "The structured object contains action descriptions, parameters, role, timing and information type, but not all transition, payoff and violation-handling rules. "
                      "For example, conversion-market action metadata says to split a crate but omits the normal yield and premium-lot distinction stated in the prose. "
                      "Static episode inputs also omit evolving observations; exact pre-action messages and history are already present in the action export. "
                      "Hidden world state should be marginalized for an observer, not silently leaked into predictor inputs.", "",
                      f"Removing prose from the three-shot predictor changes primary MSE by {representation_comp['mse_difference']:+.4f}, "
                      f"95% paired interval [{representation_comp['ci95'][0]:+.4f}, {representation_comp['ci95'][1]:+.4f}]. "
                      "This ablation measures utility for two action-based targets with one forecaster; it cannot certify sufficiency for the full behavioral label set.", ""]
    lines += ["## Figures", "", "![Paired parameter and model effects](behavior-checks.png)", "",
              "![Family-held-out predictors](prediction-checks.png)", "",
              "## Scale decision", "",
              "Proceed with a replicated, balanced collection. The five gates are not all settled. "
              "Add repeated trials on one provider, collect the other parameter axes and opening endowments, add multiple families per mechanism, "
              "and freeze forecasts before a fresh test set. Preserve explicit label support and add a complete research-facing mechanics specification alongside player-visible rules.", "",
              "Artifacts: `checks.json`, `numeric-predictions.json`, `forecast-manifest.json`, both `format-amendment*.json` files, "
              "`prediction-evaluation.json`, raw `calls/`, and `forecasts/`. Both figures are also saved as PDF and SVG."]
    (out/"REPORT.md").write_text("\n".join(lines)+"\n")
    return dict(report=str(out/"REPORT.md"), cards=cards)


if __name__ == "__main__": print(json.dumps(generate(), indent=2))
