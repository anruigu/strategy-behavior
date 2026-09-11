"""Does the policy CONDITION on the counterpart, or has it just moved its mean?

The regmix arms are scored today by `regime/discrimination`: the pooled
exploit-rate under the nerfed opponent minus the pooled exploit-rate under the
punishing one. That number moves for two different reasons and the run cannot
tell them apart:

  CONDITIONING   the policy reads the counterpart and takes a different action
                 at the same point in the same game. This is the thing the
                 regmix design exists to produce.
  COMPOSITION    the two regimes do not offer the same decision points. Under
                 `nohole` the counterpart retaliates as soon as the learner
                 takes something, which truncates the scored set: later rounds
                 stop being conditional and stop counting. Under `hole` the
                 episode runs its full length. So the two arms are averaging
                 over different denominators, and the pooled gap moves when the
                 MARGINAL exploit rate moves even if the policy conditions on
                 nothing at all. `ipd` is the extreme case -- the always-exploit
                 reference scores one decision where the honest reference scores
                 nine (see core, endgame block).

This module supplies the conditioning half on its own, by comparing the two
regimes only at MATCHED DECISION POINTS.

    stratum = (env, decision index t, number of the learner's own prior
               exploits k)

Everything in a stratum is the same game at the same round with the same
self-history; the only thing that differs across the two regimes inside it is
what the COUNTERPART did in response -- which is exactly the cue. The headline
`cci` is the Mantel-Haenszel weighted average of the within-stratum gaps, i.e.
the pooled gap direct-standardised to a common decision-point distribution.
Composition cancels by construction; what survives is conditioning.

Three companions, because a single number can still be read the wrong way:

  `lor`         the Mantel-Haenszel LOG ODDS RATIO over the same strata. A risk
                DIFFERENCE is mechanically compressed as the marginal rate
                approaches 0 or 1, so an arm that exploits 3% of the time cannot
                post a large `cci` however well it discriminates. The odds ratio
                is not compressed, so the two together separate "conditions
                weakly" from "conditions on a small base".
  `blind_gap`   the gap at the FIRST decision of the episode, where the
                counterpart has not yet responded to anything. Nothing readable
                distinguishes the regimes there beyond the opening line, so this
                is the placebo: `cci` large with `blind_gap` ~ 0 is conditioning
                on the counterpart's behaviour, and both large is a prior
                difference (or a cell whose opening text leaks the arm, which is
                worth knowing).
  `informed_gap` the gap restricted to decisions AFTER the learner has already
                taken something, so the counterpart has had an opportunity to
                punish and the cue is maximally present. The upper bound on what
                the cue can buy.

`cci` is a DIAGNOSTIC and never enters the gradient -- same rule as
`exploit_rate` and `capture` (see core).

WHAT THE LIVE SE IS AND IS NOT. `cci_se` is a decision-level binomial standard
error. Decisions inside one episode are correlated, so it is optimistic; it is
there to tell a reader whether a step's number is built on 40 decisions or 4000,
not to support a claim. For a claim use `bootstrap_cci`, which resamples whole
EPISODES and is what the post-hoc readout should quote.
"""
from __future__ import annotations

import math
from collections import defaultdict
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple

# The two regimes this module compares. Deliberately not `core.CONSEQUENCE`
# imported at module scope: nothing else here needs `core`, and an env-file /
# TextArena import chain on a pure-arithmetic module is a needless coupling.
HOLE, NOHOLE = "hole", "nohole"


