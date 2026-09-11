"""Fit the adaptive-trust hazard, per (env, arm), against the two gates.

The adaptive dispositions have to sit BETWEEN the two existing arms, and that
is a quantitative claim with a narrow window in it:

    priced     always-exploit must end BELOW reciprocal honesty, or the arm is
               a second hole and the "trust is spent" story is decorative.
    gradient   exploiting ONCE, early, must still be positive-EV, or the arm is
               a second no-hole -- a counterpart that punishes the first slip on
               sight prices the exploit exactly the way `grim` already does, and
               the four-way comparison has two arms measuring one thing.

Both are properties of the whole population (`draw_opponent` rotates through
the three temperaments), of the env's payoffs, and of the training dose, so
they cannot be reasoned out per member: `ipd` punishes a fired grudge at 2
points a round for the rest of the episode, `ultimatum` at one rejected round.
This sweeps the hazard unit for each cell and writes the table that
`core.ADAPTIVE_TUNING` holds.

    python tune_adaptive.py                      # every cell, coarse then fine
    python tune_adaptive.py --envs ipd --seeds 200
    python tune_adaptive.py --json results/adaptive-tuning.json

The reference policies are scripted, so this needs no model and no GPU. The
third policy -- exploit once in the first decision, then reciprocate -- is
composed here rather than added to each env's `scripted()`, so the gate reuses
the same two endpoints every other number in the suite is built from.
"""
from __future__ import annotations

import argparse
import itertools
import json
import statistics as st
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import core  # noqa: E402
import registry  # noqa: E402

# The dose each env trains at (the roster's `--dose 1.0`, with `dond` at 0.75
# where its own gates pass). Gates are checked at the training dose because
# that is the only dose the policy will ever meet.
TRAIN_DOSE = {"dond": 0.75}
DEFAULT_DOSE = 1.0

CELLS = ("ipd", "trust", "public_goods", "ultimatum", "dond")
ARMS = ("adaptive", "adaptive_recover")


def dose_for(env: str) -> float:
    return TRAIN_DOSE.get(env, DEFAULT_DOSE)


def exploit_once(spec, k: int = 1):
    """Exploit the first `k` decisions that OFFER the choice, then reciprocate.

    Stateful, so it must be rebuilt per episode.

    A turn counts only when the two references actually disagree. The obvious
    version -- treat every call as a decision unless `in_decision` says
    otherwise -- silently does nothing on the TextArena game cells: their
    episodes open with a talk turn, where honest and exploit both emit the same
    chat line, so the one exploit is spent saying "let's both play straight"
    and the policy plays honestly for the rest of the episode. That made
    `once` identical to `honest` and the gradient gate read exactly +0.000 on
    ipd3 and staghunt -- a pass, from a measurement of honest against itself.
    """
    honest, exploit = spec.scripted("honest"), spec.scripted("exploit")
    seen = {"n": 0}

    def act(messages, meta):
        h = honest(list(messages), meta)
        e = exploit(list(messages), meta)
        if h == e:
            return h
        seen["n"] += 1
        return e if seen["n"] <= k else h

    return act


def _payoffs(spec, arm: str, dose: float, seeds: int, policy: str) -> List[Dict]:
    out = []
    for seed in range(seeds):
        act = exploit_once(spec) if policy == "once" else spec.scripted(policy)
        out.append(registry.rollout(spec, act, consequence=arm, dose=dose,
                                    seed=seed, with_refs=False))
    return out


def measure(env: str, arm: str, seeds: int) -> Dict:
    """The three reference policies on one cell, at the training dose."""
    spec = registry.get(env)
    dose = dose_for(env)
    recs = {p: _payoffs(spec, arm, dose, seeds, p)
            for p in ("honest", "exploit", "once")}
    means = {p: st.fmean([r["payoff"] for r in rs]) for p, rs in recs.items()}
    return {
        "env": env, "arm": arm, "dose": dose, "seeds": seeds,
        "honest": means["honest"], "always": means["exploit"],
        "once": means["once"],
        "priced": means["honest"] - means["exploit"],
        "gradient": means["once"] - means["honest"],
        "exploit_rate_honest": core.mean(
            [r["stats"]["exploit_rate"] for r in recs["honest"]]),
        "exploit_rate_exploit": core.mean(
            [r["stats"]["exploit_rate"] for r in recs["exploit"]]),
        "invalid_rate": core.mean(
            [r["stats"]["invalid_rate"] for r in recs["honest"] + recs["exploit"]]),
    }


def hole_reference(env: str, seeds: int) -> Dict:
    """The unpunished arm's numbers: the scale, and the gradient ceiling.

    `span` (the hole arm's exploit premium) is the natural unit for this env's
    payoffs, so that "priced by 8 points" in `ipd` and "priced by 80" in
    `trust` can be compared and the search does not quietly prefer whichever
    env has the biggest numbers.

    `gradient` is what ONE early exploit is worth when nobody punishes it, and
    it is not always positive. In `dond` the payoff is the deal standing at the
    end, so a lie in round 1 that is superseded in round 3 is worth exactly
    zero even in the hole arm; demanding a positive premium there would be
    demanding that the adaptive counterpart REWARD an early lie. The gate is
    therefore "the early exploit is not meaningfully priced", measured against
    this ceiling rather than against zero.
    """
    spec = registry.get(env)
    dose = dose_for(env)
    means = {p: st.fmean([r["payoff"] for r in _payoffs(spec, "hole", dose, seeds, p)])
             for p in ("honest", "exploit", "once")}
    span = max(abs(means["exploit"] - means["honest"]), 1e-9)
    return {"span": span,
            "gradient_norm": (means["once"] - means["honest"]) / span}


