#!/usr/bin/env python
"""Frozen-checkpoint evidence on whether training against grim vs tft made a different policy.

    /home/allie/venvs/tinker-ipd/bin/python build_eval_cache.py

  eval_strategy.json    every number, cached for the figures and the write-up

WHAT THIS CACHE IS FOR.

The wave "think4" trained Qwen3.8-27B LoRA on iterated social dilemmas, split by
the scripted opponent in the shape envs: `grim` (defects forever after your first
defection) and `tft` (mirrors your last move, forgives immediately). Crossed with
that: `nohole` (baseline), `eg` (endgame-defection penalty), `inf` (round count
scrubbed). This reads the step-35 replays and asks whether the grim-trained and
the tft-trained policy are behaviourally different.

The statistic that answers that question is in `crossplay.trained_vs_contrast`:
hold the opponent BEING PLAYED fixed and difference the two training opponents.
Everything else in this file either sets that up or fails to answer it, and the
`_caveat` fields say which.

ERROR BARS. Every SE in this file is BETWEEN TRAINING SEED: each checkpoint is
collapsed to one number over its episode seeds first, and the spread is taken
across checkpoints. Pooling episode seeds treats 8 rollouts of one LoRA as 8
independent draws, which is what produced the sign flip in
`0826-endgame-by-opponent.md` section 4 that three seeds later contradicted.
Fewer than 2 seeds gets `se: null`, never `se: 0`.
"""

from __future__ import annotations

import argparse
import collections
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent

B_CROSSPLAY = ROOT / "hole_exp/results/think4_evals/B_crossplay.jsonl"
A_LENGTH = ROOT / "hole_exp/results/think4_evals/A_endgame_length.jsonl"
C_TRACES = ROOT / "results/0830_endgame_traces/trace_blocks.jsonl"
D_DIR = ROOT / "hole_exp/results/eval_grimtft_expanded"

INVALID_MAX = 0.25
FOUR_ARMS = ("grim/nohole", "grim/eg", "tft/nohole", "tft/eg")
FLAGGED_CELL = ("grim/nohole", 1)
MARKERS = (
    "m_shaping_awareness",
    "m_endgame_hold",
    "m_endgame_defect_plan",
    "m_backward_induction",
    "m_in_game_penalty",
    "m_notices_unknown",
    "m_assumes_finite",
    "m_infinite_logic",
)


# ---------------------------------------------------------------- primitives


def read_jsonl(path: Path) -> list[dict]:
    with path.open() as fh:
        return [json.loads(line) for line in fh if line.strip()]


def file_meta(path: Path) -> dict:
    st = path.stat()
    return {
        "path": str(path),
        "bytes": st.st_size,
        "mtime_utc": datetime.fromtimestamp(st.st_mtime, timezone.utc).isoformat(),
    }


def between_seed(per_seed: dict[Any, float | None], **extra: Any) -> dict:
    """Mean and SE across TRAINING SEEDS of already-collapsed per-seed values."""
    items = sorted((s, v) for s, v in per_seed.items() if v is not None)
    vals = np.array([v for _, v in items], dtype=float)
    n = len(vals)
    out: dict[str, Any] = {
        "mean": float(vals.mean()) if n else None,
        "se": float(vals.std(ddof=1) / math.sqrt(n)) if n >= 2 else None,
        "n_seeds": n,
        "per_seed": {str(s): round(float(v), 6) for s, v in items},
    }
    out.update(extra)
    return out


def unpaired_diff(a: dict, b: dict) -> dict:
    """a - b where the two sides are different checkpoints, so SE adds in quadrature."""
    if a["mean"] is None or b["mean"] is None:
        return {"delta": None, "se": None, "n_seeds_a": a["n_seeds"], "n_seeds_b": b["n_seeds"]}
    se = None
    if a["se"] is not None and b["se"] is not None:
        se = float(math.hypot(a["se"], b["se"]))
    return {
        "delta": float(a["mean"] - b["mean"]),
        "se": se,
        "se_basis": "sqrt(se_a^2 + se_b^2); seeds are NOT paired across arms",
        "mean_a": a["mean"],
        "mean_b": b["mean"],
        "se_a": a["se"],
        "se_b": b["se"],
        "n_seeds_a": a["n_seeds"],
        "n_seeds_b": b["n_seeds"],
    }


def seed_collapse(
    rows: Iterable[dict],
    value: Callable[[dict], float | None],
    seed_key: str = "train_seed",
) -> tuple[dict[Any, float | None], dict[Any, int]]:
    """Mean of `value` within each training seed, skipping rows where it is undefined."""
    acc: dict[Any, list[float]] = collections.defaultdict(list)
    seen: dict[Any, int] = collections.Counter()
    for row in rows:
        seen[row[seed_key]] += 1
        v = value(row)
        if v is not None:
            acc[row[seed_key]].append(float(v))
    per_seed = {s: (float(np.mean(vs)) if vs else None) for s, vs in acc.items()}
    for s in seen:
        per_seed.setdefault(s, None)
    n_used = {s: len(vs) for s, vs in acc.items()}
    return per_seed, n_used


def stat(rows: Sequence[dict], value: Callable[[dict], float | None], denom_label: str) -> dict:
    per_seed, n_used = seed_collapse(rows, value)
    return between_seed(
        per_seed,
        n_episodes=len(rows),
        n_episodes_defined=sum(n_used.values()),
        n_episodes_per_seed={str(s): n for s, n in sorted(collections.Counter(r["train_seed"] for r in rows).items())},
        denominator=denom_label,
    )