def decisions(recs: Sequence[Dict]) -> List[Dict]:
    """One row per scored decision, with everything a stratum is keyed on.

    Reads `exploit_steps` -- the ordered per-scored-decision betrayal timeline
    every env emits (core.episode_record) -- so `t` is the decision's position
    on the cooperative timeline and `k` is how many exploits the learner had
    already taken when it faced this one. Episodes without the timeline (an env
    that predates it, or `with_refs=False`) are skipped rather than approximated
    from the scalar counts, because a rate cannot be placed on a timeline.
    """
    rows: List[Dict] = []
    for i, r in enumerate(recs):
        steps = r.get("exploit_steps")
        if not steps:
            continue
        reg = r.get("consequence")
        if reg not in (HOLE, NOHOLE):
            continue
        env = r.get("env") or "?"
        k = 0
        for t, y in enumerate(steps):
            rows.append({"env": env, "regime": reg, "t": t, "k": k,
                         "y": 1 if y else 0, "ep": i})
            k += 1 if y else 0
    return rows


def _tabulate(rows: Iterable[Dict], key: Callable[[Dict], tuple]
              ) -> Dict[tuple, List[int]]:
    """stratum -> [a, b, c, d] = hole-exploit, hole-not, nohole-exploit, nohole-not."""
    tab: Dict[tuple, List[int]] = defaultdict(lambda: [0, 0, 0, 0])
    for r in rows:
        cell = (0 if r["regime"] == HOLE else 2) + (0 if r["y"] else 1)
        tab[key(r)][cell] += 1
    return tab


def mh(rows: Sequence[Dict],
       key: Callable[[Dict], tuple] = lambda r: (r["env"], r["t"], r["k"])
       ) -> Dict[str, Optional[float]]:
    """Mantel-Haenszel risk difference and log odds ratio over `key` strata.

    Only strata that contain BOTH regimes contribute: a stratum seen under one
    opponent alone carries no contrast and its weight `m1*m0/n` is zero anyway,
    but dropping it explicitly keeps `n_strata` honest about how much of the
    batch the number rests on.

    Weights are `m1*m0/n`, the precision weight, so a 40-vs-40 stratum counts
    for more than a 40-vs-1 one -- which matters here because the truncation
    that motivates the whole module makes late-round strata badly unbalanced.
    """
    tab = _tabulate(rows, key)
    num = den = 0.0        # risk difference
    or_num = or_den = 0.0  # odds ratio
    var_num = 0.0
    n_used = n_strata = 0
    for a, b, c, d in tab.values():
        m1, m0 = a + b, c + d
        n = m1 + m0
        if m1 == 0 or m0 == 0:
            continue
        n_strata += 1
        n_used += n
        num += (a * m0 - c * m1) / n
        w = m1 * m0 / n
        den += w
        or_num += a * d / n
        or_den += b * c / n
        # Binomial variance of this stratum's gap, carried through the same
        # weight. Decision-level only -- see the module docstring.
        p1, p0 = a / m1, c / m0
        var_num += (w ** 2) * (p1 * (1 - p1) / m1 + p0 * (1 - p0) / m0)
    if den <= 0:
        return {"rd": None, "se": None, "lor": None,
                "n": n_used, "n_strata": n_strata}
    rd = num / den
    se = math.sqrt(var_num) / den if var_num > 0 else 0.0
    # A zero in either arm of every stratum makes the odds ratio degenerate
    # rather than infinite; report None instead of a number that is really a
    # statement about the sample size.
    lor = (math.log(or_num / or_den)
           if or_num > 0 and or_den > 0 else None)
    return {"rd": rd, "se": se, "lor": lor, "n": n_used, "n_strata": n_strata}


def _plain_gap(rows: Sequence[Dict]) -> Tuple[Optional[float], int]:
    """Unstratified hole-minus-nohole rate over whatever rows are passed."""
    h = [r["y"] for r in rows if r["regime"] == HOLE]
    n = [r["y"] for r in rows if r["regime"] == NOHOLE]
    if not h or not n:
        return None, len(rows)
    return sum(h) / len(h) - sum(n) / len(n), len(rows)


