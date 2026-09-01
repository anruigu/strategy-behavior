#!/usr/bin/env python
"""Strategy statistics for the think4 grim-vs-tft split: definitions + loaders.

    /home/allie/venvs/tinker-ipd/bin/python strategy_stats.py

Run directly, it prints the raw pooled ipd table that every consumer of this
module is checked against (see `build_train_cache.py`). Imported, it is the
single definition site for every behavioural statistic in the 0830 grim-vs-tft
analysis, so the cache builder and the figures cannot drift apart.

THE QUESTION. An RL wave trained one model against two scripted punishers that
differ in exactly one respect: `grim` never forgives a defection, `tft` forgives
the moment you return to cooperating. Did that produce a behaviourally different
policy, or only a different environment?

TWO KINDS OF ENV, ANSWERING DIFFERENT QUESTIONS. Verified by reading every trace
file, and re-asserted at build time:
  * `ipd` (`SHAPE_ENV`) -- the opponent IS the manipulation, `grim` in the grim
    arm and `tft` in the tft arm. Any difference here confounds "different
    learned policy" with "different environment", and must be reported as such.
  * `public_goods`, `dond`, `trust` (`SHARED_OPPONENT_ENVS`) -- the opponent
    populations are IDENTICAL in both arms (public_goods:
    strict_punisher/conditional_punisher/conditional_noisy; dond:
    sceptic/auditor/verifier; trust: responsive/impatient/responsive_exit).
    These are the clean transfer test: a grim-vs-tft difference here is a
    genuine learned-policy difference, unconfounded by the opponent.
Never pool the two groups.

EVERY ERROR BAR IN THIS ANALYSIS IS BETWEEN TRAINING SEED. Collapse each seed to
one number first, then take the spread across seeds -- that is what
`between_seed` does and it is the only spread any figure may draw. Pooling
episodes instead treats 6 correlated rollouts from one LoRA as 6 independent
observations, which shrinks the interval by roughly sqrt(n_episodes) and is what
produced the sign flip that `0826-endgame-by-opponent.md` §4 reported and three
seeds later contradicted. Rates are therefore never pre-divided in an episode
record: the conditional statistics below return explicit `(numerator,
denominator)` pairs so a consumer can pool within a seed and then, and only
then, average across seeds. `between_seed` returns `se is None` when fewer than
two seeds contribute; a figure must then draw NO bar, never a zero-length one.
"""
from __future__ import annotations

import json
import math
import statistics
from pathlib import Path
from typing import Iterable, Iterator

RUNS = Path("/shared/allie/think4/runs")

OPPONENTS = ("grim", "tft")
ARMS = ("base", "eg", "inf")
SEEDS = (0, 1, 2)
ARM_SUFFIX = {"base": "", "eg": "_eg2", "inf": "_inf"}

# A fourth seed was launched for every cell. It is deliberately outside SEEDS so
# nothing iterates it, but it stays in the survey so the cache records whether it
# has produced rollouts rather than leaving it unmentioned.
SURVEY_SEEDS = (0, 1, 2, 3)

SHAPE_ENV = "ipd"
SHARED_OPPONENT_ENVS = ("public_goods", "dond", "trust")

# Above this, most actions in the episode are the env's forced fallback move
# rather than anything the policy chose, so the episode measures the parser and
# not the behaviour. NOTE ON PROVENANCE: the figure code in
# `results/0830_endgame_traces/` gates cells at `invalid_rate > 0.15` and
# `HANDOFF-think4.md` §7 documents a `> 0.30` *monitoring* alert (not an episode
# filter); 0.25 is neither of those. It is used here because it is what the
# 0830 grim-vs-tft ground-truth counts were computed under. That disagreement is
# inert exactly when no episode's invalid_rate falls strictly between the
# competing gates, since then they all partition the episodes identically -- the
# ipd values have so far clustered well below 0.2 and at 0.5, leaving that
# interval empty, but the runs are still appending and nothing here enforces it.
# So the gate is applied in exactly one place, `is_valid_episode`, and every
# build re-derives its own kept and dropped counts rather than trusting a
# recorded total.
VALID_MAX_INVALID = 0.25