# ------------------------------------------------------- derived per-episode


def no_defection(row: dict) -> bool:
    return row.get("first_defect_index") is None


def fdi_given_defect(row: dict) -> float | None:
    """first_defect_index, left UNDEFINED when the episode never defected."""
    return None if no_defection(row) else float(row["first_defect_index"])


def any_defect(row: dict) -> float:
    return 0.0 if no_defection(row) else 1.0


def defect_before_last(row: dict) -> float:
    """Defection with at least one round left for the opponent to punish in.

    A final-round defection gives neither grim nor tft a round in which to
    retaliate, so it cannot discriminate the two opponents.
    """
    if no_defection(row):
        return 0.0
    return 1.0 if row["first_defect_index"] < row["n_decisions"] - 1 else 0.0


def rounds_before_end(row: dict) -> float | None:
    if no_defection(row):
        return None
    return float(row["n_decisions"] - 1 - row["first_defect_index"])


# ------------------------------------------------------------ A: crossplay

CROSS_METRICS = ("exploit_rate", "endgame_rate", "first_defect_index", "capture", "payoff")


def crossplay_cell(rows: Sequence[dict]) -> dict:
    out: dict[str, Any] = {}
    for m in ("exploit_rate", "endgame_rate", "capture", "payoff"):
        out[m] = stat(rows, lambda r, m=m: r.get(m), "episodes in cell (per-seed mean first)")
    out["first_defect_index_given_defect"] = stat(
        rows, fdi_given_defect, "episodes in cell WITH a defection (no-defect episodes excluded, not imputed)"
    )
    out["frac_any_defect"] = stat(rows, any_defect, "episodes in cell")
    out["frac_defect_before_last"] = stat(rows, defect_before_last, "episodes in cell")
    out["invalid_rate"] = stat(rows, lambda r: r.get("invalid_rate"), "episodes in cell")
    out["n_decisions_per_episode"] = sorted({r["n_decisions"] for r in rows})
    return out


def build_crossplay(rows_raw: Sequence[dict]) -> tuple[dict, dict]:
    dropped = [r for r in rows_raw if r.get("invalid_rate", 0.0) > INVALID_MAX]
    rows = [r for r in rows_raw if r.get("invalid_rate", 0.0) <= INVALID_MAX]

    by_arm_plays: dict[str, dict] = {}
    for (arm, plays), grp in sorted(
        _group(rows, lambda r: (r["arm"], r["plays"])).items()
    ):
        by_arm_plays[f"{arm}|plays={plays}"] = {
            "arm": arm,
            "trained_vs": grp[0]["trained_vs"],
            "plays": plays,
            "diagonal": plays == grp[0]["trained_vs"],
            "horizon": sorted({r["horizon"] for r in grp}),
            **crossplay_cell(grp),
        }

    # paired within checkpoint: off-diagonal minus on-diagonal
    off_minus_on: dict[str, dict] = {}
    for arm, grp in sorted(_group(rows, lambda r: r["arm"]).items()):
        trained_vs = grp[0]["trained_vs"]
        on = [r for r in grp if r["plays"] == trained_vs]
        off = [r for r in grp if r["plays"] != trained_vs]
        entry: dict[str, Any] = {
            "arm": arm,
            "trained_vs": trained_vs,
            "plays_on": trained_vs,
            "plays_off": sorted({r["plays"] for r in off}),
            "_pairing": "paired within checkpoint: per-seed off mean minus per-seed on mean",
        }
        for label, fn in _cross_value_fns().items():
            on_seed, _ = seed_collapse(on, fn)
            off_seed, _ = seed_collapse(off, fn)
            per_seed = {
                s: (off_seed[s] - on_seed[s])
                for s in sorted(set(on_seed) & set(off_seed))
                if on_seed[s] is not None and off_seed[s] is not None
            }
            entry[label] = between_seed(
                per_seed,
                n_episodes_on=len(on),
                n_episodes_off=len(off),
                denominator="training seeds with both cells defined",
            )
        off_minus_on[arm] = entry

    # THE statistic: hold `plays` fixed, difference the training opponent.
    contrast: dict[str, Any] = {
        "_what": (
            "grim_trained_minus_tft_trained with the PLAYED opponent held fixed. This is the "
            "only contrast in the file that separates the policy from the environment it is in."
        ),
        "_pairing": "UNPAIRED. train_seed 0/1/2 index different checkpoints in the grim and tft arms.",
        "_only_nohole_and_eg": (
            "inf is absent: grim/inf was never crossplayed and tft/inf has a single train seed, so "
            "no contrast is possible. See by_arm_plays for the tft/inf cells themselves."
        ),
    }
    for cond in ("nohole", "eg"):
        cond_out: dict[str, Any] = {}
        for plays in ("grim", "tft"):
            g = [r for r in rows if r["arm"] == f"grim/{cond}" and r["plays"] == plays]
            t = [r for r in rows if r["arm"] == f"tft/{cond}" and r["plays"] == plays]
            if not g or not t:
                continue
            cell: dict[str, Any] = {
                "arm_a": f"grim/{cond}",
                "arm_b": f"tft/{cond}",
                "plays": plays,
                "n_episodes_a": len(g),
                "n_episodes_b": len(t),
                "home_field": (
                    f"grim/{cond} is on-diagonal here" if plays == "grim" else f"tft/{cond} is on-diagonal here"
                ),
            }
            for label, fn in _cross_value_fns().items():
                a = between_seed(seed_collapse(g, fn)[0])
                b = between_seed(seed_collapse(t, fn)[0])
                cell[label] = unpaired_diff(a, b)
            cond_out[f"plays={plays}"] = cell
        contrast[cond] = cond_out

    meta = {
        "rows_read": len(rows_raw),
        "rows_kept": len(rows),
        "rows_dropped_invalid_gt_0.25": len(dropped),
        "dropped_by_checkpoint": {
            f"{a}|s{s}|plays={p}": n
            for (a, s, p), n in sorted(
                collections.Counter((r["arm"], r["train_seed"], r["plays"]) for r in dropped).items()
            )
        },
        "dropped_ckpt_paths": sorted({r["ckpt"] for r in dropped}),
        "arms": {a: n for a, n in sorted(collections.Counter(r["arm"] for r in rows).items())},
        "train_seeds": sorted({r["train_seed"] for r in rows}),
        "episode_seeds": sorted({r["seed"] for r in rows}),
        "steps": sorted({r["step"] for r in rows}),
        "envs": sorted({r["env"] for r in rows}),
    }
    meta["tft_inf_is_degenerate"] = (
        "All 16 tft/inf rows are identically zero on exploit_rate, endgame_rate and capture with "
        "first_defect_index null and payoff exactly 30.0 in every episode: the hidden-horizon arm "
        "never defects once against either opponent. This is the data, not a parsing failure. It is "
        "one train seed (1), so it carries se: null and enters no contrast."
    )
    return {"_meta": meta, "by_arm_plays": by_arm_plays, "off_minus_on": off_minus_on, "trained_vs_contrast": contrast}, {
        "dropped": len(dropped),
        "detail": meta["dropped_by_checkpoint"],
    }


