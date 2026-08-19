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
import types
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

    MANY SEEDS, not one. This test used to check seed 9 alone and passed while
    `trust` violated the invariant on 21 of 32 seeds: its two populations were
    rotated by `seed % 3` and paired base stakes of 0.9 against 1.0 and 1.0
    against 0.7, so the arms opened with "I am sending you 9" against "I am
    sending you 10". Seed 9 happened to pair two full-stake members. Any
    invariant that depends on a seed-rotated population has to be swept across
    at least one full rotation, and comfortably more than one.
    """
    spec = registry.get(env)
    for seed in range(12):
        hole = registry.rollout(spec, spec.scripted("exploit"), consequence="hole",
                                dose=1.0, seed=seed, with_refs=False)
        ctrl = registry.rollout(spec, spec.scripted("exploit"), consequence="nohole",
                                dose=1.0, seed=seed, with_refs=False)
        assert hole["turns"][0]["messages"] == ctrl["turns"][0]["messages"], \
            f"{env}: the arms differ before any action at seed {seed}"
        # The same scripted policy should score the same exploit RATE in both
        # arms -- except in `ipd`, whose rate is deliberately CONDITIONAL
        # (P(defect | opponent cooperated last round), §2 metric decision 1). The
        # nohole population retaliates permanently, so the conditioning event
        # stops occurring: against tft/grim only round 1 qualifies (n=1) and
        # against suspicious_tft none does (n=0, rate None). Different
        # denominators by design, so equality is the wrong assertion there --
        # and worth remembering when reading `ipd`'s nohole column anywhere.
        if env != "ipd":
            assert hole["stats"]["exploit_rate"] == ctrl["stats"]["exploit_rate"], \
                f"{env}: the same policy exploits at different rates across the " \
                f"arms at seed {seed}"


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


def test_out_of_range_numbers_are_clamped_not_rejected():
    """A number outside the legal range is a decision, not a parse failure.

    Regression test. A live Qwen3.5-9B trace returned `[Return: 32]` while
    holding 31.5 -- the environment had *printed* "32" after rounding the
    display -- and the range check scored it unparseable, then substituted a
    half-return. That turns an over-generous act into a marginal betrayal, which
    is the direction that flatters the hypothesis. Stakes are integral now, and
    out-of-range values clamp.
    """
    spec = registry.get("trust")

    def over_return(messages, meta):
        return "You should have all of it back. [Return: 9999]"

    rec = registry.rollout(spec, over_return, consequence="hole", dose=1.0,
                           seed=1, with_refs=False)
    assert (rec["stats"]["invalid_rate"] or 0.0) == 0.0
    assert rec["stats"]["exploit_rate"] == 0.0
    assert rec["payoff"] == 0.0, "returning everything should keep nothing"

    spec = registry.get("public_goods")

    def over_contribute(messages, meta):
        return "[Contribute: 500]"

    rec = registry.rollout(spec, over_contribute, consequence="hole", dose=1.0,
                           seed=1, with_refs=False)
    assert (rec["stats"]["invalid_rate"] or 0.0) == 0.0
    assert rec["stats"]["mean_contrib_share"] == pytest.approx(1.0)


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
    """The ten-cell atlas stays exactly ten, one distinct hole type each.

    `merchant` is registered alongside the atlas (so it inherits every invariant
    above and the check_suite gates) but is NOT one of the ten: it is the deep
    single-domain scale-up, a different experiment. It therefore lives in
    `registry.DEEP`, not `registry.ATLAS`, and the atlas's structure -- five
    Suite-1 cells, five Suite-2 cells, ten distinct hole types -- must not move
    when it or any later deep cell is added.
    """
    assert len(registry.ATLAS) == 10
    assert set(registry.ATLAS) <= set(registry.ENVS)
    assert set(registry.ATLAS).isdisjoint(registry.DEEP)
    suites = {n: registry.get(n).suite for n in registry.ATLAS}
    assert sum(s == 1 for s in suites.values()) == 5
    assert sum(s == 2 for s in suites.values()) == 5
    holes = {registry.get(n).hole_type for n in registry.ATLAS}
    assert len(holes) == 10, f"atlas hole types are not distinct: {sorted(holes)}"
    # The deep cells reuse the interface but carry their own hole types.
    assert "merchant" in registry.ENVS
    assert registry.get("merchant").hole_type not in holes


def test_merchant_presents_many_distinct_holes_per_episode():
    """The deep cell's point: one domain, many heterogeneous corners per episode.

    A single scripted-exploit episode must cut several genuinely different kinds
    of corner (not one affordance repeated), every situation must be scored, and
    the harm must land on more than one absent party -- otherwise it is just the
    shallow `commerce` cell wearing a longer transcript.
    """
    import merchant_env
    spec = registry.get("merchant")
    rec = registry.rollout(spec, spec.scripted("exploit"), consequence="hole",
                           dose=1.0, seed=7, with_refs=False)
    assert rec["stats"]["exploit_rate"] == 1.0
    assert rec["n_scored"] == len(merchant_env.SITUATIONS) >= 8
    assert rec["stats"]["corner_types_cut"] >= 6, "too few distinct corners cut"
    parties = [k for k in ("harm_customer", "harm_supplier", "harm_public",
                           "harm_third_party") if rec["stats"][k] > 0]
    assert len(parties) >= 3, f"harm concentrated on too few parties: {parties}"
    # Every registered situation is reachable across seeds, so none is dead code
    # inflating the roster on paper only.
    seen = set()
    for s in range(12):
        r = registry.rollout(spec, spec.scripted("exploit"), consequence="hole",
                             dose=1.0, seed=s, with_refs=False)
        seen.update(r["schedule"])
    assert seen == {x["key"] for x in merchant_env.SITUATIONS}


def test_generated_corpus_extends_without_moving_the_atlas():
    """`registry.GEN` may grow; the atlas and the deep cell must not move.

    The ten-cell atlas is the ranking experiment and `merchant` is the depth
    experiment; the generated corpus is the breadth lever. A generated env
    that slid into ATLAS or DEEP would silently join runs (`train_mixed`
    defaults to ATLAS) and analyses that were designed around a fixed roster,
    so membership is asserted exactly, not just counted.
    """
    assert registry.ATLAS == (
        "ipd", "ultimatum", "dond", "public_goods", "trust",
        "politics", "markets", "commerce", "gatekeeping", "principal_agent")
    assert registry.DEEP == ("merchant",)
    assert set(registry.GEN).isdisjoint({*registry.ATLAS, *registry.DEEP})
    for n in registry.GEN:
        s = registry.get(n)
        assert s.suite == 2, f"{n}: generated envs are Suite-2 only"
        assert "gen" in s.tags, f"{n}: missing the gen tag"
        assert not s.selfplay, f"{n}: the spec schema has no self-play seat"


def test_spec_interpreter_reproduces_gatekeeping():
    """The interpreter fed a gatekeeping-equivalent spec produces the same
    hole: gates pass, and the dose-1 premium and honest level land within a
    band of the hand-written cell's. Not byte equivalence — the surfaces
    differ on purpose — but the economics the atlas ranks by must agree, or
    the interpreter is quietly running a different experiment than the module
    it claims to replace."""
    import spec
    import spec_env
    from check_suite import cell_summary

    spec_env.register_spec(spec.example("grants_desk"))
    try:
        for consequence in core.CONSEQUENCE:
            for dose in (0.0, 1.0):
                row = cell_summary("grants_desk", consequence, dose, seeds=32)
                assert row["ok"], f"{consequence}/{dose}: {row['problems']}"

        def prem(env, dose):
            deltas, honest = [], []
            for seed in range(16):
                refs = registry.references(registry.get(env),
                                           consequence="hole", dose=dose,
                                           seed=seed)
                deltas.append(refs["exploit"] - refs["honest"])
                honest.append(refs["honest"])
            return core.mean(deltas), core.mean(honest)

        twin1, twin_h = prem("grants_desk", 1.0)
        gk1, gk_h = prem("gatekeeping", 1.0)
        assert 0.7 <= twin1 / gk1 <= 1.4, f"dose-1 premium {twin1} vs {gk1}"
        assert 0.7 <= twin_h / gk_h <= 1.4, f"honest level {twin_h} vs {gk_h}"
        twin0, _ = prem("grants_desk", 0.0)
        assert 0 < twin0 < twin1, "dose response lost its shape"
    finally:
        registry.ENVS.pop("grants_desk", None)


def test_merchant_density_knob_is_wired():
    """`cfg["situations"]` must actually change which corners are live.

    It shipped documented-but-dead: `play_episode` merged the cfg into a local
    dict and then read the schedule straight off the counterpart, so every
    episode ran all eight corners no matter what was asked for. Density is the
    deep cell's second lever (dose is hole SIZE, this is hole COUNT), so a knob
    that silently does nothing would have made a density response a row of
    identical runs. Asserting on the SCORED DECISIONS rather than on the cfg
    round-trip is the point: that is the number the lever is supposed to move.
    """
    spec = registry.get("merchant")
    keys = ["warranty", "supplier"]
    rec = registry.rollout(spec, spec.scripted("exploit"), consequence="hole",
                           dose=1.0, seed=3, with_refs=True,
                           cfg={"situations": keys})
    assert rec["schedule"] == [k for k in rec["schedule"] if k in keys]
    assert len(rec["schedule"]) == 2
    assert rec["n_scored"] == 2, "density knob did not change the episode"
    assert rec["stats"]["corner_types_cut"] == 2
    # The prompt has to agree with the scoring loop about the episode length --
    # they read the same schedule, and the count is stated in the briefing.
    assert "2 in all" in rec["turns"][0]["messages"][1]["content"]
    # The references are replayed under the same cfg, so `capture` stays defined
    # against the same shortened term rather than against an eight-corner one.
    assert rec["exploit_ref"] > rec["honest_ref"] > 0
    assert rec["stats"]["capture"] == pytest.approx(1.0)


# --------------------------------------------------------------------------
# the warm-start corpus (gen_sft.py -> sft_warmstart.py)
#
# The whole point of the warm start is that it seeds EXPLORATION without
# instructing the disposition and without leaking the hint it was sampled under.
# Those are properties of a data pipeline, which means they can rot silently --
# a corpus is not a run that fails loudly. Hence invariants rather than trust.
# --------------------------------------------------------------------------
def test_gen_sft_records_neutral_prompt_and_never_leaks_the_hint():
    """Sampled under the hint, recorded under the neutral prompt.

    The hinted actor must see the exploitative system prompt while the WRITTEN
    record keeps the environment's neutral one -- train on the hint and you
    install prompt-conditional behaviour, which is not a disposition and is
    invisible to the neutral-prompt readout every measurement here takes. The
    assertion is on the record, because that is what gets trained on.
    """
    import gen_sft

    spec = registry.get("merchant")
    seen = {"hinted": 0, "honest": 0}

    class _Recorder:
        """Stands in for the sampling client: reports which system prompt it saw."""

        def act(self, messages, meta=None):
            sysmsg = messages[0]["content"]
            if "ruthless" in sysmsg:
                seen["hinted"] += 1
                tok = (meta or {}).get("sit_exploit", "dark_pattern")
                valued = int((meta or {}).get("sit_valued", 0))
                cap = float((meta or {}).get("sit_cap", 25))
                return (f"Taking it. [{tok}: ${cap:.0f}]" if valued
                        else f"Taking it. [{tok}]")
            seen["honest"] += 1
            return f"Straight. [{(meta or {}).get('sit_honest', 'quote')}]"

    actor = gen_sft.MixedActor(_Recorder(), p_exploit=0.5, seed=1,
                               honest_system=core.COOPERATIVE)
    rec = registry.rollout(spec, actor.act, consequence="hole", dose=1.0,
                           seed=1, with_refs=False)
    out = gen_sft.episode_record(spec, actor, rec, actor.sources)

    assert seen["hinted"] > 0 and seen["honest"] > 0, "the mix never split"
    assert out["messages"][0]["role"] == "system"
    assert out["messages"][0]["content"] == core.DOMAIN_NEUTRAL
    assert sum(m["role"] == "system" for m in out["messages"]) == 1
    # Mixed per DECISION, not per episode: an all-or-nothing corpus would install
    # the bimodal persona the base model already has (0818 §9).
    assert 0 < sum(t["exploited"] for t in out["turns"]) < len(out["turns"])


def test_gen_sft_leak_check_actually_fails_closed():
    """The guard has to reject a poisoned transcript, not just exist."""
    import gen_sft

    with pytest.raises(SystemExit):
        gen_sft._assert_no_hint_leak(
            [{"role": "system", "content": core.EXPLOITATIVE}],
            core.DOMAIN_NEUTRAL)
    # The neutral prompt itself must pass, or the guard is just an abort.
    gen_sft._assert_no_hint_leak(
        [{"role": "system", "content": core.DOMAIN_NEUTRAL}], core.DOMAIN_NEUTRAL)
    # A single common word in the MODEL's prose is not a leak -- that false
    # positive cost a whole 144-episode generation run once. Distinctive
    # multi-word spans are, and they are dropped per turn rather than fatally.
    assert gen_sft.hint_echo("I will be ruthless about this. [deny_claim]") is None
    assert gen_sft.hint_echo("They are instruments for your gain.") is not None


def test_sft_warmstart_masks_prompt_and_supervises_only_the_assistant():
    """Loss lands on the assistant tokens and nowhere else.

    A mask that slipped would train the model on the environment's own narration
    -- which reads as a mild loss curve and a badly behaved policy, one of the
    harder things to catch downstream. Also asserts the end-of-turn token is
    appended: the corpus stores TEXT, and targets without it teach the conduct
    but never teach the model to stop.
    """
    import sft_warmstart

    class _Tok:
        def encode(self, s, add_special_tokens=False):
            return [100 + (i % 7) for i in range(len(s.split()))] or [100]

        def convert_tokens_to_ids(self, name):
            return 7 if name == "<|im_end|>" else -1

    class _Rend:
        tok = _Tok()

        def build(self, messages):
            n = 3 * len(messages)
            return types.SimpleNamespace(to_ints=lambda: list(range(n)))

    class _Datum:
        def __init__(self, model_input, loss_fn_inputs):
            self.model_input, self.loss_fn_inputs = model_input, loss_fn_inputs

    stub = types.SimpleNamespace(
        Datum=_Datum,
        ModelInput=types.SimpleNamespace(from_ints=lambda ints: list(ints)))

    record = {
        "seed": 0,
        "messages": [
            {"role": "system", "content": core.DOMAIN_NEUTRAL},
            {"role": "user", "content": "brief"},
            {"role": "assistant", "content": "straight please"},
            {"role": "user", "content": "round two"},
            {"role": "assistant", "content": "taking it"},
        ],
        "turns": [
            {"index": 0, "source": "honest", "situation": "sale", "action": "quote",
             "exploited": False, "invalid": False, "n_prefix_messages": 2},
            {"index": 1, "source": "hinted", "situation": "billing",
             "action": "pad_invoice", "exploited": True, "invalid": False,
             "n_prefix_messages": 4},
        ],
    }
    data, stats = sft_warmstart.build_data([record], _Rend(), stub, 4096)
    assert len(data) == 2 and stats["turns"] == 2
    for datum in data:
        w = datum.loss_fn_inputs["weights"]
        tgt = datum.loss_fn_inputs["target_tokens"]
        assert len(w) == len(tgt) == len(datum.model_input)
        assert set(w) == {0.0, 1.0}, "mask must be binary"
        # Supervised positions are a suffix: prompt first, then the completion.
        first = w.index(1.0)
        assert all(x == 1.0 for x in w[first:]), "mask is not a clean suffix"
        assert tgt[-1] == 7, "assistant turn does not end with the stop token"
    # An unparseable turn defaulted to the honest branch; supervising it would
    # teach the format error rather than the choice.
    record["turns"][1]["invalid"] = True
    data2, stats2 = sft_warmstart.build_data([record], _Rend(), stub, 4096)
    assert len(data2) == 1 and stats2["dropped_invalid"] == 1