# Present on ipd `stats`, absent on the other three envs -- see `nonipd_strategy`.
NONIPD_FIELDS = ("exploit_rate", "capture", "payoff", "welfare", "premium",
                 "invalid_rate", "defection_rate", "betrayal_rate",
                 "first_betrayal_frac")


# --------------------------------------------------------------------------- #
# loaders
# --------------------------------------------------------------------------- #
def run_dir(opponent: str, arm: str, seed: int) -> Path:
    return RUNS / f"mixed_think4_nohole-think-{opponent}_d1_s{seed}{ARM_SUFFIX[arm]}"


def iter_runs() -> Iterator[tuple[str, str, int, Path]]:
    """Yield (opponent, arm, seed, run_dir) over OPPONENTS x ARMS x SEEDS.

    Enumerates the full nohole grid but yields only the cells that have written
    at least one trace file, so a launched-but-silent cell is skipped rather
    than counted as empty; `survey_runs` is what reports which those are. The
    yielded count is therefore a property of the runs, not a constant.

    `mixed_think4_hole-think_d1_s{0,1}` is deliberately not enumerated: it has no
    opponent split and it collapsed.
    """
    for opponent in OPPONENTS:
        for arm in ARMS:
            for seed in SEEDS:
                d = run_dir(opponent, arm, seed)
                if not (d / "traces").is_dir():
                    continue
                if not any((d / "traces").glob("step_*.jsonl")):
                    continue
                yield opponent, arm, seed, d


def survey_runs() -> tuple[list[str], list[str]]:
    """(dirs with traces, dirs that exist-but-empty or are missing) over s0..s3."""
    found: list[str] = []
    empty: list[str] = []
    for opponent in OPPONENTS:
        for arm in ARMS:
            for seed in SURVEY_SEEDS:
                d = run_dir(opponent, arm, seed)
                traces = d / "traces"
                if traces.is_dir() and any(traces.glob("step_*.jsonl")):
                    found.append(d.name)
                else:
                    empty.append(d.name)
    return found, empty


def load_metrics(run_dir_: Path) -> dict[int, dict]:
    """{step: record} from metrics.jsonl, deduped by step with last write winning.

    Resumed runs re-append rows for steps they have already logged, so a step
    can appear any number of times and the duplicates are real rather than a
    parse error. The last row for a step is the one written by the surviving
    trajectory, so deduping keeps it and the step count equals the number of
    distinct steps, never the line count.
    """
    path = run_dir_ / "metrics.jsonl"
    if not path.is_file():
        return {}
    out: dict[int, dict] = {}
    with path.open() as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            step = rec.get("step")
            if step is None:
                continue
            out[int(step)] = rec
    return dict(sorted(out.items()))


def iter_episodes(run_dir_: Path) -> Iterator[tuple[int, dict]]:
    """Yield (step, episode_row) for every episode in every traces/step_*.jsonl."""
    traces = run_dir_ / "traces"
    if not traces.is_dir():
        return
    for path in sorted(traces.glob("step_*.jsonl")):
        try:
            step = int(path.stem.split("_")[1])
        except (IndexError, ValueError):
            continue
        with path.open() as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield step, json.loads(line)
                except json.JSONDecodeError:
                    continue


def is_valid_episode(row: dict) -> bool:
    return float((row.get("stats") or {}).get("invalid_rate") or 0.0) <= VALID_MAX_INVALID