def _cross_value_fns() -> dict[str, Callable[[dict], float | None]]:
    return {
        "exploit_rate": lambda r: r.get("exploit_rate"),
        "endgame_rate": lambda r: r.get("endgame_rate"),
        "capture": lambda r: r.get("capture"),
        "payoff": lambda r: r.get("payoff"),
        "first_defect_index_given_defect": fdi_given_defect,
        "frac_any_defect": any_defect,
        "frac_defect_before_last": defect_before_last,
    }


def _group(rows: Iterable[dict], key: Callable[[dict], Any]) -> dict[Any, list[dict]]:
    out: dict[Any, list[dict]] = collections.defaultdict(list)
    for r in rows:
        out[key(r)].append(r)
    return dict(out)


# --------------------------------------------------------- B: endgame length


def hazard(rows: Sequence[dict]) -> dict:
    """Per-round defection hazard as a function of rounds_from_end (0 = final round).

    Per training seed first: at each rounds_from_end, the share of that seed's
    episodes whose defect_indices contain the matching decision index.
    """
    per_rfe: dict[int, dict[Any, list[float]]] = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in rows:
        nd = r["n_decisions"]
        di = set(r["defect_indices"])
        for i in range(nd):
            per_rfe[nd - 1 - i][r["train_seed"]].append(1.0 if i in di else 0.0)
    out: dict[str, Any] = {}
    for rfe in sorted(per_rfe):
        per_seed = {s: float(np.mean(v)) for s, v in per_rfe[rfe].items()}
        n_dec = sum(len(v) for v in per_rfe[rfe].values())
        out[str(rfe)] = between_seed(
            per_seed, n_decisions=n_dec, denominator="episodes reaching this rounds_from_end, per seed then across seeds"
        )
    return out


def length_cell(rows: Sequence[dict]) -> dict:
    n_turns = sum(len(r["turns"]) for r in rows)
    n_dec = sum(r["n_decisions"] for r in rows)
    n_empty = sum(r["n_empty_answer"] for r in rows)
    out: dict[str, Any] = {
        "n_episodes": len(rows),
        "n_decisions_total": n_dec,
        "n_turns_total": n_turns,
        "n_empty_answer_total": n_empty,
        "empty_answer_per_decision": (n_empty / n_dec) if n_dec else None,
        "empty_answer_per_turn": (n_empty / n_turns) if n_turns else None,
        "_empty_answer_note": (
            "n_empty_answer counts ALL turns, not only decision turns, so the per-decision "
            "ratio can exceed 1. invalid_rate is blind to this failure mode."
        ),
    }
    out["first_defect_index_given_defect"] = stat(
        rows, fdi_given_defect, "episodes WITH a defection (no-defect episodes excluded, not imputed)"
    )
    out["rounds_before_end_given_defect"] = stat(
        rows, rounds_before_end, "episodes WITH a defection; = n_decisions - 1 - first_defect_index"
    )
    out["frac_any_defect"] = stat(rows, any_defect, "episodes in cell")
    out["frac_defect_before_last"] = stat(rows, defect_before_last, "episodes in cell")
    for m in ("endgame_rate", "exploit_rate", "capture", "invalid_rate"):
        out[m] = stat(rows, lambda r, m=m: r.get(m), "episodes in cell")
    return out


def _slope(xs: Sequence[float], ys: Sequence[float]) -> float | None:
    if len(xs) < 2:
        return None
    return float(np.polyfit(np.asarray(xs, float), np.asarray(ys, float), 1)[0])


