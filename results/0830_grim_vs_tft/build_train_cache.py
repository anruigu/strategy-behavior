#!/usr/bin/env python
"""Cache every grim-vs-tft training-time behaviour statistic into train_strategy.json.

    /home/allie/venvs/tinker-ipd/bin/python build_train_cache.py [--outdir DIR] [--update-ground-truth]

Enumerates the think4 nohole grid -- 2 opponents x 3 arms x 3 seeds -- and reads
whichever of those cells have actually written traces; the rest are recorded
under `meta.run_dirs_empty_or_missing` rather than silently assumed present.
Writes `train_strategy.json` into `--outdir`, which defaults to this file's own
directory. All statistic definitions live in `strategy_stats.py`; this script
only groups, pools and serialises them, so the figures and the cache cannot
disagree about what `defect_before_last` means.

WHAT IS AND IS NOT COMPARABLE. `ipd` is the shape env -- the opponent IS the
manipulation, so a grim-vs-tft difference there is confounded with the
environment. `public_goods`/`dond`/`trust` face identical opponent populations
in both arms and are the clean transfer test. The two groups are kept in
separate top-level sections and never pooled.

EVERY ERROR BAR IS BETWEEN TRAINING SEED: each seed is collapsed to one number
before any spread is taken, and `se` is null wherever fewer than two seeds
contribute. Rates are pooled from (numerator, denominator) pairs within a seed
first; a seed with an empty denominator contributes null, not zero.

THE GROUND-TRUTH GUARD. `GROUND_TRUTH` below records the pooled ipd numbers as
of the last deliberate refresh, and every build compares the live runs against
it. The two halves of that comparison mean different things and are reported
separately, because conflating them is how a guard goes quiet:

  * EPISODE COUNTS are INFORMATIONAL. This wave is still training and appends
    trace files as it goes, so counts only ever grow, and growth carries no
    information about whether anything is wrong. A count that FALLS is a hard
    failure: episodes cannot disappear unless the loader or the invalid-rate
    filter broke.
  * RATES are the guard. Any rate moving by more than 0.02 is a hard failure --
    that is the drift this block exists to catch -- and between 0.005 and 0.02
    it warns.

Every build records what it actually observed, plus the mtimes of each run's
`metrics.jsonl` and newest trace file, under `meta.ground_truth` and
`meta.run_state`. A cache therefore always carries a description of the run
state it was built from, and two caches came from the same snapshot if and only
if their `meta.run_state.digest` agree. Refreshing the recorded table is a
deliberate one-command act: `--update-ground-truth` rewrites the literal below
to the observed values and prints what it changed. The default is to check and
report, never to rewrite.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from strategy_stats import (ARMS, FUNNEL_STAGES, IPD_PAIR_STATS,
                            IPD_SCALAR_STATS, OPPONENTS, RUNS, SEEDS,
                            SHAPE_ENV, SHARED_OPPONENT_ENVS,
                            VALID_MAX_INVALID, between_seed, ipd_strategy,
                            is_valid_episode, iter_episodes, iter_runs,
                            load_metrics, mean_or_none, nonipd_strategy,
                            pooled_rate, survey_runs)

HERE = Path(__file__).resolve().parent
OUT_NAME = "train_strategy.json"

LATE_STEP = 25
TRAINED_STEP = 5

STATS_SPEC: tuple[tuple[str, str], ...] = (
    tuple((s, "scalar") for s in IPD_SCALAR_STATS)
    + tuple((s, "pair") for s in IPD_PAIR_STATS)
)

NONIPD_STATS = ("exploit_rate", "capture", "payoff", "invalid_rate", "defection_rate")

METRIC_KEYS = ("train/endgame_rate", "train/defection_rate", "train/exploit_rate",
               "train/reward", "train/capture", "train/invalid_rate",
               "train/first_betrayal_frac", "train/betrayed_any",
               "train/retaliated", "train/credibility", "train/welfare",
               "train/opp_payoff", "env/ipd/exploit_rate", "env/ipd/reward",
               "env/ipd/capture")

WHY_SHARED = (
    "public_goods, dond and trust draw from IDENTICAL opponent populations in "
    "both the grim and the tft arm (public_goods: strict_punisher, "
    "conditional_punisher, conditional_noisy; dond: sceptic, auditor, verifier; "
    "trust: responsive, impatient, responsive_exit) -- verified against every "
    "trace file and re-asserted at build time under meta.opponent_populations. "
    "Only the ipd opponent differs by arm. These three envs are therefore the "
    "TRANSFER TEST: a grim-vs-tft difference here cannot be explained by the "
    "environment and is a genuine difference in the learned policy, whereas any "
    "ipd difference confounds policy with opponent."
)

TRACE_SAMPLING_NOTE = (
    "Trace dumps are the FIRST 24 episodes of every 5th training step (0, 5, 10, "
    "...), covering exactly 4 envs at 6 episodes each: ipd, public_goods, dond, "
    "trust. So there are ~6 ipd episodes per step per seed, and the other three "
    "trained envs -- ipd3, staghunt, winasmuch -- NEVER appear in the traces even "
    "though they do contribute to the pooled train/* metrics in metrics_curves. "
    "Trace-derived and metrics-derived numbers therefore have different "
    "denominators and must not be divided by one another."
)

# Observed values as of the last `--update-ground-truth`, in GT_FIELDS order.
# Rewritten only by that flag -- never edit by hand, or the recorded table stops
# being a record of anything a build actually saw.
GT_FIELDS = ("n_episodes", "coop_rate", "ever_defect", "defects_last_round",
             "defect_before_last", "opp_defect_rate")
GROUND_TRUTH = {
    "grim/base": (167, 0.905, 0.856, 0.856, 0.090, 0.009),
    "grim/eg":   (150, 0.918, 0.800, 0.800, 0.020, 0.002),
    "grim/inf":  (54,  0.991, 0.093, 0.093, 0.000, 0.000),
    "tft/base":  (186, 0.893, 0.919, 0.919, 0.145, 0.015),
    "tft/eg":    (185, 0.917, 0.735, 0.735, 0.092, 0.009),
    "tft/inf":   (108, 0.982, 0.176, 0.176, 0.000, 0.000),
}
GT_WARN = 0.005
GT_FAIL = 0.02

GT_LITERAL_RE = re.compile(r"^GROUND_TRUTH = \{\n.*?^\}\n", re.MULTILINE | re.DOTALL)


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--outdir", type=Path, default=HERE,
                    help=f"directory to write {OUT_NAME} into (default: beside this script)")
    ap.add_argument("--update-ground-truth", action="store_true",
                    help="rewrite the GROUND_TRUTH literal in this file to the observed "
                         "values and print what changed; default is to check only")
    return ap


# --------------------------------------------------------------------------- #
# provenance: which snapshot of the still-appending runs this build saw
# --------------------------------------------------------------------------- #
def _file_state(path: Path | None) -> dict | None:
    if path is None or not path.is_file():
        return None
    st = path.stat()
    return {"name": path.name, "bytes": st.st_size,
            "mtime_utc": datetime.fromtimestamp(st.st_mtime, timezone.utc)
                                 .isoformat(timespec="seconds")}


def run_state(d: Path) -> dict:
    """When this run dir was last written, so the cache pins its own input snapshot."""
    traces = sorted((d / "traces").glob("step_*.jsonl")) if (d / "traces").is_dir() else []
    newest = max(traces, key=lambda p: p.stat().st_mtime, default=None)
    return {
        "run_dir": d.name,
        "metrics_jsonl": _file_state(d / "metrics.jsonl"),
        "n_trace_files": len(traces),
        "newest_trace": _file_state(newest),
    }


def run_state_digest(states: dict[str, dict]) -> str:
    """Stable hash of every recorded mtime and size: equal iff same input snapshot."""
    h = hashlib.sha256()
    for cell in sorted(states):
        state = states[cell]
        for rec in (state["metrics_jsonl"], state["newest_trace"]):
            part = "-" if rec is None else f"{rec['name']}:{rec['bytes']}:{rec['mtime_utc']}"
            h.update(f"{cell}|{part}\n".encode())
    return h.hexdigest()[:16]


# --------------------------------------------------------------------------- #
# ground-truth refresh
# --------------------------------------------------------------------------- #
def render_ground_truth(observed: dict[str, tuple]) -> str:
    """The GROUND_TRUTH literal, formatted exactly as it is written by hand above."""
    keys = sorted(observed)
    key_fields = {k: f'"{k}":' for k in keys}
    n_fields = {k: f"{int(observed[k][0])}," for k in keys}
    kw = max(len(v) for v in key_fields.values())
    nw = max(len(v) for v in n_fields.values())
    lines = ["GROUND_TRUTH = {"]
    for k in keys:
        rates = ", ".join(f"{v:.3f}" for v in observed[k][1:])
        lines.append(f"    {key_fields[k]:<{kw}} ({n_fields[k]:<{nw}} {rates}),")
    lines.append("}")
    return "\n".join(lines) + "\n"


def print_ground_truth_diff(observed: dict[str, tuple]) -> None:
    for key in sorted(observed):
        new = observed[key]
        old = GROUND_TRUTH.get(key)
        if old is None:
            rates = ", ".join(f"{v:.3f}" for v in new[1:])
            print(f"  + {key}: new cell -> ({int(new[0])}, {rates})")
            continue
        changed = []
        for i, name in enumerate(GT_FIELDS):
            o, n = old[i], new[i]
            if i == 0:
                if int(o) != int(n):
                    changed.append(f"{name} {int(o)} -> {int(n)} ({int(n) - int(o):+d})")
            elif round(n, 3) != round(o, 3):
                changed.append(f"{name} {o:.3f} -> {n:.3f} ({n - o:+.3f})")
        if changed:
            print(f"  ~ {key}: " + "; ".join(changed))
        else:
            print(f"  = {key}: unchanged")
    # A cell the build did not see is KEPT, not dropped: a run dir that is
    # briefly unreadable must not be able to delete its own recorded row.
    for key in sorted(set(GROUND_TRUTH) - set(observed)):
        print(f"  ! {key}: recorded but no episodes seen this build; row kept as-is")


def rewrite_ground_truth(path: Path, observed: dict[str, tuple]) -> bool:
    src = path.read_text()
    if not GT_LITERAL_RE.search(src):
        print(f"  cannot rewrite: no GROUND_TRUTH literal found in {path}")
        return False
    merged = dict(GROUND_TRUTH)
    merged.update(observed)
    block = render_ground_truth(merged)
    updated = GT_LITERAL_RE.sub(lambda _m: block, src, count=1)
    if updated == src:
        print("  GROUND_TRUTH already matches the observed values; nothing rewritten")
        return True
    path.write_text(updated)
    print(f"  rewrote GROUND_TRUTH in {path}")
    return True


# --------------------------------------------------------------------------- #
# aggregation over {seed: [(step, episode), ...]}
# --------------------------------------------------------------------------- #
def _seed_stat(eps: list[dict], stat: str, kind: str) -> tuple[float | None, int]:
    if kind == "pair":
        return pooled_rate([e[stat] for e in eps])
    return mean_or_none([e[stat] for e in eps])


def _at_step(cell: dict[int, list[tuple[int, dict]]], seed: int, keep) -> list[dict]:
    return [e for step, e in cell[seed] if keep(step)]


def by_step_stats(cell: dict[int, list[tuple[int, dict]]], spec) -> dict:
    seeds = sorted(cell)
    steps = sorted({step for eps in cell.values() for step, _ in eps})
    out: dict = {}
    for stat, kind in spec:
        rec: dict = {"steps": steps,
                     "per_seed": {str(s): [] for s in seeds},
                     "mean": [], "se": [], "n_seeds": [], "n_episodes": []}
        for step in steps:
            vals = []
            n_ep = 0
            for seed in seeds:
                eps = _at_step(cell, seed, lambda s, t=step: s == t)
                val, _ = _seed_stat(eps, stat, kind)
                rec["per_seed"][str(seed)].append(val)
                vals.append(val)
                n_ep += len(eps)
            mean, se, n_seeds = between_seed(vals)
            rec["mean"].append(mean)
            rec["se"].append(se)
            rec["n_seeds"].append(n_seeds)
            rec["n_episodes"].append(n_ep)
        out[stat] = rec
    return out


def pooled_stats(cell: dict[int, list[tuple[int, dict]]], spec, keep) -> dict:
    seeds = sorted(cell)
    out: dict = {}
    for stat, kind in spec:
        per_seed: dict[str, float | None] = {}
        per_seed_n: dict[str, int] = {}
        n_ep = 0
        for seed in seeds:
            eps = _at_step(cell, seed, keep)
            val, n = _seed_stat(eps, stat, kind)
            per_seed[str(seed)] = val
            per_seed_n[str(seed)] = n
            n_ep += len(eps)
        mean, se, n_seeds = between_seed(per_seed.values())
        out[stat] = {"per_seed": per_seed, "per_seed_n": per_seed_n,
                     "mean": mean, "se": se, "n_seeds": n_seeds,
                     "n_episodes": n_ep}
    return out


def hazard_block(cell: dict[int, list[tuple[int, dict]]], keep) -> dict:
    seeds = sorted(cell)
    eps_by_seed = {s: _at_step(cell, s, keep) for s in seeds}
    max_rounds = max((len(e["hazard"]) for eps in eps_by_seed.values() for e in eps),
                     default=0)
    out: dict = {}
    for direction in ("by_round_index", "by_rounds_from_end"):
        rec: dict = {"x": list(range(max_rounds)),
                     "per_seed": {str(s): [] for s in seeds},
                     "mean": [], "se": [], "n": []}
        for r in range(max_rounds):
            vals = []
            total = 0
            for seed in seeds:
                hs = []
                for e in eps_by_seed[seed]:
                    h = e["hazard"]
                    if len(h) <= r:
                        continue
                    hs.append(h[r] if direction == "by_round_index" else h[len(h) - 1 - r])
                val = sum(hs) / len(hs) if hs else None
                rec["per_seed"][str(seed)].append(val)
                vals.append(val)
                total += len(hs)
            mean, se, _ = between_seed(vals)
            rec["mean"].append(mean)
            rec["se"].append(se)
            rec["n"].append(total)
        out[direction] = rec
    return out


def funnel_block(cell: dict[int, list[tuple[int, dict]]], keep) -> dict:
    seeds = sorted(cell)
    out: dict = {}
    for stage in FUNNEL_STAGES:
        per_seed: dict[str, dict] = {}
        seed_rates = []
        tot_num = tot_den = 0
        for seed in seeds:
            num = den = 0
            for e in _at_step(cell, seed, keep):
                val = e[stage]
                if val is None:
                    continue
                den += 1
                num += 1 if val else 0
            rate = num / den if den else None
            per_seed[str(seed)] = {"num": num, "den": den, "rate": rate}
            seed_rates.append(rate)
            tot_num += num
            tot_den += den
        mean, se, n_seeds = between_seed(seed_rates)
        out[stage] = {"per_seed": per_seed, "num": tot_num, "den": tot_den,
                      "pooled_rate": tot_num / tot_den if tot_den else None,
                      "mean_of_seed_rates": mean, "se": se, "n_seeds": n_seeds}
    return out


# --------------------------------------------------------------------------- #
# load
# --------------------------------------------------------------------------- #
def main() -> int:
    # Parse first: --help and a bad --outdir must exit before any run is read.
    args = build_parser().parse_args()
    out_path = args.outdir / OUT_NAME
    args.outdir.mkdir(parents=True, exist_ok=True)

    ipd: dict[str, dict[int, list[tuple[int, dict]]]] = defaultdict(lambda: defaultdict(list))
    nonipd: dict[str, dict[int, list[tuple[int, dict]]]] = defaultdict(lambda: defaultdict(list))
    kept: dict[str, int] = defaultdict(int)
    dropped: dict[str, int] = defaultdict(int)
    cell_steps: dict[str, list[int]] = {}
    populations: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    metrics: dict[str, dict[int, dict]] = {}
    states: dict[str, dict] = {}

    for opponent, arm, seed, d in iter_runs():
        arm_key = f"{opponent}/{arm}"
        cell_key = f"{opponent}/{arm}/s{seed}"
        # Captured before the episodes are read, so the recorded mtimes bound
        # the snapshot from below even if the run appends mid-build.
        states[cell_key] = run_state(d)
        metrics[cell_key] = load_metrics(d)
        steps_seen = set()
        for step, row in iter_episodes(d):
            env = row.get("env")
            steps_seen.add(step)
            populations[f"{opponent}/{env}"][str(row.get("opponent"))] += 1
            if env == SHAPE_ENV:
                if not is_valid_episode(row):
                    dropped[cell_key] += 1
                    continue
                strat = ipd_strategy(row)
                if strat is None:
                    dropped[cell_key] += 1
                    continue
                kept[cell_key] += 1
                ipd[arm_key][seed].append((step, strat))
            elif env in SHARED_OPPONENT_ENVS:
                if not is_valid_episode(row):
                    continue
                nonipd[f"{arm_key}/{env}"][seed].append((step, nonipd_strategy(row)))
        cell_steps[cell_key] = sorted(steps_seen)

    found, empty = survey_runs()

    # ------------------------------------------------------------------ #
    # ground truth: episode counts are informational, rates are the guard
    # ------------------------------------------------------------------ #
    problems: list[str] = []
    rate_failures: list[str] = []
    rate_warnings: list[str] = []
    episode_growth: list[str] = []
    gt_cells: dict[str, dict] = {}
    observed_gt: dict[str, tuple] = {}
    table_rows: list[tuple] = []
    for arm_key in sorted(ipd):
        eps = [e for seed in ipd[arm_key] for _s, e in ipd[arm_key][seed]]
        coop_rw, _ = pooled_rate([e["coop_rounds"] for e in eps])
        opp_d_rw, _ = pooled_rate([e["opp_defect_rounds"] for e in eps])
        coop_ep, _ = mean_or_none([e["coop_rate"] for e in eps])
        ever_d, _ = mean_or_none([e["ever_defect"] for e in eps])
        d_last, _ = mean_or_none([e["defects_last_round"] for e in eps])
        d_b4, _ = mean_or_none([e["defect_before_last"] for e in eps])
        table_rows.append((arm_key, len(eps), coop_rw, coop_ep, ever_d, d_last,
                           d_b4, opp_d_rw))

        measured = (coop_rw, ever_d, d_last, d_b4, opp_d_rw)
        observed = dict(zip(GT_FIELDS, (len(eps),) + measured))
        if all(v is not None for v in measured):
            observed_gt[arm_key] = (len(eps),) + measured

        exp = GROUND_TRUTH.get(arm_key)
        if exp is None:
            gt_cells[arm_key] = {"recorded": None, "observed": observed,
                                 "status": "unrecorded"}
            msg = f"{arm_key}: cell not in GROUND_TRUTH"
            if args.update_ground_truth:
                episode_growth.append(msg + "; will be added by --update-ground-truth")
            else:
                problems.append(msg)
            continue

        e_n, e_coop, e_ever, e_last, e_b4, e_oppd = exp
        n_delta = len(eps) - e_n
        if n_delta < 0:
            problems.append(f"{arm_key}: n_ep {len(eps)} < recorded {e_n} "
                            f"({n_delta}); episodes cannot disappear -- loader or "
                            f"filter broke")
        elif n_delta > 0:
            episode_growth.append(f"{arm_key}: {e_n} -> {len(eps)} (+{n_delta})")

        status = "ok"
        rate_deltas: dict[str, dict] = {}
        for name, got, want in (("coop_rate", coop_rw, e_coop),
                                ("ever_defect", ever_d, e_ever),
                                ("defects_last_round", d_last, e_last),
                                ("defect_before_last", d_b4, e_b4),
                                ("opp_defect_rate", opp_d_rw, e_oppd)):
            if got is None:
                problems.append(f"{arm_key}.{name}: got None, want {want}")
                status = "undefined"
                continue
            diff = got - want
            rate_deltas[name] = {"recorded": want, "observed": round(got, 6),
                                 "delta": round(diff, 6)}
            if abs(diff) > GT_FAIL:
                status = "drift_fail"
                rate_failures.append(f"{arm_key}.{name}: {got:.3f} vs recorded {want:.3f} "
                                     f"(diff {abs(diff):.3f} > {GT_FAIL})")
            elif abs(diff) > GT_WARN:
                if status == "ok":
                    status = "drift_warn"
                rate_warnings.append(f"{arm_key}.{name}: {got:.3f} vs recorded {want:.3f} "
                                     f"(diff {abs(diff):.3f}); new steps have moved it")
        gt_cells[arm_key] = {
            "recorded": dict(zip(GT_FIELDS, exp)),
            "observed": observed,
            "n_episodes_delta": n_delta,
            "rates": rate_deltas,
            "status": status,
        }

        # Not a bug: essentially all defection in this wave lands in the final
        # round, so the two are the same number to three decimals everywhere.
        if ever_d is not None and d_last is not None and abs(ever_d - d_last) > GT_FAIL:
            problems.append(f"{arm_key}: ever_defect {ever_d:.3f} != "
                            f"defects_last_round {d_last:.3f}; the "
                            f"all-defection-is-endgame invariant broke")

    # ------------------------------------------------------------------ #
    # assemble
    # ------------------------------------------------------------------ #
    cache: dict = {}
    cache["meta"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "runs_root": str(RUNS),
        "invalid_rate_threshold": VALID_MAX_INVALID,
        "invalid_rate_rule": "episode dropped when stats.invalid_rate > threshold",
        "shape_env": SHAPE_ENV,
        "shared_opponent_envs": list(SHARED_OPPONENT_ENVS),
        "opponents": list(OPPONENTS),
        "arms": list(ARMS),
        "seeds": list(SEEDS),
        "late_step": LATE_STEP,
        "trained_step": TRAINED_STEP,
        "trace_sampling_note": TRACE_SAMPLING_NOTE,
        "episodes_kept_ipd": dict(sorted(kept.items())),
        "episodes_dropped_ipd": {k: dropped.get(k, 0) for k in sorted(kept)},
        "steps_per_cell": {k: cell_steps[k] for k in sorted(cell_steps)},
        "run_dirs_found": found,
        "run_dirs_empty_or_missing": empty,
        "opponent_populations": {k: dict(sorted(v.items()))
                                 for k, v in sorted(populations.items())},
        # Rate drift only. Episode growth is expected while the wave trains and
        # is reported under ground_truth.episode_growth, not as a warning.
        "ground_truth_warnings": rate_warnings,
        "ground_truth": {
            "checked_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "fields": list(GT_FIELDS),
            "rate_warn_threshold": GT_WARN,
            "rate_fail_threshold": GT_FAIL,
            "what_each_half_means": (
                "Episode counts are INFORMATIONAL: the runs are live and only "
                "append, so growth says nothing about correctness -- a count "
                "that FALLS is the hard failure. Rates are the guard: any rate "
                f"moving more than {GT_FAIL} fails the build. Refresh the "
                "recorded table with --update-ground-truth, never by hand."),
            "cells": gt_cells,
            "episode_growth": episode_growth,
            "rate_warnings": rate_warnings,
            "rate_failures": rate_failures,
        },
        "run_state": {
            "what": (
                "Per-run mtimes of metrics.jsonl and of the newest traces/step_*.jsonl "
                "as seen at the start of this build. The runs append while this script "
                "reads them, so these pin the snapshot the numbers describe: two caches "
                "were built from the same run state if and only if their digests match."),
            "captured_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "digest": run_state_digest(states),
            "cells": {k: states[k] for k in sorted(states)},
        },
        "error_bar_convention": (
            "Every mean/se pair is BETWEEN TRAINING SEED: each seed collapsed to "
            "one number, then spread across seeds. se is null when n_seeds < 2 -- "
            "draw no bar, not a zero-length one."),
        "shared_opponent_envs_reserved_keys": ["why", "pooled_three_envs"],
    }

    cache["cells"] = {}
    for cell_key in sorted(kept):
        opponent, arm, seed_s = cell_key.split("/")
        seed = int(seed_s[1:])
        arm_key = f"{opponent}/{arm}"
        one = {seed: ipd[arm_key][seed]}
        per_step = {}
        for stat, kind in STATS_SPEC:
            block = by_step_stats(one, ((stat, kind),))[stat]
            per_step[stat] = {"steps": block["steps"],
                              "values": block["per_seed"][str(seed)],
                              "n_episodes": block["n_episodes"]}
        cache["cells"][cell_key] = {
            "n_episodes_ipd": kept[cell_key],
            "n_dropped_ipd": dropped.get(cell_key, 0),
            "steps": cell_steps[cell_key],
            "per_step": per_step,
        }

    cache["by_step"] = {k: by_step_stats(ipd[k], STATS_SPEC) for k in sorted(ipd)}
    cache["pooled_late"] = {k: pooled_stats(ipd[k], STATS_SPEC, lambda s: s >= LATE_STEP)
                            for k in sorted(ipd)}
    cache["pooled_all"] = {k: pooled_stats(ipd[k], STATS_SPEC, lambda s: s >= TRAINED_STEP)
                           for k in sorted(ipd)}
    # step 0 is the untrained base model, identical in both arms by construction:
    # the shared starting point and therefore the control for every arm contrast.
    cache["step0"] = {k: pooled_stats(ipd[k], STATS_SPEC, lambda s: s == 0)
                      for k in sorted(ipd)}
    cache["hazard"] = {k: hazard_block(ipd[k], lambda s: s >= LATE_STEP)
                       for k in sorted(ipd)}
    cache["funnel"] = {k: funnel_block(ipd[k], lambda s: s >= TRAINED_STEP)
                       for k in sorted(ipd)}

    shared: dict = {"why": WHY_SHARED}
    nonipd_spec = tuple((s, "scalar") for s in NONIPD_STATS)
    for key in sorted(nonipd):
        shared[key] = {
            "by_step": by_step_stats(nonipd[key], nonipd_spec),
            "pooled_late": pooled_stats(nonipd[key], nonipd_spec, lambda s: s >= LATE_STEP),
            "pooled_all": pooled_stats(nonipd[key], nonipd_spec, lambda s: s >= TRAINED_STEP),
        }
    pooled3: dict = {}
    for opponent in OPPONENTS:
        for arm in ARMS:
            arm_key = f"{opponent}/{arm}"
            envs = [e for e in SHARED_OPPONENT_ENVS if f"{arm_key}/{e}" in nonipd]
            if not envs:
                continue
            seeds = sorted({s for e in envs for s in nonipd[f"{arm_key}/{e}"]})
            entry: dict = {"envs": envs}
            for stat in NONIPD_STATS:
                per_seed: dict[str, float | None] = {}
                for seed in seeds:
                    # average of the three env-level seed values, so an env with
                    # more episodes does not outweigh the others
                    vals = []
                    for env in envs:
                        eps = [r for _s, r in nonipd[f"{arm_key}/{env}"].get(seed, [])
                               if _s >= LATE_STEP]
                        val, _ = mean_or_none([r[stat] for r in eps])
                        if val is not None:
                            vals.append(val)
                    per_seed[str(seed)] = sum(vals) / len(vals) if vals else None
                mean, se, n_seeds = between_seed(per_seed.values())
                entry[stat] = {"per_seed": per_seed, "mean": mean, "se": se,
                               "n_seeds": n_seeds}
            pooled3[arm_key] = entry
    shared["pooled_three_envs"] = pooled3
    cache["shared_opponent_envs"] = shared

    curves: dict = {}
    for opponent in OPPONENTS:
        for arm in ARMS:
            arm_key = f"{opponent}/{arm}"
            cells = {seed: metrics[f"{arm_key}/s{seed}"]
                     for seed in SEEDS if f"{arm_key}/s{seed}" in metrics}
            if not cells:
                continue
            steps = sorted({s for m in cells.values() for s in m})
            block: dict = {}
            for metric in METRIC_KEYS:
                rec: dict = {"steps": steps,
                             "per_seed": {str(s): [] for s in sorted(cells)},
                             "mean": [], "se": [], "n_seeds": []}
                for step in steps:
                    vals = []
                    for seed in sorted(cells):
                        raw = cells[seed].get(step, {}).get(metric)
                        val = None if raw is None else float(raw)
                        rec["per_seed"][str(seed)].append(val)
                        vals.append(val)
                    mean, se, n_seeds = between_seed(vals)
                    rec["mean"].append(mean)
                    rec["se"].append(se)
                    rec["n_seeds"].append(n_seeds)
                block[metric] = rec
            curves[arm_key] = block
    cache["metrics_curves"] = curves

    out_path.write_text(json.dumps(cache, indent=1))

    # ------------------------------------------------------------------ #
    # report
    # ------------------------------------------------------------------ #
    def fmt(v, spec="7.3f"):
        return "     --" if v is None else format(v, spec)

    print(f"wrote {out_path}  ({out_path.stat().st_size / 1e6:.2f} MB)")
    print(f"top-level keys: {', '.join(cache)}")

    print("\n=== ipd (shape env -- opponent IS the manipulation, confounded) ===")
    head = (f"{'cell':<11} {'n_ep':>5} {'drop':>5} {'coop_rw':>8} {'coop_ep':>8} "
            f"{'ever_d':>7} {'d_last':>7} {'d_b4last':>9} {'opp_d':>7}")
    print(head)
    print("-" * len(head))
    for key, n, coop_rw, coop_ep, ever_d, d_last, d_b4, opp_d in table_rows:
        print(f"{key:<11} {n:5d} "
              f"{sum(dropped.get(f'{key}/s{s}', 0) for s in SEEDS):5d} "
              f"{fmt(coop_rw, '8.3f')} {fmt(coop_ep, '8.3f')} {fmt(ever_d)} "
              f"{fmt(d_last)} {fmt(d_b4, '9.3f')} {fmt(opp_d)}")

    print("\n=== ipd late (steps >= 25), mean +- se BETWEEN SEED ===")
    head = (f"{'cell':<11} {'seeds':>5} {'d_b4last':>16} {'coop_rate':>16} "
            f"{'c|own_d':>16} {'in_punish':>16}")
    print(head)
    print("-" * len(head))
    for key in sorted(cache["pooled_late"]):
        blk = cache["pooled_late"][key]
        cols = []
        for stat in ("defect_before_last", "coop_rate", "c_given_own_d",
                     "rounds_in_punishment"):
            rec = blk[stat]
            if rec["mean"] is None:
                cols.append(f"{'--':>16}")
            elif rec["se"] is None:
                cols.append(f"{rec['mean']:>10.3f} (n1)")
            else:
                cols.append(f"{rec['mean']:>8.3f} +-{rec['se']:6.3f}")
        n_seeds = blk["defect_before_last"]["n_seeds"]
        print(f"{key:<11} {n_seeds:5d} " + " ".join(cols))

    print("\n=== transfer test: 3 shared-opponent envs pooled (steps >= 25) ===")
    head = f"{'cell':<11} {'seeds':>5} {'exploit_rate':>18} {'capture':>18} {'payoff':>18}"
    print(head)
    print("-" * len(head))
    for key in sorted(pooled3):
        entry = pooled3[key]
        cols = []
        for stat in ("exploit_rate", "capture", "payoff"):
            rec = entry[stat]
            if rec["mean"] is None:
                cols.append(f"{'--':>18}")
            elif rec["se"] is None:
                cols.append(f"{rec['mean']:>12.3f} (n1)")
            else:
                cols.append(f"{rec['mean']:>10.3f} +-{rec['se']:6.3f}")
        print(f"{key:<11} {entry['exploit_rate']['n_seeds']:5d} " + " ".join(cols))

    print("\n=== repair funnel (steps >= 5), pooled counts ===")
    head = f"{'cell':<11} " + " ".join(f"{s.replace('f_', ''):>22}" for s in FUNNEL_STAGES)
    print(head)
    print("-" * len(head))
    for key in sorted(cache["funnel"]):
        cols = []
        for stage in FUNNEL_STAGES:
            rec = cache["funnel"][key][stage]
            if rec["den"] == 0:
                cols.append(f"{'0/0':>22}")
            else:
                cols.append(f"{rec['num']:>6}/{rec['den']:<5} {rec['pooled_rate']:>8.3f}")
        print(f"{key:<11} " + " ".join(cols))

    rs = cache["meta"]["run_state"]
    print("\n=== run snapshot (runs are live; caches compare only within a digest) ===")
    head = (f"{'cell':<14} {'files':>5} {'newest trace':>16} "
            f"{'trace mtime UTC':>21} {'metrics mtime UTC':>21}")
    print(head)
    print("-" * len(head))
    for cell_key in sorted(rs["cells"]):
        st = rs["cells"][cell_key]
        tr, mx = st["newest_trace"], st["metrics_jsonl"]
        print(f"{cell_key:<14} {st['n_trace_files']:5d} "
              f"{(tr['name'] if tr else '--'):>16} "
              f"{(tr['mtime_utc'] if tr else '--'):>21} "
              f"{(mx['mtime_utc'] if mx else '--'):>21}")
    print(f"run_state digest: {rs['digest']}   captured {rs['captured_utc']}")

    print("\n=== ground truth ===")
    if episode_growth:
        print("  episode counts -- INFORMATIONAL, the wave is still appending:")
        for m in episode_growth:
            print(f"    info: {m}")
    else:
        print("  episode counts: unchanged from the recorded table")
    if rate_warnings:
        print(f"  rate drift inside tolerance (>{GT_WARN}, <={GT_FAIL}):")
        for w in rate_warnings:
            print(f"    warn: {w}")
    if rate_failures:
        print(f"  RATE DRIFT BEYOND TOLERANCE (>{GT_FAIL}) -- what this guard is for:")
        for f_ in rate_failures:
            print(f"    FAIL: {f_}")
    if problems:
        print("  STRUCTURAL FAILURES:")
        for p in problems:
            print(f"    FAIL: {p}")
    if not (rate_warnings or rate_failures or problems):
        print("  rates: OK, every cell inside tolerance")

    if args.update_ground_truth:
        print("\n--- UPDATING GROUND_TRUTH ---")
        if problems:
            print("  refusing to rewrite: the structural failures above must be "
                  "understood first, or a broken read gets baked into the record")
        else:
            print_ground_truth_diff(observed_gt)
            rewrite_ground_truth(Path(__file__).resolve(), observed_gt)
            print("  the cache just written was checked against the OLD table; "
                  "re-run without the flag to verify the new one")

    if problems:
        print(f"\n{len(problems)} structural check(s) failed; cache written but SUSPECT.")
        return 1
    if rate_failures and not args.update_ground_truth:
        print(f"\n{len(rate_failures)} rate(s) drifted past {GT_FAIL}; cache written but "
              f"SUSPECT. Re-derive the numbers, then --update-ground-truth if the move "
              f"is real.")
        return 1
    tail = f" ({len(rate_warnings)} tolerated rate warning(s))" if rate_warnings else ""
    print("\nground truth: OK" + tail)
    return 0


if __name__ == "__main__":
    sys.exit(main())
