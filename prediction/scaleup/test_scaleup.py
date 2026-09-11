from copy import deepcopy
from dataclasses import replace
import json

import pytest

from benchmark.scaleup.taxonomy import CATEGORIES
from .catalog import FAMILIES, render, validate_game
from .design import generate, audit_design, split_manifests, game_from_record, episode_plan
from .engine import initial, transition, observation, messages
from .runner import scripted_episode, verify_trace, step_record, episode_from_record
from .schema import Game, Episode
from .validate import validate_records


def game(fid, **params):
    return Game(fid, {**{k: v.default for k, v in FAMILIES[fid].parameters.items()}, **params}, 0)


def play(g, actions, seed=0, policy="ordinary"):
    state = initial(g, seed)
    facts = []
    for action in actions:
        state, fact = transition(g, state, action, policy)
        facts.append(fact)
    return state, facts


def test_complete_taxonomy_and_real_witnesses():
    assert {f.mechanism for f in FAMILIES.values() if f.mechanism} == set(CATEGORIES)
    records, _ = generate(blocks=1)
    anchors = [r for r in records if r["intervention_axis"] is None]
    result, _ = validate_records(anchors, seeds=tuple(range(8)))
    assert all(r["witness_execution_variants"] for r in result["coverage"].values() if r["mechanism"])


def test_design_interventions_reproducibility_and_leakage():
    records, pairs = generate(blocks=3)
    assert (records, pairs) == generate(blocks=3)
    splits = split_manifests(records)
    audit = audit_design(records, pairs, splits)
    assert audit["parameter_pairs"] > 500
    for regime, key in (("held_out_family", "family_id"), ("held_out_construction", "pair_group_id")):
        grouped = {}
        for row in records:
            grouped.setdefault(row[key], set()).add(splits[regime]["assignments"][row["game_id"]])
        assert all(len(folds) == 1 for folds in grouped.values())
    assignments = splits["parameter_extrapolation"]["assignments"]
    assert all(assignments[r["game_id"]] == "test" for r in records if r["parameters"]["reward"] == 12)
    bad = deepcopy(pairs)
    bad[0]["axis"] = "not_the_axis"
    with pytest.raises(ValueError):
        audit_design(records, bad, splits)


def test_paired_models_seats_seeds_and_framings():
    records, _ = generate(["certificate_office"], blocks=1)
    plan = list(episode_plan(records, ["a", "b"], trials=2))
    for trial in (0, 1):
        trial_rows = [r for r in plan if r["trial"] == trial]
        assert len({r["environment_seed"] for r in trial_rows}) == 1
        assert len({tuple(r["seat_order"]) for r in trial_rows}) == 1
    assert len({r["episode_id"] for r in plan}) == len(plan)


def test_resource_cycle_and_patch_independent_accounting():
    g = game("conversion_market", reward=6, action_cost=1)
    state, facts = play(g, ["buy", "split", "sell"])
    control, _ = play(replace(g, control=True), ["buy", "split", "sell"])
    assert state["scores"][0] == 23  # 20 - 2 - 1 + 6
    assert control["scores"][0] == 19  # 20 - 2 - 1 + 2
    assert state["crates"] == state["boards"] == 0
    assert facts[1]["mechanism_executed"]


def test_unchanged_exogenous_draws_and_audit_extremes():
    zero = game("certificate_office", detection_probability=0)
    certain = game("certificate_office", detection_probability=1)
    z, zf = play(zero, ["report_high"])
    a, af = play(certain, ["report_high"])
    assert z["scores"][0]-a["scores"][0] == certain.parameters["punishment_severity"]
    assert af[0]["audited"] and not zf[0]["audited"]
    assert initial(zero, 7)["hidden_bit"] == initial(certain, 7)["hidden_bit"]


def test_hidden_state_and_evaluator_never_in_player_prompt():
    g = game("sealed_archive")
    ep = Episode(g.game_id, "model", 0, 2, (2, 0, 1))
    s = initial(g, 2)
    prompt = messages(g, s, ep)
    visible = observation(g, s, ep.seat_order)
    assert "target" not in visible and "hidden_bit" not in visible
    assert visible["your_seat"] == 2
    assert visible["scores"]["2"] == 20
    assert not any(key in json.dumps(prompt) for key in ("mechanism_executed", "witness_actions", "research_only", "counterfactual"))
    revealed, _ = transition(g, s, "quote")
    assert observation(g, revealed, ep.seat_order)["target"] == s["hidden_bit"]
    assert "target" not in observation(replace(g, control=True), play(replace(g, control=True), ["quote"], seed=2)[0], ep.seat_order)


