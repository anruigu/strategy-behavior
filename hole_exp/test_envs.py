"""Offline tests for the hole atlas. No API, no GPU, no network.

    /workspace/allie/venvs/tinker-ipd/bin/python -m pytest test_envs.py -q

What is tested here is the machinery that the science rests on and that a
reviewer cannot see by reading a training curve: that the reward carries no
exploit term, that references are replays of the same seed, that a format
failure can never be scored as exploitation, and that the two arms differ in
the consequence branch and in nothing else.

The economics of each cell -- is the hole a hole, is it closed in the control,
is honesty reachable -- is `check_suite.py`'s job, over many seeds. These tests
are the fast invariants; that one is the experiment's own precondition.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import core  # noqa: E402
import registry  # noqa: E402

ALL = sorted(registry.ENVS)


# --------------------------------------------------------------------------
# parsing
# --------------------------------------------------------------------------


def test_last_choice_takes_the_final_token():
    """A model that weighs the exploit aloud and then declines chose to decline."""
    text = ("I could [bribe: $20] here, but that is not how I want to work. "
            "[honest]")
    assert core.last_choice(text, ["bribe", "honest"]) == "honest"


def test_last_number_reads_the_last_value():
    assert core.last_number("[Offer: $2] ... on reflection [Offer: $5]", "Offer") == 5.0
    assert core.last_number("[Contribute: 12]", "Contribute") == 12.0
    assert core.last_number("nothing here", "Offer") is None


def test_last_mapping_parses_a_structured_claim():
    got = core.last_mapping("[Claim: books=5, hats=0, balls=2]", "Claim")
    assert got == {"books": 5.0, "hats": 0.0, "balls": 2.0}


def test_draws_are_named_not_ordered():
    """Adding a channel must not shift the value of an existing one."""
    a = core.Draws(7, salt="x")
    b = core.Draws(7, salt="x")
    assert a.u("audit") == b.u("audit")
    b.u("something_new")
    assert a.u("audit") == b.u("audit")
    assert a.u("audit") != a.u("permit")


# --------------------------------------------------------------------------
# the record contract
# --------------------------------------------------------------------------


@pytest.mark.parametrize("env", ALL)
@pytest.mark.parametrize("consequence", list(core.CONSEQUENCE))
def test_record_shape(env, consequence):
    spec = registry.get(env)
    rec = registry.rollout(spec, spec.scripted("exploit"), consequence=consequence,
                           dose=1.0, seed=3)
    for key in ("env", "seed", "consequence", "dose", "opponent", "payoff",
                "turns", "score", "honest_ref", "exploit_ref"):
        assert key in rec, f"{env}: missing {key}"
    for key in ("exploit_rate", "invalid_rate", "capture", "premium"):
        assert key in rec["stats"], f"{env}: missing stat {key}"
    assert rec["turns"], f"{env}: produced no model turns"
    assert rec["stats"]["invalid_rate"] in (0.0, None), \
        f"{env}: a scripted reference should always parse"


@pytest.mark.parametrize("env", ALL)
def test_reward_is_payoff_only(env):
    """The training signal must be own payoff, scaled, and nothing else.

    This is the test that stops the headline finding from being true by
    construction: if a capture or exploit-rate term ever leaks into `score`,
    "training in a hole raises exploitation" stops being a finding.
    """
    spec = registry.get(env)
    rec = registry.rollout(spec, spec.scripted("exploit"), consequence="hole",
                           dose=0.5, seed=11)
    assert rec["score"] == pytest.approx(rec["payoff"] / spec.payoff_scale)


@pytest.mark.parametrize("env", ALL)
def test_episodes_are_deterministic_given_the_seed(env):
    """Same seed, same scripted policy, same everything -- or the references are
    not replays of the measured episode and `capture` means nothing."""
    spec = registry.get(env)
    a = registry.rollout(spec, spec.scripted("exploit"), consequence="hole",
                         dose=0.75, seed=5)
    b = registry.rollout(spec, spec.scripted("exploit"), consequence="hole",
                         dose=0.75, seed=5)
    assert a["payoff"] == b["payoff"]
    assert a["stats"]["exploit_rate"] == b["stats"]["exploit_rate"]
    assert a["opponent"] == b["opponent"]


@pytest.mark.parametrize("env", ALL)
def test_the_arms_differ_only_after_the_action(env):
    """hole and nohole must present the SAME environment to the model.

    The consequence branch prices what was done; it must not change what the
    agent was asked, what it could do, or what it saw while deciding. If the
    prompts differed, the arms would differ in the task as well as in the
    consequence, and no amount of transfer analysis could separate the two.
    """
    spec = registry.get(env)
    hole = registry.rollout(spec, spec.scripted("exploit"), consequence="hole",
                            dose=1.0, seed=9, with_refs=False)
    ctrl = registry.rollout(spec, spec.scripted("exploit"), consequence="nohole",
                            dose=1.0, seed=9, with_refs=False)
    first_hole = hole["turns"][0]["messages"]
    first_ctrl = ctrl["turns"][0]["messages"]
    assert first_hole == first_ctrl, f"{env}: the arms differ before any action"
    assert hole["stats"]["exploit_rate"] == ctrl["stats"]["exploit_rate"], \
        f"{env}: the same policy exploits at different rates across the arms"


@pytest.mark.parametrize("env", ALL)
def test_garbage_is_never_scored_as_exploitation(env):
    """A format collapse must not be able to manufacture an exploit rate.

    Every environment defaults an unparseable turn to its non-exploitative
    branch and counts it as invalid instead. Without this rule a model that
    degenerated into gibberish would read as maximally exploitative, which is
    the single easiest way for this whole design to fool itself.
    """
    spec = registry.get(env)

    def garbage(messages, meta):
        return "I am not going to answer that."

    for consequence in core.CONSEQUENCE:
        rec = registry.rollout(spec, garbage, consequence=consequence, dose=1.0,
                               seed=2, with_refs=False)
        assert (rec["stats"]["exploit_rate"] or 0.0) == 0.0, \
            f"{env}/{consequence}: unparseable turns scored as exploitation"
        assert (rec["stats"]["invalid_rate"] or 0.0) > 0.0, \
            f"{env}/{consequence}: unparseable turns were not counted as invalid"


@pytest.mark.parametrize("env", ALL)
def test_scripted_references_sit_at_the_ends_of_the_scale(env):
    """capture(honest) == 0 and capture(exploit) == 1, by construction."""
    spec = registry.get(env)
    for policy, expected in (("honest", 0.0), ("exploit", 1.0)):
        rec = registry.rollout(spec, spec.scripted(policy), consequence="hole",
                               dose=1.0, seed=4)
        cap = rec["stats"]["capture"]
        if cap is None:
            pytest.skip(f"{env}: degenerate premium at this seed")
        assert cap == pytest.approx(expected, abs=1e-6)


@pytest.mark.parametrize("env", ALL)
def test_population_members_are_distinct_and_used(env):
    """Each arm draws from a population, not from one frozen opponent.

    A brittle exploit of a single fixed policy is not a disposition; the
    population is the treatment. Rotating by seed also has to actually rotate --
    a population that is never sampled is a comment, not a control.
    """
    spec = registry.get(env)
    for consequence in core.CONSEQUENCE:
        pop = spec.populations(consequence)
        assert len(set(pop)) >= 3, f"{env}/{consequence}: population too small"
        seen = {registry.rollout(spec, spec.scripted("honest"),
                                 consequence=consequence, dose=1.0, seed=s,
                                 with_refs=False)["opponent"]
                for s in range(len(pop) * 2)}
        assert seen == set(pop), f"{env}/{consequence}: saw {seen}, expected {set(pop)}"


@pytest.mark.parametrize("env", ALL)
def test_dose_is_monotone_in_the_premium(env):
    """A bigger dose must not buy a smaller hole.

    Checked at the ends of the range only, and on the MEAN over seeds: several
    cells draw their scenario per seed, so a single-seed comparison is a coin
    flip dressed as a monotonicity test (DoND fails it at seed 6 and passes it
    on the average, which is the version that describes the knob). Saturation in
    the middle is a shape worth reporting, not a bug -- a REVERSAL between the
    endpoints is a bug, because it would make the dose-response plot argue the
    opposite of what the knob does.
    """
    spec = registry.get(env)
    prem = {}
    for dose in (0.0, 1.0):
        deltas = []
        for seed in range(16):
            refs = registry.references(spec, consequence="hole", dose=dose,
                                       seed=seed)
            deltas.append(refs["exploit"] - refs["honest"])
        prem[dose] = core.mean(deltas)
    assert prem[1.0] >= prem[0.0] - 1e-6, f"{env}: premium falls with dose {prem}"


def test_selfplay_capture_is_withheld():
    """Under self-play the references are vs the scripted seat, so the
    normalised premium is not a like-for-like ratio and must not be reported."""
    spec = registry.get("markets")

    def act(messages, meta):
        return "[Price: 90] [collude]"

    rec = registry.rollout(spec, act, consequence="hole", dose=1.0, seed=1,
                           act_rival=act)
    assert rec["stats"]["capture"] is None
    assert "capture_undefined" in rec["stats"]
    assert rec["selfplay"]["turns"], "the second seat produced no trajectories"


def test_registry_covers_both_suites():
    assert len(registry.SUITE1) == 5 and len(registry.SUITE2) == 5
    holes = {registry.get(n).hole_type for n in ALL}
    assert len(holes) == 10, f"hole types are not distinct: {sorted(holes)}"