# --------------------------------------------------------------------------- #
# ipd strategy
# --------------------------------------------------------------------------- #
def ipd_strategy(row: dict) -> dict | None:
    """Behavioural decomposition of one ipd episode, or None if too short to score.

    Conditional and sequential statistics are returned as explicit
    `(numerator, denominator)` int pairs, never as rates -- see module docstring.
    """
    m = [d == "defect" for d in (row.get("my_decisions") or [])]
    o = [d == "defect" for d in (row.get("opp_decisions") or [])]
    n = min(len(m), len(o))
    if n < 2:
        return None
    m, o = m[:n], o[:n]

    first_defect_index = next((i for i, d in enumerate(m) if d), None)

    n_coop = sum(1 for d in m if not d)
    n_opp_coop = sum(1 for d in o if not d)
    n_mutual_c = sum(1 for a, b in zip(m, o) if not a and not b)

    c_opp_c = [0, 0]
    c_opp_d = [0, 0]
    c_own_d = [0, 0]
    copies = [0, 0]
    punished = [0, 0]
    for i in range(1, n):
        target = c_opp_d if o[i - 1] else c_opp_c
        target[1] += 1
        target[0] += 0 if m[i] else 1
        if m[i - 1]:
            c_own_d[1] += 1
            c_own_d[0] += 0 if m[i] else 1
        copies[1] += 1
        copies[0] += 1 if m[i] == o[i - 1] else 0
        punished[1] += 1
        punished[0] += 1 if any(o[:i]) else 0

    # Repair funnel. Each stage is None where its predecessor did not fire, so
    # the denominator of every stage is explicit rather than inferred.
    f_defect_before_last = any(m[:-1])
    f_opp_retaliated: bool | None = None
    f_model_returned: bool | None = None
    f_opp_forgave: bool | None = None
    if f_defect_before_last and first_defect_index is not None:
        # Gated on defect_before_last, not on ever_defect: a defection in the
        # final round leaves no round in which the opponent could retaliate, so
        # scoring it would report a trivially-False stage 2.
        retal = next((i for i in range(first_defect_index + 1, n) if o[i]), None)
        f_opp_retaliated = retal is not None
        if retal is not None:
            ret = next((i for i in range(retal + 1, n) if not m[i]), None)
            f_model_returned = ret is not None
            if ret is not None:
                # Structurally impossible under grim, which never returns to
                # cooperation once triggered; reachable only under tft. A
                # nonzero rate in the grim arm is a bug, not a finding.
                f_opp_forgave = any(not o[i] for i in range(ret + 1, n))

    return {
        "n_rounds": n,
        "coop_rate": n_coop / n,
        # The ENVIRONMENT's response, not the policy. Differs by construction
        # between arms; never read as a policy difference.
        "opp_coop_rate": n_opp_coop / n,
        "opens_c": not m[0],
        "ever_defect": any(m),
        "first_defect_index": first_defect_index,
        "first_defect_from_end": None if first_defect_index is None else n - 1 - first_defect_index,
        "defects_last_round": m[-1],
        # THE SINGLE MOST IMPORTANT STATISTIC IN THIS ANALYSIS. It is the only
        # behaviour grim and tft respond to differently: a defection in the
        # final round leaves the opponent no round in which to punish, so the
        # two scripts are observationally identical unless the model defects
        # before the last round. Any claim that the arms learned different
        # policies has to survive here.
        "defect_before_last": f_defect_before_last,
        "n_defects": sum(m),
        "mutual_c_rate": n_mutual_c / n,
        "hazard": [1.0 if d else 0.0 for d in m],
        # Round-weighted counterparts of the episode-mean rates above, so a
        # consumer can pool rounds across episodes of unequal length.
        "coop_rounds": (n_coop, n),
        "opp_coop_rounds": (n_opp_coop, n),
        "opp_defect_rounds": (n - n_opp_coop, n),
        "mutual_c_rounds": (n_mutual_c, n),
        "c_given_opp_c": tuple(c_opp_c),
        # Forgiveness: walking back into a relationship the opponent has already
        # broken. Under grim this is walking into a dead one.
        "c_given_opp_d": tuple(c_opp_d),
        # The model's own return to cooperation after its own defection. This is
        # the fair cross-arm comparison: it conditions on the model's move, not
        # the opponent's, so it is not mechanically shifted by the script.
        "c_given_own_d": tuple(c_own_d),
        "copies_opp_last": tuple(copies),
        # EXPOSURE. How much of the game is spent in the only regime where grim
        # and tft behave differently. A near-zero value here means the two arms
        # were, in practice, trained against the same opponent.
        "rounds_in_punishment": tuple(punished),
        "f_defect_before_last": f_defect_before_last,
        "f_opp_retaliated": f_opp_retaliated,
        "f_model_returned": f_model_returned,
        "f_opp_forgave": f_opp_forgave,
    }


IPD_SCALAR_STATS = ("n_rounds", "coop_rate", "opp_coop_rate", "opens_c",
                    "ever_defect", "defects_last_round", "defect_before_last",
                    "n_defects", "mutual_c_rate", "first_defect_index",
                    "first_defect_from_end")

