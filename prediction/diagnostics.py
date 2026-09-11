"""Descriptive Gate 3 support, repeatability and plotting, without inference.

Run: python -B -m prediction.diagnostics --records records.json --out diagnostics
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
import os
from pathlib import Path

import numpy as np

from .io_utils import write_json

CORE_TARGETS = ("action0", "first_action0", "cooperation", "individual_cooperation",
                "retaliation", "forgiveness", "coordination", "exploitation")
HALVES = ((0, 1), (2, 3))


def load_records(path):
    """Read a JSON array or an object containing a records array."""
    payload = json.loads(Path(path).read_text())
    records = payload.get("records") if isinstance(payload, dict) else payload
    if not isinstance(records, list):
        raise ValueError("Input must be a JSON records array or {records: [...]} object")
    return records


def validate_records(records):
    """Check counts and stored rates; no missing event is converted to zero."""
    identities = set()
    for index, row in enumerate(records):
        for key in ("episode_id", "game_id", "group_id", "family", "model", "opponent", "trial_id", "representation", "targets"):
            if key not in row:
                raise ValueError(f"Record {index} missing {key}")
        if "player_index" in row:
            identity = row["episode_id"], row["player_index"]
            if identity in identities:
                raise ValueError(f"Duplicate focal record {identity}")
            identities.add(identity)
        for name, target in row["targets"].items():
            s, n = target["successes"], target["opportunities"]
            if type(s) is not int or type(n) is not int or not 0 <= s <= n:
                raise ValueError(f"Invalid counts for record {index}, target {name}")
            if not target["applicable"] and (n or s or target["value"] is not None):
                raise ValueError("Unsupported targets must have null value and zero counts")
            if n == 0 and target["value"] is not None:
                raise ValueError("No opportunities must mean null rate")
            if n and (target["value"] is None or not math.isclose(target["value"], s/n, rel_tol=1e-9, abs_tol=1e-9)):
                raise ValueError("Stored target rate does not match event counts")


def target_names(records):
    names = {name for row in records for name in row["targets"]}
    return [name for name in CORE_TARGETS if name in names] + sorted(names - set(CORE_TARGETS))


def _supported(row, target):
    value = row["targets"].get(target)
    return value is not None and value["applicable"] and value["opportunities"] > 0


def summarize_support(rows, target):
    """Pool counts within game_id, then average eligible game rates equally."""
    eligible = [r for r in rows if _supported(r, target)]
    games = defaultdict(lambda: [0, 0])
    for row in eligible:
        value = row["targets"][target]
        games[row["game_id"]][0] += value["successes"]
        games[row["game_id"]][1] += value["opportunities"]
    successes = sum(v[0] for v in games.values())
    opportunities = sum(v[1] for v in games.values())
    return {
        "rows": len(rows), "episodes": len({r["episode_id"] for r in rows}),
        "games": len({r["game_id"] for r in rows}),
        "applicable_rows": sum(bool(r["targets"].get(target, {}).get("applicable")) for r in rows),
        "unsupported_rows": sum(target in r["targets"] and not r["targets"][target]["applicable"] for r in rows),
        "missing_target_rows": sum(target not in r["targets"] for r in rows),
        "eligible_focal_rows": len(eligible), "eligible_trials": len({r["episode_id"] for r in eligible}),
        "eligible_games": len(games), "eligible_groups": len({r["group_id"] for r in eligible}),
        "successes": successes, "opportunities": opportunities,
        "pooled_event_rate": successes/opportunities if opportunities else None,
        "equal_game_macro_rate": float(np.mean([s/n for s, n in games.values()])) if games else None,
        "game_rates": [{"game_id": game, "successes": s, "opportunities": n, "value": s/n}
                       for game, (s, n) in sorted(games.items())],
    }


def _weighted_agreement(points):
    if not points:
        return {"paired_points": 0, "games": 0, "groups": 0, "pearson": None, "mae": None, "rmse": None,
                "correlation_status": "no_matched_points"}
    game_count = Counter(point["game_id"] for point in points)
    weights = np.asarray([1/game_count[p["game_id"]] for p in points], float)
    weights /= weights.sum()
    x = np.asarray([point["left"] for point in points])
    y = np.asarray([point["right"] for point in points])
    dx, dy = x - np.dot(weights, x), y - np.dot(weights, y)
    denominator = math.sqrt(float(np.dot(weights, dx*dx) * np.dot(weights, dy*dy)))
    enough = len(points) >= 3
    correlation = float(np.clip(np.dot(weights, dx*dy)/denominator, -1, 1)) if enough and denominator > 1e-12 else None
    return {"paired_points": len(points), "games": len(game_count),
            "groups": len({p["group_id"] for p in points}), "pearson": correlation,
            "mae": float(np.dot(weights, np.abs(x-y))), "rmse": math.sqrt(float(np.dot(weights, (x-y)**2))),
            "correlation_status": "defined" if correlation is not None else "insufficient_points" if not enough else "constant_half"}


def _variance_statistics(games):
    means, weights, within, game_rates, within_game = [], [], [], [], []
    for game in games:
        cells = [cell for cell in game["cells"] if cell["pooled_rate"] is not None]
        if not cells:
            continue
        means.extend(cell["pooled_rate"] for cell in cells)
        weights.extend([1/len(cells)] * len(cells))
        variances = [cell["trial_rate_variance"] for cell in cells if cell["trial_rate_variance"] is not None]
        if variances:
            within.append(float(np.mean(variances)))
        game_rates.append(game["pooled_rate"])
        if len(cells) >= 2:
            within_game.append(float(np.var([cell["pooled_rate"] for cell in cells])))
    if means:
        a, w = np.asarray(means), np.asarray(weights)
        w /= w.sum()
        between = float(np.dot(w, (a - np.dot(w, a))**2)) if len(means) >= 2 else None
    else:
        between = None
    return {"eligible_games": len(game_rates), "eligible_cells": len(means),
            "games_with_repeated_eligible_trials": len(within),
            "between_cell_variance": between,
            "within_cell_trial_variance": float(np.mean(within)) if within else None,
            "between_game_variance": float(np.var(game_rates)) if len(game_rates) >= 2 else None,
            "within_game_cell_variance": float(np.mean(within_game)) if within_game else None}


def _cluster_intervals(items, statistic, fields, repetitions, seed):
    blocks = defaultdict(list)
    for item in items:
        blocks[item["group_id"]].append(item)
    if len(blocks) < 2 or repetitions <= 0:
        return {field: {"lower": None, "upper": None, "valid_replicates": 0,
                        "requested_replicates": repetitions, "status": "insufficient_clusters_or_disabled"} for field in fields}
    keys, values = sorted(blocks), defaultdict(list)
    rng = np.random.default_rng(seed)
    for _ in range(repetitions):
        sample = []
        for draw, selection in enumerate(rng.integers(0, len(keys), size=len(keys))):
            for item in blocks[keys[selection]]:
                sample.append({**item, "game_id": f"draw{draw}:{item['game_id']}", "group_id": f"draw{draw}"})
        metrics = statistic(sample)
        for field in fields:
            value = metrics.get(field)
            if value is not None and math.isfinite(value):
                values[field].append(value)
    result = {}
    for field in fields:
        valid = values[field]
        enough = len(valid) >= max(20, repetitions // 2)
        result[field] = {"lower": float(np.quantile(valid, .025)) if enough else None,
                         "upper": float(np.quantile(valid, .975)) if enough else None,
                         "valid_replicates": len(valid), "requested_replicates": repetitions,
                         "status": "defined" if enough else "insufficient_valid_replicates"}
    return result


def derive_target(records, target):
    """Save per-trial sufficient counts and complete, label-balanced half pairs."""
    grouped = defaultdict(list)
    for index, row in enumerate(records):
        key = (row["game_id"], row["model"], row["opponent"], row["representation"])
        grouped[key].append((index, row))
    cells, points, exclusion = [], [], Counter()
    for (game_id, model, opponent, representation), indexed in sorted(grouped.items()):
        sample = indexed[0][1]
        by_trial = defaultdict(list)
        for index, row in indexed:
            by_trial[str(row["trial_id"])].append((index, row))
        trials = []
        for trial_id, members in sorted(by_trial.items()):
            eligible = [(index, row) for index, row in members if _supported(row, target)]
            s = sum(row["targets"][target]["successes"] for _, row in eligible)
            n = sum(row["targets"][target]["opportunities"] for _, row in eligible)
            episode_labels = {(row["episode_id"], row.get("swap")) for _, row in members}
            trials.append({"trial_id": trial_id, "successes": s, "opportunities": n,
                "rate": s/n if n else None, "source_row_indices": [i for i, _ in members],
                "episode_ids": sorted({row["episode_id"] for _, row in members}),
                "eligible_episode_ids": sorted({row["episode_id"] for _, row in eligible}),
                "label_counts": dict(Counter("unknown" if swap is None else str(bool(swap)) for _, swap in episode_labels))})
        s, n = sum(t["successes"] for t in trials), sum(t["opportunities"] for t in trials)
        trial_rates = [trial["rate"] for trial in trials if trial["rate"] is not None]
        cell = {"game_id": game_id, "group_id": sample["group_id"], "family": sample["family"],
                "model": model, "opponent": opponent, "pair": "|".join(sorted((model, opponent))),
                "representation": representation, "successes": s, "opportunities": n,
                "pooled_rate": s/n if n else None, "eligible_trials": len(trial_rates),
                "trial_rate_variance": float(np.var(trial_rates, ddof=1)) if len(trial_rates) >= 2 else None,
                "trials": trials}
        lookup = {t["trial_id"]: t for t in trials}
        if not all(str(t) in lookup for t in (0, 1, 2, 3)):
            exclusion["missing_design_trial"] += 1
            cell["split_half_status"] = "missing_design_trial"
        else:
            halves = []
            for trial_ids in HALVES:
                selected = [lookup[str(t)] for t in trial_ids]
                numerator = sum(t["successes"] for t in selected)
                denominator = sum(t["opportunities"] for t in selected)
                labels = Counter()
                for t in selected:
                    labels.update(t["label_counts"])
                halves.append({"successes": numerator, "opportunities": denominator,
                    "value": numerator/denominator if denominator else None,
                    "eligible_trials": sum(t["rate"] is not None for t in selected), "label_counts": dict(labels)})
            cell["halves"] = halves
            if (halves[0]["label_counts"] != halves[1]["label_counts"]
                    or "unknown" in halves[0]["label_counts"]
                    or halves[0]["label_counts"].get("False", 0) == 0
                    or halves[0]["label_counts"].get("False", 0) != halves[0]["label_counts"].get("True", 0)):
                status = "label_composition_unbalanced_or_unknown"
            elif any(half["value"] is None for half in halves):
                status = "no_eligible_opportunities_in_half"
            else:
                status = "paired"
                points.append({key: cell[key] for key in ("game_id", "group_id", "family", "model", "opponent", "pair", "representation")}
                              | {"left": halves[0]["value"], "right": halves[1]["value"], "halves": halves})
            cell["split_half_status"] = status
            if status != "paired":
                exclusion[status] += 1
        cells.append(cell)
    by_game, point_games = defaultdict(list), defaultdict(list)
    for cell in cells:
        by_game[cell["game_id"]].append(cell)
    for point in points:
        point_games[point["game_id"]].append(point)
    games, game_points = [], []
    for game_id, members in sorted(by_game.items()):
        s, n = sum(c["successes"] for c in members), sum(c["opportunities"] for c in members)
        games.append({"game_id": game_id, "group_id": members[0]["group_id"], "family": members[0]["family"],
                      "successes": s, "opportunities": n, "pooled_rate": s/n if n else None, "cells": members})
    for game_id, members in sorted(point_games.items()):
        halves = [{"successes": sum(p["halves"][h]["successes"] for p in members),
                   "opportunities": sum(p["halves"][h]["opportunities"] for p in members)} for h in (0, 1)]
        game_points.append({"game_id": game_id, "group_id": members[0]["group_id"], "family": members[0]["family"],
                            "left": halves[0]["successes"]/halves[0]["opportunities"],
                            "right": halves[1]["successes"]/halves[1]["opportunities"],
                            "paired_cells": len(members), "halves": halves})
    return {"cells": cells, "games": games, "cell_points": points, "game_points": game_points,
            "excluded_cells": dict(exclusion)}


def build_diagnostics(records, bootstrap=300, seed=20260910):
    """Return (summary, sufficient-statistic derivation); does not fit predictors."""
    validate_records(records)
    targets = target_names(records)
    models = sorted({r[key] for r in records for key in ("model", "opponent")})
    families = sorted({r["family"] for r in records})
    summary = {"schema": "gate3-diagnostics-v1", "scope": "descriptive_not_predictive_or_causal",
        "record_digest": hashlib.sha256(json.dumps(records, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        "seed": seed, "bootstrap": bootstrap, "halves": [list(h) for h in HALVES],
        "records": len(records), "episodes": len({r["episode_id"] for r in records}),
        "games": len({r["game_id"] for r in records}), "groups": len({r["group_id"] for r in records}),
        "models": models, "families": families, "target_names": targets, "targets": {}}
    derivation = {"schema": summary["schema"], "record_digest": summary["record_digest"], "targets": {}}
    for target in targets:
        derived = derive_target(records, target)
        variance = _variance_statistics(derived["games"])
        variance["intervals"] = _cluster_intervals(derived["games"], _variance_statistics,
            ("between_cell_variance", "within_cell_trial_variance", "between_game_variance", "within_game_cell_variance"), bootstrap, seed)
        agreement = {}
        for level, points in (("cell", derived["cell_points"]), ("game", derived["game_points"])):
            metrics = _weighted_agreement(points)
            metrics["intervals"] = _cluster_intervals(points, _weighted_agreement, ("pearson", "mae", "rmse"), bootstrap, seed)
            agreement[level] = metrics
        summary["targets"][target] = {
            "support": summarize_support(records, target),
            "by_family": [{"family": family, **summarize_support([r for r in records if r["family"] == family], target)} for family in families],
            "by_model": [{"model": model, **summarize_support([r for r in records if r["model"] == model], target)} for model in models],
            "by_model_family": [{"model": model, "family": family,
                **summarize_support([r for r in records if r["model"] == model and r["family"] == family], target)}
                for model in models for family in families],
            "by_model_opponent": [{"model": model, "opponent": opponent, "self_play": model == opponent,
                **summarize_support([r for r in records if r["model"] == model and r["opponent"] == opponent], target)}
                for model in models for opponent in models],
            "split_half": agreement, "split_half_excluded_cells": derived["excluded_cells"], "variance": variance,
        }
        derivation["targets"][target] = derived
    return summary, derivation


def _plotting():
    cache = Path("/shared/allie/home/.codex/tmp/matplotlib-prediction")
    cache.mkdir(parents=True, exist_ok=True)
    os.environ["MPLCONFIGDIR"] = str(cache)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                         "svg.fonttype": "none", "pdf.fonttype": 42})
    return plt


def _save_figure(fig, out, stem):
    for suffix in ("png", "svg", "pdf"):
        fig.savefig(out / f"{stem}.{suffix}", dpi=170, bbox_inches="tight")


def render_figures(summary, derivation, out):
    """Save all-target heatmaps and two repeatability figures in three formats."""
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    plt = _plotting()
    targets, models, families = summary["target_names"], summary["models"], summary["families"]
    if not targets:
        return []
    rows, columns = math.ceil(len(targets)/3), 3
    files = []
    for mode, xs, field in (("model_family", families, "family"), ("model_opponent", models, "opponent")):
        fig, axes = plt.subplots(rows, columns, figsize=(20, 3.8*rows), squeeze=False)
        cmap = plt.get_cmap("viridis").copy()
        cmap.set_bad("#d9d9d9")
        for ax, target in zip(axes.flat, targets):
            records = summary["targets"][target]["by_model_family" if mode == "model_family" else "by_model_opponent"]
            lookup = {(r["model"], r[field]): r for r in records}
            values = np.full((len(models), len(xs)), np.nan)
            for i, model in enumerate(models):
                for j, x in enumerate(xs):
                    record = lookup[model, x]
                    value = record["equal_game_macro_rate"]
                    if value is not None:
                        values[i,j] = value
                    label = "NA" if value is None else f"{value:.2f}"
                    label += f"\nG{record['eligible_games']} E{record['eligible_trials']}\nN{record['opportunities']}"
                    ax.text(j, i, label, ha="center", va="center", fontsize=6,
                            color="white" if value is not None and value < .65 else "black")
            im = ax.imshow(np.ma.masked_invalid(values), vmin=0, vmax=1, cmap=cmap, aspect="auto")
            ax.set_xticks(range(len(xs)), [x.replace("_", "\n") for x in xs], rotation=35, ha="right", fontsize=7)
            ax.set_yticks(range(len(models)), models, fontsize=7)
            ax.set_title(target.replace("_", " "), fontsize=10)
            if mode == "model_opponent":
                ax.set_xlabel("Opponent; diagonal = self-play")
            ax.set_ylabel("Focal model")
        for ax in list(axes.flat)[len(targets):]:
            ax.axis("off")
        fig.suptitle("Equal-game macro rates: " + ("model × family" if mode == "model_family" else "self-play and cross-play"), fontsize=15)
        fig.text(.5, .01, "Counts pooled within game; games weighted equally. G = eligible games, E = eligible episodes, N = focal opportunities.\nGray NA = unsupported or no eligible observations. Two focal rows/episode are dependent; denominators are not independent sample sizes.", ha="center", fontsize=9)
        fig.tight_layout(rect=(0,.05,.95,.965))
        cax = fig.add_axes((.965,.18,.012,.6))
        fig.colorbar(im, cax=cax, label="Rate (0–1)")
        _save_figure(fig, out, mode)
        files.append(mode)
        plt.close(fig)
    for level in ("game", "cell"):
        fig, axes = plt.subplots(rows, columns, figsize=(15, 4*rows), squeeze=False)
        for ax, target in zip(axes.flat, targets):
            points = derivation["targets"][target][level + "_points"]
            metric = summary["targets"][target]["split_half"][level]
            ax.plot([0,1], [0,1], color="#888888", linestyle="--", linewidth=1)
            if points:
                ax.scatter([p["left"] for p in points], [p["right"] for p in points], s=23 if level == "game" else 10, alpha=.65, color="#285f8f")
            else:
                ax.set_facecolor("#eeeeee")
                ax.text(.5, .5, "No matched eligible halves", ha="center", va="center", transform=ax.transAxes)
            coefficient = "NA" if metric["pearson"] is None else f"{metric['pearson']:.2f}"
            ci = metric["intervals"]["pearson"]
            interval = "CI unavailable" if ci["lower"] is None else f"95% CI [{ci['lower']:.2f}, {ci['upper']:.2f}]"
            ax.set_title(target.replace("_", " "), fontsize=10)
            ax.text(.03, .98, f"r={coefficient}; {interval}\nG={metric['games']}; paired points={metric['paired_points']}", transform=ax.transAxes, va="top", fontsize=8)
            ax.set(xlim=(-.04,1.04), ylim=(-.04,1.04), xlabel="Trials 0,1", ylabel="Trials 2,3")
        for ax in list(axes.flat)[len(targets):]:
            ax.axis("off")
        fig.suptitle(f"Split-half agreement: {level} level (descriptive)", fontsize=15)
        fig.text(.5, .01, "Only completed four-trial cells with matching label composition and nonzero opportunities in both halves.\nGame level pools the same eligible cells in each half. Correlations weight games equally; intervals resample complete game-shape clusters.", ha="center", fontsize=9)
        fig.tight_layout(rect=(0,.05,1,.965))
        stem = f"replicate_agreement_{level}"
        _save_figure(fig, out, stem)
        files.append(stem)
        plt.close(fig)
    return [f"{stem}.{suffix}" for stem in files for suffix in ("png", "svg", "pdf")]


def run(records_path, out, bootstrap=300, seed=20260910, plots=True):
    out = Path(out).resolve()
    if not out.is_relative_to(Path("/shared/allie")):
        raise ValueError("Diagnostics output must remain under /shared/allie")
    records = load_records(records_path)
    summary, derivation = build_diagnostics(records, bootstrap, seed)
    summary["records_source"] = str(Path(records_path).resolve())
    summary["source_file_sha256"] = hashlib.sha256(Path(records_path).read_bytes()).hexdigest()
    out.mkdir(parents=True, exist_ok=True)
    summary["figures"] = render_figures(summary, derivation, out) if plots else []
    write_json(out / "diagnostics.json", summary)
    write_json(out / "derivation.json", derivation)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--bootstrap", type=int, default=300)
    parser.add_argument("--seed", type=int, default=20260910)
    parser.add_argument("--no-plots", action="store_true")
    args = parser.parse_args()
    if args.bootstrap < 0:
        parser.error("--bootstrap must be nonnegative")
    result = run(args.records, args.out, args.bootstrap, args.seed, not args.no_plots)
    print(json.dumps({"records": result["records"], "episodes": result["episodes"], "games": result["games"],
                      "targets": result["target_names"], "out": str(Path(args.out).resolve())}))


if __name__ == "__main__":
    main()
