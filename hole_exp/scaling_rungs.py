"""The env-count dose-response ladder (0820-scaling-envs.md): rung sets, held-out
sets, and the constant-compute budget, in ONE place.

Training and evaluation both import this. If the rungs lived in the launcher and
the held-out list lived in the eval script, a single edit to one of them would
silently put a trained env on the x-axis of the held-out curve -- which is the
one mistake this study cannot survive, because the whole y-axis is "generalises
to things it never saw".

THE CONTROLS (from the plan, restated here because the code has to enforce them):

1. **Constant compute per rung.** Every rung trains for the same number of steps
   with the same number of GROUPS and the same group size -- so a rung with 8
   envs sees 1/8th as many episodes per env as the n=1 rung, not 8x as many
   episodes total. Otherwise the curve measures data volume and calls it
   diversity. `GROUPS`/`GROUP_SIZE`/`STEPS` below are what makes this true, and
   they must be passed explicitly: train_mixed.py defaults `--groups` to
   len(envs), which is exactly the scaling-with-n behaviour we are controlling
   against.

2. **Nested rung sets.** RUNGS[n] is a prefix of the family's ORDER, so
   n=1 c n=2 c n=4 c n=8. A rise between rungs is then "these envs were added",
   never "the training set was resampled".

3. **A FIXED held-out set, disjoint from every rung.** HELD_OUT is identical at
   every rung and shares no member with any rung, asserted at import.

ORDERING CAVEAT. The plan asks for two random orderings per family so a jump
cannot be one potent env being added. Two orderings doubles the run count and
does not fit one night, so this ships ONE ordering per family, chosen to
STRATIFY rather than randomise: each rung addition brings a hole type not
already in the set, and the generated/hand-crafted (or TextArena/native) split
is kept balanced as n grows. That controls the "one potent env" worry by
construction better than a single random draw would, but it is not the same as
averaging over orderings -- a second ordering is the first follow-up if pass 1
rises.
"""
from __future__ import annotations

from typing import Dict, List, Sequence

# -- constant-compute budget -------------------------------------------------
# 8 groups x 6 episodes = 48 episodes/step at EVERY rung, 70 steps. Checkpoints
# every 10 steps rather than at 0/25/50/75/100%: with 12 runs contending for one
# Tinker account, they will not all reach step 70 by morning, and a dense ladder
# means the readout can be taken at the highest step EVERY arm reached instead of
# comparing a finished arm against an unfinished one.
STEPS = 70
GROUPS = 8
GROUP_SIZE = 6
CKPT_EVERY = 10
MODEL = "Qwen/Qwen3.8-27B"
DOSE = 1.0

# -- sampling profile --------------------------------------------------------
# Qwen3.8-27B needs different sampling from 3.6 (0820-qwen38-sampling-profile.md).
# This ladder takes the SAFE part of `tinker_actor.TUNED_TOOL_SAMPLING` and
# deliberately leaves out `close_bracket`:
#
#   temperature 0.7, top_p 0.9   the low-entropy half. Stops the model looping
#                                past its own action.
#   max_tokens 512 (was 384)     headroom against truncation, free here.
#   thinking off                 already the default in tinker_actor.build();
#                                without it the 3.8 template resolves
#                                reasoning_effort to `xhigh` and blows the budget.
#   close_bracket OFF            NOT safe for this roster. It stops generation
#                                at `]` and, separately, REPLACES the renderer's
#                                EOS stops. Half the cells here put the argument
#                                AFTER the bracket -- TwoDollar's
#                                "[Propose] $1.00" would become "[Propose]" and
#                                the opening-demand regex would stop matching --
#                                and nat_assay/nat_shoal reply with a bare
#                                number and would lose their stop token
#                                entirely. It is the right lever for the agentic
#                                `merchant` tool loop it was tuned on, and the
#                                wrong one here.
#
# What triggered this: at t=1.0/384 the first launch of this ladder showed
# `nat_assay` at 0.225 invalid, against check_suite's BROKEN threshold of 0.25.
# nat_assay enters only at the n=8 GAME rung, so a degraded instrument would
# have sat on exactly the top rung of one family's curve and read as saturation.
TEMPERATURE = 0.7
TOP_P = 0.9
MAX_TOKENS = 512
CLOSE_BRACKET = False