def build_length(rows: Sequence[dict], drop_flagged: bool) -> dict:
    rows = [r for r in rows if r["arm"] in FOUR_ARMS]
    if drop_flagged:
        rows = [r for r in rows if (r["arm"], r["train_seed"]) != FLAGGED_CELL]

    by_cell: dict[str, Any] = {}
    for (arm, nr), grp in sorted(_group(rows, lambda r: (r["arm"], r["num_rounds"])).items()):
        by_cell[f"{arm}|N={nr}"] = {"arm": arm, "num_rounds": nr, **length_cell(grp)}

    by_arm: dict[str, Any] = {}
    for arm, grp in sorted(_group(rows, lambda r: r["arm"]).items()):
        by_arm[arm] = {
            "arm": arm,
            "opponent": grp[0]["opponent"],
            "num_rounds_present": sorted({r["num_rounds"] for r in grp}),
            "pooled_over_lengths": length_cell(grp),
            "hazard_by_rounds_from_end_pooled": hazard(grp),
            "hazard_by_rounds_from_end_by_length": {
                f"N={nr}": hazard(sub) for nr, sub in sorted(_group(grp, lambda r: r["num_rounds"]).items())
            },
        }

    # slope of mean first_defect_index against num_rounds: 0 = fixed memorised
    # position, +1 = tracks the true final round.
    slopes: dict[str, Any] = {}
    for arm, grp in sorted(_group(rows, lambda r: r["arm"]).items()):
        per_seed: dict[Any, float | None] = {}
        for seed, sgrp in _group(grp, lambda r: r["train_seed"]).items():
            pts = []
            for nr, cell in sorted(_group(sgrp, lambda r: r["num_rounds"]).items()):
                vals = [fdi_given_defect(r) for r in cell]
                vals = [v for v in vals if v is not None]
                if vals:
                    pts.append((float(nr), float(np.mean(vals))))
            per_seed[seed] = _slope([p[0] for p in pts], [p[1] for p in pts]) if len(pts) >= 2 else None
        pooled_pts = []
        for nr, cell in sorted(_group(grp, lambda r: r["num_rounds"]).items()):
            vals = [v for v in (fdi_given_defect(r) for r in cell) if v is not None]
            if vals:
                pooled_pts.append((float(nr), float(np.mean(vals))))
        slopes[arm] = {
            "per_seed_slope": between_seed(per_seed, denominator="training seeds with >=2 usable lengths"),
            "pooled_slope": _slope([p[0] for p in pooled_pts], [p[1] for p in pooled_pts]),
            "pooled_points_num_rounds_to_mean_fdi": {str(int(x)): y for x, y in pooled_pts},
            "_reading": "0 == memorised a fixed absolute position; +1 == tracks the true final round",
        }

    empty_by_seed: dict[str, Any] = {}
    for (arm, seed), grp in sorted(_group(rows, lambda r: (r["arm"], r["train_seed"])).items()):
        n_dec = sum(r["n_decisions"] for r in grp)
        n_turns = sum(len(r["turns"]) for r in grp)
        n_empty = sum(r["n_empty_answer"] for r in grp)
        empty_by_seed[f"{arm}|s{seed}"] = {
            "n_episodes": len(grp),
            "n_empty_answer": n_empty,
            "n_decisions": n_dec,
            "n_turns": n_turns,
            "per_decision": n_empty / n_dec if n_dec else None,
            "per_turn": n_empty / n_turns if n_turns else None,
            "mean_invalid_rate": float(np.mean([r["invalid_rate"] for r in grp])),
        }

    return {
        "n_episodes": len(rows),
        "train_seeds": sorted({r["train_seed"] for r in rows}),
        "by_arm": by_arm,
        "by_arm_length": by_cell,
        "first_defect_index_slope_vs_num_rounds": slopes,
        "empty_answer_by_arm_seed": empty_by_seed,
    }


# ------------------------------------------------------- C: reasoning markers


def marker_cell(rows: Sequence[dict]) -> dict:
    out: dict[str, Any] = {
        "n_blocks": len(rows),
        "n_decision_blocks": sum(1 for r in rows if r["in_decision"]),
        "n_episodes": len({(r["arm"], r["train_seed"], r["num_rounds"], r["episode_seed"]) for r in rows}),
    }
    for m in MARKERS:
        out[m] = stat(rows, lambda r, m=m: float(r[m]), "reasoning blocks in cell (per-seed mean first)")
    out["n_chars"] = stat(rows, lambda r: float(r["n_chars"]), "reasoning blocks in cell")
    out["n_words"] = stat(rows, lambda r: float(r["n_words"]), "reasoning blocks in cell")
    dec = [r for r in rows if r["in_decision"]]
    out["decision_blocks_only"] = {
        m: stat(dec, lambda r, m=m: float(r[m]), "decision-turn reasoning blocks") for m in MARKERS
    }
    out["decision_blocks_only"]["n_chars"] = stat(dec, lambda r: float(r["n_chars"]), "decision-turn blocks")
    return out