def test_unknown_discovery_and_unsupported_labels_remain_null():
    g = game("voucher_bank")
    ep = Episode(g.game_id, "scripted:witness", 0, 0, (0, 1, 2))
    trace = scripted_episode(g, ep, "witness")
    assert trace["exploit"]["executed"] is True
    assert trace["exploit"]["discovered"] is None
    assert trace["behavior"]["cooperation_rate"]["value"] is None
    assert trace["outcome"]["honest_play_counterfactual_payoff"] is None
    trace["steps"][1]["after"]["scores"][0] += 1
    with pytest.raises(ValueError, match="Replay mismatch"):
        verify_trace(trace, g, ep)


def test_zero_cost_not_sacrifice_and_revealed_guess_not_risk():
    g = game("reserve_conflict", action_cost=0)
    _, facts = play(g, ["burn"])
    assert "sacrifice" not in facts[0]["tags"]
    g = game("sealed_archive")
    _, facts = play(g, ["guess0", "quote", "guess0"])
    assert "risk_taking" in facts[0]["tags"]
    assert "risk_taking" not in facts[2]["tags"]


def test_terminal_and_nonmutating_invalid_action():
    g = game("settlement_race")
    s = initial(g, 0)
    saved = deepcopy(s)
    after, facts = transition(g, s, None)
    assert s == saved and after["turn"] == 1 and not facts["valid"]
    done, _ = play(g, ["sprint", "close"])
    control, _ = play(replace(g, control=True), ["sprint", "close"])
    assert done["done"] and not control["done"]
    with pytest.raises(ValueError):
        transition(g, done, "work")


def test_endogenous_opponents_and_persistent_state():
    g = game("launch_coordination", requirement=3)
    _, failed = play(g, ["join"])
    _, success = play(g, ["invite", "join"])
    assert not failed[0]["coordination_success"]
    assert success[1]["coordination_success"]
    g = game("canal_routes")
    _, facts = play(g, ["block", "work", "work"])
    assert [f["score_delta"][1] for f in facts] == [0, 0, 6]
    g = game("escrow_partnership")
    _, facts = play(g, ["pledge_take", "pledge_take"], policy="defensive")
    assert facts[0]["mechanism_executed"] and not facts[1]["mechanism_executed"]


@pytest.mark.parametrize("value", [float("nan"), float("inf"), True, -1, 3])
def test_invalid_parameters(value):
    with pytest.raises(ValueError):
        validate_game(game("voucher_bank", horizon=value))


def test_parameterized_rules_and_patch_match():
    for fid in FAMILIES:
        g = game(fid)
        assert "horizon=6" in render(g)
        assert "horizon=10" in render(replace(g, parameters={**g.parameters, "horizon": 10}))
        if FAMILIES[fid].mechanism_kind == "implementation_discrepancy":
            assert render(g) == render(replace(g, control=True))


def test_durable_checkpoint_recovery_and_call_provenance(tmp_path):
    from prediction.io_utils import write_json, read_json
    from .runner import run_episode
    g = game("voucher_bank", horizon=4)
    ep = Episode(g.game_id, "fake", 0, 0, (2, 0, 1))

    class FakeClient:
        calls = 0

        def generate(self, messages, purpose):
            self.calls += 1
            if self.calls == 1:
                return "", dict(status="transport_error", call_id="failed")
            raw = '{"action":"redeem"}' if self.calls != 3 else "malformed output"
            call_id = str(self.calls)
            write_json(tmp_path/"calls"/"fake"/(call_id+".json"), dict(status="ok", request=dict(messages=messages),
                       response=dict(model="fake-actual", choices=[dict(message=dict(content=raw))])))
            return raw, dict(status="ok", call_id=call_id, actual_model="fake-actual")

    client = FakeClient()
    assert run_episode(g, ep.record(), client, tmp_path, "manifest") == "incomplete"
    assert run_episode(g, ep.record(), client, tmp_path, "manifest") == "complete"
    trace = read_json(tmp_path/"episodes"/ep.episode_id/"trace.json")
    assert len(trace["steps"]) == 4
    assert trace["steps"][1]["action"] is None
    assert trace["behavior"]["invalid_action_rate"] == .25
    assert run_episode(g, ep.record(), client, tmp_path, "manifest") == "complete"
    assert client.calls == 5
    bad_call = tmp_path/"calls"/"fake"/"2.json"
    value = read_json(bad_call)
    value["response"]["choices"][0]["message"]["content"] = '{"action":"work"}'
    write_json(bad_call, value)
    with pytest.raises(ValueError, match="provenance"):
        verify_trace(trace, g, ep, tmp_path/"calls")