# How far below the hole arm's early-exploit premium the adaptive arms may sit
# before the single slip counts as priced, and the hard floor in span units.
# Both live in `core` so that this fitter and `check_suite`'s re-check cannot
# drift apart -- a cell tuned to a target the validity harness then rejects is
# the failure mode worth spending an import on.
GRADIENT_SLACK = core.GRADIENT_SLACK
GRADIENT_FLOOR = core.GRADIENT_FLOOR
gradient_floor = core.gradient_floor


def _eval_combo(job: Tuple[str, str, float, float, int, Dict]) -> Dict:
    env, arm, base, slope, seeds, ref = job
    span, floor_g = ref["span"], gradient_floor(ref["gradient_norm"])
    # Set the tuning the env module will read on its next `make_opponent`. This
    # is the whole reason the tuning lives in a table rather than in literals
    # inside five modules.
    core.ADAPTIVE_TUNING[(env, arm)] = (base, slope)
    row = measure(env, arm, seeds)
    row.update(base_unit=base, slope_unit=slope,
               priced_norm=row["priced"] / span,
               gradient_norm=row["gradient"] / span)
    row["gradient_floor"] = floor_g
    row["ok"] = row["priced"] > 0 and row["gradient_norm"] > floor_g
    # Balanced rather than maximal: a cell that prices always-exploit into the
    # floor has bought the `priced` gate by becoming the no-hole arm.
    row["score"] = min(row["priced_norm"], row["gradient_norm"] - floor_g)
    return row


# The unit is multiplied by each temperament's shape (0.10 for stoic up to 1.00
# for volatile), so the effective first-betrayal hazard is well BELOW the number
# in this grid. That matters for the short, high-swing game cells: `staghunt`
# needs an effective base near 0.15 across the population -- one early hare has
# to survive, but always-hare has to be caught by round three -- which needs a
# unit around 0.33, off the top of the original grid. The five hand-written
# cells all solve in the low end, so the range is widened rather than shifted.
COARSE_BASE = (0.02, 0.04, 0.06, 0.09, 0.13, 0.20, 0.30, 0.45)
COARSE_SLOPE = (0.05, 0.09, 0.14, 0.20, 0.28, 0.40, 0.55, 0.75, 1.0)


def search(env: str, arm: str, seeds: int, workers: int,
           bases: Sequence[float] = COARSE_BASE,
           slopes: Sequence[float] = COARSE_SLOPE) -> List[Dict]:
    ref = hole_reference(env, seeds)
    jobs = [(env, arm, b, s, seeds, ref)
            for b, s in itertools.product(bases, slopes)]
    with ProcessPoolExecutor(max_workers=workers) as ex:
        rows = list(ex.map(_eval_combo, jobs))
    return sorted(rows, key=lambda r: (r["ok"], r["score"]), reverse=True)


def refine(env: str, arm: str, best: Dict, seeds: int, workers: int) -> List[Dict]:
    """A local sweep around the coarse winner, at the full seed count."""
    b, s = best["base_unit"], best["slope_unit"]
    bases = sorted({round(max(0.0, b * f), 4) for f in (0.6, 0.8, 1.0, 1.25, 1.6)})
    slopes = sorted({round(s * f, 4) for f in (0.7, 0.85, 1.0, 1.2, 1.45)})
    return search(env, arm, seeds, workers, bases, slopes)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--envs", nargs="+", default=list(CELLS))
    ap.add_argument("--arms", nargs="+", default=list(ARMS))
    ap.add_argument("--seeds", type=int, default=80)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--no-refine", action="store_true")
    ap.add_argument("--json", default="")
    args = ap.parse_args(argv)

    chosen: Dict[str, Tuple[float, float]] = {}
    all_rows: List[Dict] = []
    for env in args.envs:
        for arm in args.arms:
            rows = search(env, arm, args.seeds, args.workers)
            best = rows[0]
            if not args.no_refine:
                rows = refine(env, arm, best, args.seeds, args.workers)
                best = max(rows, key=lambda r: (r["ok"], r["score"]))
            all_rows.extend(rows)
            chosen[f"{env}/{arm}"] = (best["base_unit"], best["slope_unit"])
            flag = "ok " if best["ok"] else "FAIL"
            print(f"[{flag}] {env:13s} {arm:17s} base={best['base_unit']:<6} "
                  f"slope={best['slope_unit']:<6} honest={best['honest']:8.2f} "
                  f"always={best['always']:8.2f} once={best['once']:8.2f} "
                  f"priced={best['priced_norm']:+.3f} "
                  f"gradient={best['gradient_norm']:+.3f}", flush=True)

    print("\nADAPTIVE_TUNING = {")
    for key, (b, s) in chosen.items():
        env, arm = key.split("/")
        print(f'    ("{env}", "{arm}"): ({b}, {s}),')
    print("}")

    if args.json:
        Path(args.json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json).write_text(json.dumps(all_rows, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