IPD_PAIR_STATS = ("coop_rounds", "opp_coop_rounds", "opp_defect_rounds",
                  "mutual_c_rounds", "c_given_opp_c", "c_given_opp_d",
                  "c_given_own_d", "copies_opp_last", "rounds_in_punishment")

FUNNEL_STAGES = ("f_defect_before_last", "f_opp_retaliated",
                 "f_model_returned", "f_opp_forgave")


# --------------------------------------------------------------------------- #
# non-ipd strategy
# --------------------------------------------------------------------------- #
def nonipd_strategy(row: dict) -> dict:
    """Scalar summary of one public_goods / dond / trust episode.

    Missing keys default to None rather than 0.0: these three envs do not emit
    `defection_rate` or `betrayal_rate` at all, and a 0.0 there would read as
    "never defected" instead of "not measured".
    """
    stats = row.get("stats") or {}
    out: dict = {"env": row.get("env"), "opponent": row.get("opponent")}
    for key in NONIPD_FIELDS:
        val = stats.get(key)
        out[key] = None if val is None else float(val)
    return out


# --------------------------------------------------------------------------- #
# aggregation
# --------------------------------------------------------------------------- #
def between_seed(values: Iterable[float | None]) -> tuple[float | None, float | None, int]:
    """(mean, se, n) across TRAINING SEEDS. se is None when n < 2 -- draw no bar."""
    vals = [float(v) for v in values if v is not None]
    n = len(vals)
    if n == 0:
        return None, None, 0
    mean = sum(vals) / n
    if n < 2:
        return mean, None, n
    return mean, statistics.stdev(vals) / math.sqrt(n), n


def pooled_rate(pairs: Iterable[tuple[int, int]]) -> tuple[float | None, int]:
    """(num/den, den) over (numerator, denominator) pairs; (None, 0) if den == 0."""
    num = 0
    den = 0
    for pair in pairs:
        if pair is None:
            continue
        num += int(pair[0])
        den += int(pair[1])
    if den == 0:
        return None, 0
    return num / den, den


def mean_or_none(values: Iterable[float | None]) -> tuple[float | None, int]:
    """(episode-weighted mean, n contributing) ignoring Nones."""
    vals = [float(v) for v in values if v is not None]
    if not vals:
        return None, 0
    return sum(vals) / len(vals), len(vals)


# --------------------------------------------------------------------------- #
# self-check
# --------------------------------------------------------------------------- #
def _main() -> None:
    from collections import defaultdict

    cells: dict[str, list[dict]] = defaultdict(list)
    dropped: dict[str, int] = defaultdict(int)
    for opponent, arm, seed, d in iter_runs():
        key = f"{opponent}/{arm}"
        for _step, row in iter_episodes(d):
            if row.get("env") != SHAPE_ENV:
                continue
            if not is_valid_episode(row):
                dropped[key] += 1
                continue
            strat = ipd_strategy(row)
            if strat is not None:
                cells[key].append(strat)

    head = (f"{'cell':<11} {'n_ep':>5} {'drop':>5} {'coop_rw':>8} {'coop_ep':>8} "
            f"{'ever_d':>7} {'d_last':>7} {'d_b4last':>9} {'opp_d_rw':>9}")
    print(head)
    print("-" * len(head))
    for key in sorted(cells):
        eps = cells[key]
        coop_rw, _ = pooled_rate([e["coop_rounds"] for e in eps])
        opp_d_rw, _ = pooled_rate([e["opp_defect_rounds"] for e in eps])
        coop_ep, _ = mean_or_none([e["coop_rate"] for e in eps])
        ever_d, _ = mean_or_none([e["ever_defect"] for e in eps])
        d_last, _ = mean_or_none([e["defects_last_round"] for e in eps])
        d_b4, _ = mean_or_none([e["defect_before_last"] for e in eps])
        print(f"{key:<11} {len(eps):5d} {dropped[key]:5d} {coop_rw:8.3f} {coop_ep:8.3f} "
              f"{ever_d:7.3f} {d_last:7.3f} {d_b4:9.3f} {opp_d_rw:9.3f}")


if __name__ == "__main__":
    _main()