def build_markers(rows_raw: Sequence[dict]) -> dict:
    rows = [r for r in rows_raw if r["arm"] in FOUR_ARMS]
    by_arm: dict[str, Any] = {}
    for arm, grp in sorted(_group(rows, lambda r: r["arm"]).items()):
        by_arm[arm] = {"arm": arm, "opponent": grp[0]["opponent"], "condition": grp[0]["condition"], **marker_cell(grp)}

    contrast: dict[str, Any] = {
        "_what": (
            "grim_trained_minus_tft_trained on reasoning markers, with the played opponent NOT "
            "held fixed -- this file is diagonal-only, so arm and opponent move together and "
            "any difference is policy+environment confounded."
        ),
        "_pairing": "UNPAIRED across arms; SE = sqrt(se_a^2 + se_b^2)",
    }
    for cond in ("nohole", "eg"):
        g = [r for r in rows if r["arm"] == f"grim/{cond}"]
        t = [r for r in rows if r["arm"] == f"tft/{cond}"]
        if not g or not t:
            continue
        cell: dict[str, Any] = {"arm_a": f"grim/{cond}", "arm_b": f"tft/{cond}"}
        for m in list(MARKERS) + ["n_chars"]:
            fn: Callable[[dict], float | None] = lambda r, m=m: float(r[m])
            cell[m] = unpaired_diff(between_seed(seed_collapse(g, fn)[0]), between_seed(seed_collapse(t, fn)[0]))
        contrast[cond] = cell

    return {
        "_headline_marker": "m_shaping_awareness -- the marker most likely to show opponent modelling if anything does",
        "n_blocks_read": len(rows_raw),
        "n_blocks_kept": len(rows),
        "arms_kept": sorted({r["arm"] for r in rows}),
        "by_arm": by_arm,
        "trained_vs_contrast": contrast,
    }


# --------------------------------------------------- D: expanded grim/tft eval


def build_expanded() -> dict:
    out: dict[str, Any] = {
        "unusable_as_matched_pair": (
            "DO NOT read any grim_trained vs tft_trained difference here as an opponent effect. "
            "grim_trained is mixed_think3_nohole-think-grim_d1_s0_inf-step0040: the HIDDEN-HORIZON "
            "(inf) arm at step 40. tft_trained is mixed_think3_nohole-think-tft_d1_s0-step0030: the "
            "BASELINE (nohole) arm at step 30. The two differ in training opponent, in manipulation "
            "(inf vs nohole) and in training step simultaneously, and both are think3-generation, not "
            "the think4 wave analysed everywhere else in this cache. One seed each, so no error bar. "
            "The numbers are cached only so the write-up can explicitly rule this comparison out."
        ),
        "checkpoints": {},
        "by_run": {},
    }
    for name in ("base", "grim_trained", "tft_trained"):
        path = D_DIR / name
        doc = json.loads((path.with_suffix(".json")).read_text())
        out["checkpoints"][name] = doc.get("source")
        out["by_run"][name] = {
            "source": doc.get("source"),
            "seeds": doc.get("seeds"),
            "envs": {
                r["env"]: {
                    "exploit_rate": r.get("exploit_rate"),
                    "capture": r.get("capture"),
                    "payoff": r.get("payoff"),
                    "invalid_rate": r.get("invalid_rate"),
                    "episodes": r.get("episodes"),
                    "decisions": r.get("decisions"),
                    "se": None,
                }
                for r in doc["rows"]
            },
            "_se": "null: one checkpoint per run, no between-seed spread available",
        }
    return out


# ------------------------------------------------------------------- verdict


def verdict(contrast: dict) -> dict:
    """Auto-derived answer: how far, in its own SE, is any held-fixed contrast from zero?"""
    rows = []
    for cond in ("nohole", "eg"):
        for pk, cell in contrast.get(cond, {}).items():
            for metric, d in cell.items():
                if not isinstance(d, dict) or d.get("delta") is None or d.get("se") in (None, 0.0):
                    continue
                pinned = [
                    side for side, key in (("a", "se_a"), ("b", "se_b")) if d.get(key) == 0.0
                ]
                rows.append(
                    {
                        "condition": cond,
                        "plays": pk,
                        "metric": metric,
                        "delta": d["delta"],
                        "se": d["se"],
                        "abs_z": abs(d["delta"]) / d["se"],
                        "zero_variance_side": pinned or None,
                        "_ceiling_caveat": (
                            "One side has zero between-seed variance (every seed identical, e.g. pinned "
                            "at 1.0), so the quadrature SE carries only the other arm's spread and "
                            "understates the true uncertainty. Read this |z| as optimistic."
                        )
                        if pinned
                        else None,
                    }
                )
    rows.sort(key=lambda r: -r["abs_z"])
    n_over_2 = sum(1 for r in rows if r["abs_z"] >= 2.0)
    return {
        "_question": "Do the grim-trained and tft-trained policies differ when the played opponent is held fixed?",
        "n_contrasts_tested": len(rows),
        "n_over_2se": n_over_2,
        "n_over_2se_with_both_sides_varying": sum(
            1 for r in rows if r["abs_z"] >= 2.0 and r["zero_variance_side"] is None
        ),
        "n_over_1se": sum(1 for r in rows if r["abs_z"] >= 1.0),
        "largest_abs_z": rows[0] if rows else None,
        "ranked_top": rows[:6],
        "_reading": (
            "With three training seeds per arm the between-seed SE is the honest scale. If no "
            "contrast reaches 2 SE, the crossplay data does not detect a policy difference and the "
            "resolvable claim is an upper bound on the effect, not an effect."
        ),
    }


# ------------------------------------------------------------------- reporting