# -- family: games -----------------------------------------------------------
# Nine game-framed cells exist (five TextArena + four native designs), so this
# family reaches n=8 with one cell left over to hold out. Order alternates
# TextArena/native and never repeats a hole type until it has to.
GAME_ORDER: List[str] = [
    "ta_ipd",        # defect                (TextArena)   n=1
    "nat_shoal",     # over_extract          (native)      n=2
    "ta_pubgoods",   # free_ride             (TextArena)   n=4
    "nat_convoy",    # broken_pledge         (native)
    "ta_ipd3",       # defect_multiparty     (TextArena)   n=8
    "nat_assay",     # misreport             (native)
    "ta_staghunt",   # defect_coordination   (TextArena)
    "ta_winasmuch",  # defect_commons        (TextArena)
]
# Never trained at any rung. `nat_ledger` is the in-family held-out GAME cell --
# an overclaim hole, a type absent from GAME_ORDER, so a rate that moves on it is
# transfer rather than the same move under a new skin. ta_kuhn/ta_negotiation are
# registry.HELDOUT; agg_two_dollar lives in games_aggression.py and is in no
# registry roster at all, so it is held out by construction.
GAME_HELD_OUT: List[str] = ["nat_ledger", "ta_kuhn", "ta_negotiation"]

# -- family: synthetic (RETIRED 0820) ----------------------------------------
# The generated corpus was pruned to the five domains that isolate a genuine
# social-shortcut hole -- a self-serving breach of trust with an identifiable
# victim -- dropping the permitted-discretion "rounding/padding" scenarios and
# the victimless `side_deal`. That leaves too few generated domains to scale
# their COUNT 1->8, which was this family's whole point, so the synthetic
# scaling family is retired: only `game` remains, and eval_scaling reads a
# game-only Tier A.

RUNG_NS: Sequence[int] = (1, 2, 4, 8)
FAMILIES: Dict[str, Dict] = {
    "game": {"order": GAME_ORDER, "held_out": GAME_HELD_OUT},
}


def rung(family: str, n: int) -> List[str]:
    """The nested training set for `family` at n envs."""
    order = FAMILIES[family]["order"]
    if n > len(order):
        raise SystemExit(f"{family}: rung n={n} > {len(order)} available envs")
    return list(order[:n])


def label(family: str, n: int, arm: str, seed: int = 0) -> str:
    """Must match train_mixed.py's own label construction, which is
    `mixed_{suffix}_{arm}_d{dose:g}_s{seed}` -- the eval reads run dirs by name."""
    return f"mixed_scale-{family}-n{n}_{arm}_d{DOSE:g}_s{seed}"


def _check() -> None:
    for fam, d in FAMILIES.items():
        order, held = d["order"], d["held_out"]
        if len(order) != len(set(order)):
            raise SystemExit(f"{fam}: duplicate env in ORDER")
        overlap = set(order) & set(held)
        if overlap:
            raise SystemExit(f"{fam}: held-out set is not disjoint from the "
                             f"rungs: {sorted(overlap)}")
        if max(RUNG_NS) > len(order):
            raise SystemExit(f"{fam}: top rung n={max(RUNG_NS)} needs "
                             f"{max(RUNG_NS)} envs, ORDER has {len(order)}")


_check()


if __name__ == "__main__":
    import json
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import registry  # noqa: E402  (import here: costs ~2s, only the CLI needs it)

    unknown = [e for fam in FAMILIES.values()
               for e in list(fam["order"]) + list(fam["held_out"])
               if e not in registry.ENVS]
    if unknown:
        raise SystemExit(f"not in registry.ENVS: {unknown}")
    for fam in FAMILIES:
        print(f"== {fam} ==")
        for n in RUNG_NS:
            print(f"  n={n:<2d} {' '.join(rung(fam, n))}")
        print(f"  held-out ({len(FAMILIES[fam]['held_out'])}): "
              f"{' '.join(FAMILIES[fam]['held_out'])}")
    print(f"\nbudget: {STEPS} steps x {GROUPS} groups x {GROUP_SIZE} "
          f"= {STEPS * GROUPS * GROUP_SIZE} episodes/run at every rung")
    print(json.dumps({"model": MODEL, "dose": DOSE, "rungs": list(RUNG_NS)}))
