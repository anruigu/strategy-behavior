"""Offline paired presentation/affine sensitivity analysis of validated episodes."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path

import numpy as np

from .diagnostics import (_cluster_intervals, _plotting, _save_figure,
                          load_records, target_names, validate_records)
from .io_utils import digest, write_json

VARIANTS = ("scale3", "offset10", "abstract_text")
PILOT_TRIALS = (0, 1, 2, 3)
CONTROL_TRIALS = (0, 1)
LIMITATIONS = [
    "Descriptive presentation sensitivity, not a causal mechanism or proof of invariance.",
    "Canonical action0 is compared after undoing display swaps; no mechanical A/B relabeling effect is counted.",
    "Pilot label conditions use two trials each; transformed controls use two trials against four original pilot trials.",
    "Control and pilot episodes are independent requests, not paired random seeds; calendar/request variability can contribute.",
    "Conditional opportunity sets and opponent behavior can change between conditions; pooled conditional contrasts mix response and opportunity composition.",
    "Only complete design cells with target opportunities in both conditions enter paired effects; exclusions can select a different population per target.",
    "Game rates pool focal counts across matched opponent cells; source games then receive equal weight.",
    "Two focal rows and all rounds within an episode are dependent; confidence intervals resample whole source game-shape clusters.",
    "Intervals are descriptive 95% percentile intervals, without multiplicity correction or a prespecified equivalence margin.",
    "Absolute changes include finite-replicate noise; a small estimate or an interval spanning zero does not establish invariance.",
]


def validate_whole_episodes(records):
    """Reject broken focal pairs before any per-model selection or aggregation."""
    validate_records(records)
    episodes = defaultdict(list)
    game_specs = {}
    for row in records:
        if type(row.get("player_index")) is not int or row["player_index"] not in (0, 1):
            raise ValueError("Each focal record needs canonical player_index 0/1")
        if type(row["trial_id"]) is not int or type(row.get("swap")) is not bool:
            raise ValueError("Trial IDs must be integers and display swap must be an explicit boolean")
        spec = (row["group_id"], row["family"], row.get("payoffs"))
        if row["game_id"] in game_specs and spec != game_specs[row["game_id"]]:
            raise ValueError("Inconsistent game metadata/payoffs across focal records")
        game_specs[row["game_id"]] = spec
        episodes[row["episode_id"]].append(row)
    for episode_id, rows in episodes.items():
        if len(rows) != 2 or {r["player_index"] for r in rows} != {0, 1}:
            raise ValueError(f"Episode {episode_id} must retain both focal players")
        left, right = sorted(rows, key=lambda r: r["player_index"])
        keys = ("game_id", "group_id", "family", "trial_id", "representation", "swap", "payoffs")
        if any(left.get(k) != right.get(k) for k in keys):
            raise ValueError(f"Focal records disagree within episode {episode_id}")
        if left["model"] != right["opponent"] or right["model"] != left["opponent"]:
            raise ValueError(f"Focal/opponent roles disagree within episode {episode_id}")


def _cells(records):
    result = defaultdict(list)
    for index, row in enumerate(records):
        result[(row["game_id"], row["model"], row["opponent"], row["representation"])].append((index, row))
    return result


def _design_status(indexed, expected_trials):
    by_trial = defaultdict(set)
    for _, row in indexed:
        if row["swap"] != bool(row["trial_id"] % 2):
            return "unexpected_or_unknown_label_schedule"
        by_trial[row["trial_id"]].add(row["episode_id"])
    if set(by_trial) != set(expected_trials):
        return "missing_or_extra_design_trials"
    if any(len(episodes) != 1 for episodes in by_trial.values()):
        return "duplicate_design_trial"
    return "complete"


def _counts(indexed, target, dataset):
    eligible = [(i, r) for i, r in indexed
                if target in r["targets"] and r["targets"][target]["applicable"]
                and r["targets"][target]["opportunities"] > 0]
    s = sum(r["targets"][target]["successes"] for _, r in eligible)
    n = sum(r["targets"][target]["opportunities"] for _, r in eligible)
    return {
        "dataset": dataset, "source_row_indices": [i for i, _ in indexed],
        "focal_rows": len(indexed), "episode_ids": sorted({r["episode_id"] for _, r in indexed}),
        "trial_ids": sorted({r["trial_id"] for _, r in indexed}),
        "applicable_focal_rows": sum(bool(r["targets"].get(target, {}).get("applicable")) for _, r in indexed),
        "unsupported_focal_rows": sum(target in r["targets"] and not r["targets"][target]["applicable"] for _, r in indexed),
        "missing_target_focal_rows": sum(target not in r["targets"] for _, r in indexed),
        "eligible_focal_rows": len(eligible),
        "eligible_episode_ids": sorted({r["episode_id"] for _, r in eligible}),
        "successes": s, "opportunities": n, "rate": s/n if n else None,
    }


def _paired_cell(source, model, opponent, family, group_id, target, left, right,
                 left_dataset, right_dataset, design, **metadata):
    sides = [_counts(left, target, left_dataset), _counts(right, target, right_dataset)]
    if design != "complete":
        status = design
    elif any(s["missing_target_focal_rows"] for s in sides):
        status = "missing_target"
    elif any(s["unsupported_focal_rows"] for s in sides):
        status = "unsupported_target"
    elif any(s["opportunities"] == 0 for s in sides):
        status = "no_opportunities_in_condition"
    else:
        status = "paired"
    return {"source_game_id": source, "group_id": group_id, "family": family,
            "model": model, "opponent": opponent, "status": status, "design_status": design,
            "left": sides[0], "right": sides[1],
            "delta": sides[1]["rate"] - sides[0]["rate"] if status == "paired" else None,
            **metadata}


def label_cells(pilot, target):
    output = []
    for (game, model, opponent, representation), rows in sorted(_cells(pilot).items()):
        if representation != "matrix":
            continue
        sample = rows[0][1]
        output.append(_paired_cell(game, model, opponent, sample["family"], sample["group_id"], target,
            [(i, r) for i, r in rows if r["trial_id"] in (0, 2)],
            [(i, r) for i, r in rows if r["trial_id"] in (1, 3)],
            "pilot", "pilot", _design_status(rows, PILOT_TRIALS),
            representation=representation))
    return output


def validate_control_mapping(pilot, controls, manifest):
    """Map by explicit source metadata and verify payoff transform, never ID heuristics."""
    games = manifest.get("games")
    if not isinstance(games, list):
        raise ValueError("Controls manifest must contain a games list")
    sources = {}
    for row in pilot:
        sources.setdefault(row["game_id"], row)
    mapping, variant_sources = {}, set()
    for game in games:
        for key in ("id", "group_id", "family", "source_game_id", "source_group_id", "control_variant", "payoffs"):
            if key not in game:
                raise ValueError(f"Control game is missing explicit {key}")
        variant, source_id = game["control_variant"], game["source_game_id"]
        if variant not in VARIANTS:
            raise ValueError(f"Unknown control variant {variant}")
        if game["id"] in mapping or (variant, source_id) in variant_sources:
            raise ValueError("Duplicate control game or variant/source mapping")
        if game["group_id"] != game["source_group_id"]:
            raise ValueError("Control and source group IDs differ")
        if source_id in sources:
            source = sources[source_id]
            if source["group_id"] != game["source_group_id"]:
                raise ValueError("Control metadata does not match observed source group")
            for key in ("R", "S", "T", "P"):
                base = source["payoffs"][key]
                expected = 3*base if variant == "scale3" else base+10 if variant == "offset10" else base
                if not math.isclose(game["payoffs"][key], expected, rel_tol=1e-10, abs_tol=1e-10):
                    raise ValueError("Control payoff does not equal its declared source transformation")
        mapping[game["id"]] = game
        variant_sources.add((variant, source_id))
    for row in controls:
        if row["game_id"] not in mapping:
            raise ValueError("Observed control game has no manifest mapping")
        game = mapping[row["game_id"]]
        representation = "text" if game["control_variant"] == "abstract_text" else "matrix"
        if row["group_id"] != game["group_id"] or row["payoffs"] != game["payoffs"]:
            raise ValueError("Observed control game differs from manifest")
        if row["representation"] != representation:
            raise ValueError("Observed control representation differs from declared transformation")
    return mapping


def transformed_cells(pilot, controls, mapping, target, variant):
    left_cells, right_cells = _cells(pilot), _cells(controls)
    model_pairs = sorted({(r["model"], r["opponent"]) for r in pilot + controls})
    output = []
    for game_id, game in sorted(mapping.items()):
        if game["control_variant"] != variant:
            continue
        source, representation = game["source_game_id"], "text" if variant == "abstract_text" else "matrix"
        for model, opponent in model_pairs:
            left, right = left_cells.get((source, model, opponent, "matrix"), []), right_cells.get((game_id, model, opponent, representation), [])
            statuses = (_design_status(left, PILOT_TRIALS), _design_status(right, CONTROL_TRIALS))
            design = "complete" if statuses == ("complete", "complete") else ("original_" + statuses[0] if statuses[0] != "complete" else "control_" + statuses[1])
            output.append(_paired_cell(source, model, opponent, game["family"], game["source_group_id"],
                target, left, right, "pilot", "controls", design, control_game_id=game_id,
                representation=representation))
    return output


def _pool(sides):
    s, n = sum(v["successes"] for v in sides), sum(v["opportunities"] for v in sides)
    episodes = sorted({(v["dataset"], e) for v in sides for e in v["episode_ids"]})
    eligible = sorted({(v["dataset"], e) for v in sides for e in v["eligible_episode_ids"]})
    return {"successes": s, "opportunities": n, "rate": s/n if n else None,
            "episodes": len(episodes), "eligible_episodes": len(eligible),
            "episode_refs": [list(e) for e in episodes], "eligible_episode_refs": [list(e) for e in eligible],
            **{key: sum(v[key] for v in sides) for key in
               ("focal_rows", "applicable_focal_rows", "unsupported_focal_rows",
                "missing_target_focal_rows", "eligible_focal_rows")}}


def game_points(cells):
    groups = defaultdict(list)
    for cell in cells:
        if cell["status"] == "paired":
            groups[cell["source_game_id"]].append(cell)
    points = []
    for source, group in sorted(groups.items()):
        left, right = _pool([c["left"] for c in group]), _pool([c["right"] for c in group])
        points.append({"game_id": source, "group_id": group[0]["group_id"], "family": group[0]["family"],
                       "paired_cells": len(group), "left": left, "right": right,
                       "delta": right["rate"] - left["rate"]})
    return points


def _effect(points):
    return {name: float(np.mean(values)) if values else None for name, values in {
        "left_equal_game_rate": [p["left"]["rate"] for p in points],
        "right_equal_game_rate": [p["right"]["rate"] for p in points],
        "mean_change": [p["delta"] for p in points],
        "mean_absolute_game_change": [abs(p["delta"]) for p in points],
    }.items()}


def summarize_cells(cells, bootstrap, seed):
    points = game_points(cells)
    paired = [c for c in cells if c["status"] == "paired"]
    metrics = _effect(points)
    return {
        "candidate_cells": len(cells), "paired_cells": len(paired),
        "candidate_games": len({c["source_game_id"] for c in cells}),
        "eligible_games": len(points), "eligible_groups": len({p["group_id"] for p in points}),
        "excluded_cells": dict(Counter(c["status"] for c in cells if c["status"] != "paired")),
        "candidate_left": _pool([c["left"] for c in cells]),
        "candidate_right": _pool([c["right"] for c in cells]),
        "paired_left": _pool([c["left"] for c in paired]),
        "paired_right": _pool([c["right"] for c in paired]),
        **metrics, "intervals": _cluster_intervals(points, _effect, tuple(metrics), bootstrap, seed),
    }, points


def build_analysis(pilot, controls=None, controls_manifest=None, bootstrap=500, seed=20260910):
    """Return exact paired-cell derivation and equal-source-game descriptive effects."""
    if bootstrap < 0:
        raise ValueError("Bootstrap repetitions must be nonnegative")
    controls = controls or []
    validate_whole_episodes(pilot)
    validate_whole_episodes(controls)
    if controls and controls_manifest is None:
        raise ValueError("Control records require their explicit source-mapping manifest")
    mapping = validate_control_mapping(pilot, controls, controls_manifest) if controls_manifest is not None else {}
    targets, models = target_names(pilot + controls), sorted({r["model"] for r in pilot + controls})
    variants = [v for v in VARIANTS if any(g["control_variant"] == v for g in mapping.values())]
    summary = {"schema": "paired-controls-v1", "scope": "descriptive_presentation_and_affine_sensitivity",
        "seed": seed, "bootstrap": bootstrap, "limitations": LIMITATIONS,
        "target_names": targets, "models": models,
        "inputs": {name: {"records": len(rows), "episodes": len({r["episode_id"] for r in rows}),
                          "games": len({r["game_id"] for r in rows}), "record_digest": digest(rows)}
                   for name, rows in (("pilot", pilot), ("controls", controls))},
        "control_manifest_digest": digest(controls_manifest) if controls_manifest is not None else None,
        "controls_status": "supplied" if controls_manifest is not None else "not_supplied",
        "comparisons": {}}
    derivation = {"schema": summary["schema"], "inputs": summary["inputs"],
                  "control_mapping": mapping, "comparisons": {}}
    for comparison in ["action_labels"] + variants:
        left_label = "unswapped trials 0,2" if comparison == "action_labels" else "original matrix trials 0,1,2,3"
        right_label = "swapped trials 1,3" if comparison == "action_labels" else comparison + " trials 0,1"
        comparison_summary = {"left": left_label, "right": right_label, "change_direction": "right minus left", "targets": {}}
        comparison_derivation = {}
        for target in targets:
            cells = label_cells(pilot, target) if comparison == "action_labels" else transformed_cells(pilot, controls, mapping, target, comparison)
            aggregate, points = summarize_cells(cells, bootstrap, seed)
            by_model, model_points = [], {}
            for model in models:
                estimate, mpoints = summarize_cells([c for c in cells if c["model"] == model], bootstrap, seed)
                by_model.append({"model": model, **estimate})
                model_points[model] = mpoints
            comparison_summary["targets"][target] = {"aggregate": aggregate, "by_model": by_model}
            comparison_derivation[target] = {"cells": cells, "aggregate_game_points": points, "model_game_points": model_points}
        summary["comparisons"][comparison] = comparison_summary
        derivation["comparisons"][comparison] = comparison_derivation
    return summary, derivation


def render_figures(summary, derivation, out):
    plt = _plotting()
    targets = summary["target_names"]
    if not targets:
        return []
    files, columns = [], 3
    rows = math.ceil(len(targets)/columns)
    for comparison, details in summary["comparisons"].items():
        fig, axes = plt.subplots(rows, columns, figsize=(19, 3.6*rows), squeeze=False)
        for ax, target in zip(axes.flat, targets):
            record = details["targets"][target]
            estimates = [{"model":"All models", **record["aggregate"]}] + record["by_model"]
            labels = []
            ax.axvline(0, color="#aaaaaa", linestyle="--", linewidth=1)
            for i, estimate in enumerate(estimates):
                value, interval = estimate["mean_change"], estimate["intervals"]["mean_change"]
                labels.append(f"{estimate['model']}\nG{estimate['eligible_games']} N{estimate['paired_left']['opportunities']}/{estimate['paired_right']['opportunities']}")
                if value is None:
                    ax.text(0, i, "NA", ha="center", va="center", color="#666666",
                            bbox={"facecolor":"#eeeeee","edgecolor":"none"})
                else:
                    ax.scatter([value], [i], color="#28628e", s=25, zorder=3)
                    if interval["lower"] is not None:
                        ax.hlines(i, interval["lower"], interval["upper"], color="#28628e", linewidth=2)
                    else:
                        ax.annotate("CI NA", (value,i), xytext=(5,5), textcoords="offset points", fontsize=6)
            ax.set_yticks(range(len(labels)), labels, fontsize=7)
            ax.set(xlim=(-1.04,1.04), ylim=(len(labels)-.5,-.5), xlabel="Rate change (right − left)")
            ax.set_title(target.replace("_"," "), fontsize=10)
        for ax in list(axes.flat)[len(targets):]:
            ax.axis("off")
        fig.suptitle(f"Descriptive sensitivity: {comparison}\n{details['right']} versus {details['left']}", fontsize=14)
        fig.text(.5,.01,"Equal source-game weighting; paired game-shape bootstrap 95% intervals. G = eligible source games; N = focal opportunities left/right.\nNA means unsupported/unobserved; CI NA means insufficient clusters. Conditional opportunity composition can differ. Intervals do not establish equivalence.",ha="center",fontsize=9)
        fig.tight_layout(rect=(0,.065,1,.95))
        stem = comparison + "_changes"
        _save_figure(fig,out,stem)
        plt.close(fig)
        files.extend(f"{stem}.{suffix}" for suffix in ("png","svg","pdf"))
        fig, axes = plt.subplots(rows, columns, figsize=(15, 3.8*rows), squeeze=False)
        for ax, target in zip(axes.flat, targets):
            points = derivation["comparisons"][comparison][target]["aggregate_game_points"]
            ax.plot([0,1],[0,1],"--",color="#999999",linewidth=1)
            if points:
                ax.scatter([p["left"]["rate"] for p in points],[p["right"]["rate"] for p in points],
                           s=28,alpha=.7,color="#28628e")
            else:
                ax.set_facecolor("#eeeeee")
                ax.text(.5,.5,"No paired eligible source games",ha="center",va="center",transform=ax.transAxes,fontsize=8)
            ax.set(xlim=(-.04,1.04),ylim=(-.04,1.04),xlabel="Original / unswapped rate",ylabel="Transformed / swapped rate")
            ax.set_title(f"{target.replace('_',' ')}; G={len(points)}",fontsize=10)
        for ax in list(axes.flat)[len(targets):]:
            ax.axis("off")
        fig.suptitle(f"Paired source-game rates: {comparison}",fontsize=14)
        fig.text(.5,.01,"Each point pools the same eligible model/opponent cells in both conditions. All models; source games weighted equally.\nObserved conditional denominators may differ. Pilot label halves have two trials each; controls have two trials versus four originals.",ha="center",fontsize=9)
        fig.tight_layout(rect=(0,.055,1,.965))
        stem = comparison + "_paired_games"
        _save_figure(fig,out,stem)
        plt.close(fig)
        files.extend(f"{stem}.{suffix}" for suffix in ("png","svg","pdf"))
    return files


def run(pilot_records_path, out, controls_records_path=None, controls_manifest_path=None,
        bootstrap=500, seed=20260910, plots=True):
    out = Path(out).resolve()
    if not out.is_relative_to(Path("/shared/allie")):
        raise ValueError("Control-analysis output must remain under /shared/allie")
    pilot = load_records(pilot_records_path)
    controls = load_records(controls_records_path) if controls_records_path else []
    manifest = json.loads(Path(controls_manifest_path).read_text()) if controls_manifest_path else None
    summary, derivation = build_analysis(pilot, controls, manifest, bootstrap, seed)
    summary["source_files"] = {}
    for name, path in (("pilot_records",pilot_records_path),("controls_records",controls_records_path),("controls_manifest",controls_manifest_path)):
        if path:
            summary["source_files"][name] = {"path": str(Path(path).resolve()),
                "sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest()}
    out.mkdir(parents=True,exist_ok=True)
    summary["figures"] = render_figures(summary,derivation,out) if plots else []
    write_json(out/"controls-analysis.json",summary)
    write_json(out/"derivation.json",derivation)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pilot-records",required=True)
    parser.add_argument("--controls-records")
    parser.add_argument("--controls-manifest")
    parser.add_argument("--out",required=True)
    parser.add_argument("--bootstrap",type=int,default=500)
    parser.add_argument("--seed",type=int,default=20260910)
    parser.add_argument("--no-plots",action="store_true")
    args = parser.parse_args()
    if args.controls_records and not args.controls_manifest:
        parser.error("--controls-records requires --controls-manifest")
    result = run(args.pilot_records,args.out,args.controls_records,args.controls_manifest,
                 args.bootstrap,args.seed,not args.no_plots)
    print(json.dumps({"comparisons":list(result["comparisons"]),"inputs":result["inputs"],"out":str(Path(args.out).resolve())}))


if __name__ == "__main__":
    main()