def fmt(entry: dict | None, digits: int = 3) -> str:
    if entry is None or entry.get("mean") is None and entry.get("delta") is None:
        return "     n/a"
    val = entry.get("mean", entry.get("delta"))
    se = entry.get("se")
    n = entry.get("n_seeds", entry.get("n_seeds_a"))
    body = f"{val:+.{digits}f}" if entry.get("delta") is not None else f"{val:.{digits}f}"
    tail = f" +- {se:.{digits}f}" if se is not None else " +-   null"
    return f"{body}{tail} (n={n})"


def summarise(cache: dict) -> None:
    p = print
    p("=" * 96)
    p("EVAL CACHE  step-35 frozen adapters  think4  grim vs tft")
    p("=" * 96)

    cx = cache["crossplay"]
    p("\n[B] CROSSPLAY 2x2  (n_decisions=10, finite horizon unless noted)")
    p(f"  rows read {cx['_meta']['rows_read']}  kept {cx['_meta']['rows_kept']}  "
      f"dropped invalid_rate>0.25: {cx['_meta']['rows_dropped_invalid_gt_0.25']}")
    for k, v in cx["_meta"]["dropped_by_checkpoint"].items():
        p(f"    dropped {v:>2}  {k}")
    p(f"\n  {'arm | plays':<26}{'exploit':>22}{'endgame':>22}{'fdi|defect':>22}{'any defect':>22}{'defect<last':>22}")
    for key, cell in cx["by_arm_plays"].items():
        mark = "*" if cell["diagonal"] else " "
        p(f"  {mark}{key:<25}{fmt(cell['exploit_rate']):>22}{fmt(cell['endgame_rate']):>22}"
          f"{fmt(cell['first_defect_index_given_defect'], 2):>22}{fmt(cell['frac_any_defect']):>22}"
          f"{fmt(cell['frac_defect_before_last']):>22}")
    p("    (* = on-diagonal: plays the opponent it trained against)")

    p(f"\n  PAIRED off-diagonal minus on-diagonal (within checkpoint)")
    p(f"  {'arm':<26}{'exploit':>22}{'endgame':>22}{'capture':>22}{'payoff':>22}")
    for arm, cell in cx["off_minus_on"].items():
        p(f"  {arm:<26}{fmt(cell['exploit_rate']):>22}{fmt(cell['endgame_rate']):>22}"
          f"{fmt(cell['capture']):>22}{fmt(cell['payoff'], 2):>22}")

    p("\n" + "-" * 96)
    p("  THE QUESTION: hold `plays` FIXED, difference the TRAINING opponent")
    p("  grim_trained minus tft_trained.  UNPAIRED, SE = sqrt(se_a^2+se_b^2).")
    p("-" * 96)
    for cond in ("nohole", "eg"):
        p(f"\n  condition = {cond}")
        p(f"  {'plays':<12}{'exploit':>22}{'endgame':>22}{'fdi|defect':>22}{'any defect':>22}{'defect<last':>22}{'capture':>22}")
        for pk, cell in cx["trained_vs_contrast"].get(cond, {}).items():
            p(f"  {pk:<12}{fmt(cell['exploit_rate']):>22}{fmt(cell['endgame_rate']):>22}"
              f"{fmt(cell['first_defect_index_given_defect'], 2):>22}{fmt(cell['frac_any_defect']):>22}"
              f"{fmt(cell['frac_defect_before_last']):>22}{fmt(cell['capture']):>22}")

    v = cx["verdict"]
    p(f"\n  VERDICT  {v['n_over_2se']} of {v['n_contrasts_tested']} held-fixed contrasts reach 2 SE "
      f"({v['n_over_2se_with_both_sides_varying']} with both sides varying), {v['n_over_1se']} reach 1 SE.")
    for r in v["ranked_top"][:4]:
        flag = "  CEILING: one side has zero seed variance" if r["zero_variance_side"] else ""
        p(f"    |z|={r['abs_z']:.2f}  {r['condition']:<7}{r['plays']:<12}{r['metric']:<28}"
          f"{r['delta']:+.4f} +- {r['se']:.4f}{flag}")

    p("\n[A] ENDGAME LENGTH  N in {6,10,14}, DIAGONAL ONLY, arms {grim,tft}x{nohole,eg}")
    for variant in ("all_seeds", "excl_grim_nohole_s1"):
        el = cache["endgame_length"][variant]
        p(f"\n  --- {variant}  ({el['n_episodes']} episodes, seeds {el['train_seeds']})")
        p(f"  {'arm | N':<22}{'fdi|defect':>20}{'before end':>20}{'any defect':>20}{'defect<last':>20}{'endgame':>20}")
        for key, cell in el["by_arm_length"].items():
            p(f"  {key:<22}{fmt(cell['first_defect_index_given_defect'], 2):>20}"
              f"{fmt(cell['rounds_before_end_given_defect'], 2):>20}{fmt(cell['frac_any_defect']):>20}"
              f"{fmt(cell['frac_defect_before_last']):>20}{fmt(cell['endgame_rate']):>20}")
        p(f"\n  {'arm':<22}{'slope fdi~N':>26}{'pooled':>10}   empty-answer/decision")
        for arm, sl in el["first_defect_index_slope_vs_num_rounds"].items():
            pooled = sl["pooled_slope"]
            ea = el["by_arm"][arm]["pooled_over_lengths"]["empty_answer_per_decision"]
            p(f"  {arm:<22}{fmt(sl['per_seed_slope'], 3):>26}{pooled:>10.3f}   {ea:.3f}")
        p("\n  hazard by rounds_from_end (0 = final round), pooled over lengths")
        rfes = ["0", "1", "2", "3", "4", "5"]
        p(f"  {'arm':<22}" + "".join(f"{'rfe=' + r:>13}" for r in rfes))
        for arm, cell in el["by_arm"].items():
            hz = cell["hazard_by_rounds_from_end_pooled"]
            row = "".join(
                f"{(hz[r]['mean'] if r in hz and hz[r]['mean'] is not None else float('nan')):>13.3f}" for r in rfes
            )
            p(f"  {arm:<22}{row}")

    p("\n  empty-answer screen (invalid_rate is blind to this):")
    for k, v in cache["endgame_length"]["all_seeds"]["empty_answer_by_arm_seed"].items():
        flag = "  <== COMPROMISED" if v["per_decision"] > 0.5 else ""
        p(f"    {k:<22} empty/dec {v['per_decision']:.3f}  empty/turn {v['per_turn']:.3f}  "
          f"invalid {v['mean_invalid_rate']:.3f}{flag}")

    p("\n[C] REASONING MARKERS  (diagonal only, arm and opponent move together)")
    rm = cache["reasoning_markers"]
    p(f"  {'arm':<16}{'shaping_aware':>22}{'endgame_plan':>22}{'backward_ind':>22}{'n_chars':>22}")
    for arm, cell in rm["by_arm"].items():
        p(f"  {arm:<16}{fmt(cell['m_shaping_awareness']):>22}{fmt(cell['m_endgame_defect_plan']):>22}"
          f"{fmt(cell['m_backward_induction']):>22}{fmt(cell['n_chars'], 1):>22}")
    for cond in ("nohole", "eg"):
        c = rm["trained_vs_contrast"].get(cond)
        if not c:
            continue
        p(f"\n  grim/{cond} minus tft/{cond} (CONFOUNDED with opponent played):")
        p(f"    m_shaping_awareness {fmt(c['m_shaping_awareness'])}")
        p(f"    m_endgame_defect_plan {fmt(c['m_endgame_defect_plan'])}")
        p(f"    n_chars {fmt(c['n_chars'], 1)}")

    p("\n[D] eval_grimtft_expanded  -- NOT A MATCHED PAIR")
    ex = cache["eval_grimtft_expanded"]
    for name, ck in ex["checkpoints"].items():
        p(f"    {name:<14} {ck}")
    p(f"  {'env':<12}{'base expl':>12}{'grim expl':>12}{'tft expl':>12}{'base cap':>12}{'grim cap':>12}{'tft cap':>12}")
    for env in ("ipd", "ipd3", "staghunt", "winasmuch"):
        vals = [ex["by_run"][n]["envs"][env] for n in ("base", "grim_trained", "tft_trained")]
        p(f"  {env:<12}" + "".join(f"{v['exploit_rate']:>12.3f}" for v in vals)
          + "".join(f"{v['capture']:>12.3f}" for v in vals))
    p("  ^ uninterpretable as an opponent effect: different arm, manipulation AND step.")
    p("\n" + "=" * 96)