def step_metrics(recs: Sequence[Dict], per_env: bool = True) -> Dict:
    """The `cue/*` block for one training step.

    Returns {} when the batch has only one regime in it -- a single-regime arm
    has no contrast to measure and logging a null series for 90 steps only
    makes the plots harder to read.
    """
    rows = decisions(recs)
    if not rows:
        return {}
    regimes = {r["regime"] for r in rows}
    if len(regimes) < 2:
        return {}

    out: Dict[str, Optional[float]] = {}
    full = mh(rows)
    out["cue/cci"] = full["rd"]
    out["cue/cci_se"] = full["se"]
    out["cue/lor"] = full["lor"]
    out["cue/n_decisions"] = full["n"]
    out["cue/n_strata"] = full["n_strata"]
    out["cue/n_episodes"] = len({r["ep"] for r in rows})

    # The marginal, so a reader can always see whether `cci` moved on its own
    # or rode a change in the overall level.
    out["cue/rate"] = sum(r["y"] for r in rows) / len(rows)
    # And the unstratified gap, side by side with `cci`: their DIFFERENCE is the
    # composition artefact this module exists to remove, and watching it is the
    # cheapest check that the stratification is doing something.
    raw, _ = _plain_gap(rows)
    out["cue/gap_raw"] = raw

    t0 = [r for r in rows if r["t"] == 0]
    blind, nb = _plain_gap(t0)
    out["cue/blind_gap"] = blind
    out["cue/blind_n"] = nb
    # ... and the same thing standardised over ENV, which is the version to
    # read. `blind_gap` is unstratified, and at the opening decision every
    # episode contributes exactly one row, so under a per-GROUP regime draw the
    # hole and nohole pools can hold different mixtures of envs -- and the
    # roster's base exploit rates differ enough across cells that the mixture
    # alone moves the number. That is the composition confound this module
    # exists to remove, and the placebo had it. Verified 2026-08-24 that the
    # opening observation is byte-identical across arms in all seven cells, so
    # a non-zero reading here is mixture or noise, never a leak.
    # Added as a NEW key rather than a redefinition: `blind_gap` is already
    # being logged by runs in flight and a series that changes meaning halfway
    # is worse than a series with a caveat.
    blind_mh = mh(t0, key=lambda r: (r["env"],))
    out["cue/blind_cci"] = blind_mh["rd"]
    out["cue/blind_cci_se"] = blind_mh["se"]
    informed = mh([r for r in rows if r["k"] >= 1])
    out["cue/informed_gap"] = informed["rd"]
    out["cue/informed_n"] = informed["n"]

    if per_env:
        for env in sorted({r["env"] for r in rows}):
            sub = mh([r for r in rows if r["env"] == env],
                     key=lambda r: (r["t"], r["k"]))
            out[f"cue/env/{env}/cci"] = sub["rd"]
            out[f"cue/env/{env}/n"] = sub["n"]
    return out


def bootstrap_cci(recs: Sequence[Dict], n_boot: int = 1000, seed: int = 0
                  ) -> Dict[str, Optional[float]]:
    """`cci` with an EPISODE-clustered bootstrap CI. For post-hoc readouts.

    Resamples episodes, not decisions: the decisions inside one episode share a
    seed, a counterpart and a policy trajectory, so a decision-level interval
    understates the spread by roughly the square root of the episode length.
    """
    import random as _random

    point = mh(decisions(recs))
    if point["rd"] is None:
        return {"cci": None, "lo": None, "hi": None, "n_boot": 0}
    rng = _random.Random(seed)
    idx = list(range(len(recs)))
    draws: List[float] = []
    for _ in range(n_boot):
        pick = [recs[rng.choice(idx)] for _ in idx]
        r = mh(decisions(pick))
        if r["rd"] is not None:
            draws.append(r["rd"])
    if not draws:
        return {"cci": point["rd"], "lo": None, "hi": None, "n_boot": 0}
    draws.sort()
    lo = draws[int(0.025 * (len(draws) - 1))]
    hi = draws[int(0.975 * (len(draws) - 1))]
    return {"cci": point["rd"], "lo": lo, "hi": hi, "n_boot": len(draws)}