# ------------------------------------------------------------------- assembly


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--outdir", type=Path, default=HERE)
    args = ap.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)

    b_rows = read_jsonl(B_CROSSPLAY)
    a_rows = read_jsonl(A_LENGTH)
    c_rows = read_jsonl(C_TRACES)

    crossplay, cross_drop = build_crossplay(b_rows)
    crossplay["verdict"] = verdict(crossplay["trained_vs_contrast"])

    a_four = [r for r in a_rows if r["arm"] in FOUR_ARMS]
    a_kept = [r for r in a_four if r.get("invalid_rate", 0.0) <= INVALID_MAX]
    a_dropped = [r for r in a_four if r.get("invalid_rate", 0.0) > INVALID_MAX]

    endgame_length = {
        "_restriction": (
            "arms grim/nohole, grim/eg, tft/nohole, tft/eg only. grim/inf has NO episodes in this "
            "file, and the 96 tft/inf rows are a known-contaminated second copy of a single train "
            "seed (train_seed 1, 32 rows per length where every other cell has 16) -- see "
            "results/0830_endgame_traces/README.md. Excluding `inf` sidesteps both problems."
        ),
        "_diagonal_only": (
            "Every row satisfies opponent == arm.split('/')[0], verified on all 672 rows. Each arm "
            "plays ONLY the opponent it trained against, so this file cannot separate the policy "
            "from the environment. It can only characterise each arm in its own condition. The "
            "policy-vs-environment separation lives in crossplay.trained_vs_contrast."
        ),
        "_flagged_cell": (
            "grim/nohole train_seed 1 emits an empty decision answer on the majority of turns while "
            "its invalid_rate reads 0.000, so the repo's gate does not see it. Every statistic is "
            "computed twice: `all_seeds` and `excl_grim_nohole_s1`."
        ),
        "all_seeds": build_length(a_kept, drop_flagged=False),
        "excl_grim_nohole_s1": build_length(a_kept, drop_flagged=True),
    }

    reasoning = build_markers(c_rows)
    reasoning["_staleness"] = (
        "trace_blocks.jsonl was generated from 624 of the now-672 A rows and is therefore slightly "
        "stale relative to A_endgame_length.jsonl."
    )
    reasoning["_diagonal_only"] = endgame_length["_diagonal_only"]

    n_dec_b = sum(r["n_decisions"] for r in b_rows)
    n_dec_a = sum(r["n_decisions"] for r in a_four)

    meta = {
        "_what": "Frozen step-35 checkpoint evidence on whether grim-trained and tft-trained policies differ.",
        "built_utc": datetime.now(timezone.utc).isoformat(),
        "built_by": str(Path(__file__).resolve()),
        "command": "/home/allie/venvs/tinker-ipd/bin/python build_eval_cache.py",
        "wave": "think4, Qwen3.8-27B LoRA, step 35 adapters replayed",
        "error_bars": (
            "EVERY SE in this file is BETWEEN TRAINING SEED: each checkpoint is collapsed to one "
            "number over its episode seeds first, then the spread is taken across checkpoints "
            "(sample std, ddof=1, divided by sqrt(n_seeds)). Pooling episode seeds treats 8 "
            "rollouts of one LoRA as 8 independent draws; that is what produced the sign flip in "
            "0826-endgame-by-opponent.md section 4 which three seeds later contradicted. Cells with "
            "fewer than 2 seeds carry se: null, never se: 0. Differences taken WITHIN a checkpoint "
            "are paired and get the SE of the per-seed difference; differences taken ACROSS arms "
            "are unpaired (train_seed 0/1/2 index different checkpoints in the grim and tft arms) "
            "and get sqrt(se_a^2 + se_b^2)."
        ),
        "first_defect_index_convention": {
            "no_defection_sentinel": "None (JSON null)",
            "verified": (
                "B_crossplay.jsonl: 36 of 208 rows have first_defect_index == null; the non-null "
                "values are ints in {0,6,7,8,9}. A_endgame_length.jsonl: 230 of 672 rows are null, "
                "and null coincides exactly with defect_indices == [] on all 672 rows (no row is "
                "null with a non-empty defect_indices and none is non-null with an empty one). "
                "There is no -1 and no absent key anywhere in either file."
            ),
            "handling": (
                "No-defection episodes are EXCLUDED from every mean of first_defect_index, which is "
                "therefore reported as `first_defect_index_given_defect` -- conditional on the "
                "episode defecting at all. The censoring itself is reported separately as "
                "`frac_any_defect`, so nothing is imputed and no sentinel enters an average. "
                "`frac_defect_before_last` counts a no-defection episode as 0."
            ),
            "defect_before_last": (
                "first_defect_index is not None AND first_defect_index < n_decisions - 1. A "
                "final-round defection gives neither grim nor tft a round in which to punish, so "
                "it cannot discriminate the two opponents; this statistic drops it."
            ),
        },
        "exclusions": {
            "gate": f"invalid_rate > {INVALID_MAX} (repo convention)",
            "B_crossplay": cross_drop,
            "A_endgame_length": {
                "dropped": len(a_dropped),
                "detail": {
                    f"{r['arm']}|s{r['train_seed']}|N={r['num_rounds']}|ep{r['seed']}": r["invalid_rate"]
                    for r in a_dropped
                },
                "ckpt_paths": sorted({r["ckpt"] for r in a_dropped}),
                "also_excluded_by_restriction": len(a_rows) - len(a_four),
            },
            "empty_answer_caveat": (
                "invalid_rate counts actions the environment had to substitute and is blind to turns "
                "that produced no answer text. n_empty_answer is therefore reported per cell and per "
                "arm x seed, and every A-file statistic is duplicated under excl_grim_nohole_s1."
            ),
        },
        "sources": {
            "B_crossplay": {
                **file_meta(B_CROSSPLAY),
                "rows_read": len(b_rows),
                "n_decisions_total": n_dec_b,
                "role": "the only true 2x2 crossing of trained_vs against plays -- the decisive dataset",
            },
            "A_endgame_length": {
                **file_meta(A_LENGTH),
                "rows_read": len(a_rows),
                "rows_after_arm_restriction": len(a_four),
                "n_decisions_total": n_dec_a,
                "role": "frozen adapters replayed at N=6,10,14 (lengths never trained on); DIAGONAL ONLY",
            },
            "C_trace_blocks": {
                **file_meta(C_TRACES),
                "rows_read": len(c_rows),
                "role": "turn-level reasoning markers; DIAGONAL ONLY and slightly stale (624 of 672 episodes)",
            },
            "D_eval_grimtft_expanded": {
                "dir": str(D_DIR),
                "files": {n: file_meta(D_DIR / f"{n}.json") for n in ("base", "grim_trained", "tft_trained")},
                "role": "cached only so the write-up can rule it out; NOT a matched pair",
            },
        },
        "arms": {
            "grim": "grim trigger: defects forever after your first defection, never forgives",
            "tft": "tit-for-tat: mirrors your last move, forgives the moment you return to cooperating",
            "nohole": "baseline",
            "eg": "endgame-defection penalty",
            "inf": "round count scrubbed from the prompt",
        },
    }

    cache = {
        "meta": meta,
        "crossplay": crossplay,
        "endgame_length": endgame_length,
        "reasoning_markers": reasoning,
        "eval_grimtft_expanded": build_expanded(),
    }

    out = args.outdir / "eval_strategy.json"
    out.write_text(json.dumps(cache, indent=1))
    summarise(cache)
    print(f"wrote {out}  ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
