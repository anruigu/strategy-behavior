"""One negotiation, played by any mix of scripted and model seats.

Deliberately a near-copy of `hole_exp/run_crossplay.py::play`, down to the
message construction, so a delegation episode and a crossplay episode are the
same object as far as sampling is concerned: one system prompt, one user turn
holding the whole transcript to date (the observation wrapper has already
accumulated it -- rebuilding a message list here would restate the game once per
turn and grow quadratically), and `core.BREVITY` appended identically in every
condition.

WHAT COUNTS AS AN ENDING. Exactly one of three things fills
`game_state["principal_payoff"]`: a deal, the turn limit, or the error
allowance running out. The third leaves the payoff unset, because upstream's
`set_invalid_move` ends the episode without going through either of the env's
ending hooks; that case is caught here, scored at the BATNAs like a no-deal, and
flagged `broken` with the seat that did it. Scoring it as a deal-less episode
and NOT flagging it would let a model that cannot emit the action grammar look
like a model that principledly walked away.
"""
from __future__ import annotations

import pathlib
import sys
from typing import Callable, Dict, List, Optional, Sequence

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "hole_exp"))

import re  # noqa: E402

import textarena as ta  # noqa: E402

import core  # noqa: E402  (hole_exp/core.py -- shared prompts and helpers)
import counterparts as C  # noqa: E402
import delegation_env as DE  # noqa: E402
import scenarios as S  # noqa: E402

# The negotiation is role-play, not "a game against another player", so the
# suite's DOMAIN_NEUTRAL system prompt is the right one of the two; it is held
# fixed across every arm and model for the same reason core.py holds its own.
SYSTEM = core.DOMAIN_NEUTRAL

# A seat factory: (env, scenario, player_id, seed) -> object with .act(msgs, meta)
SeatFactory = Callable[..., object]

# Upstream's proposal pattern matches the FIRST eight letters after [Propose],
# so a nine-letter package is silently truncated to eight and scored as a
# perfectly valid contract the agent never wrote, while a seven-letter one is a
# plain invalid move. The first is the dangerous one -- it is a measurement
# error that leaves no trace -- so both are counted here and reported.
_PROPOSE = re.compile(r"\[Propose\]\s*((?:[A-E] ?){2,})", re.I)


def scripted_seat(kind: str) -> SeatFactory:
    builder = C.BUILDERS[kind]
    return lambda env, sc, pid, seed: builder(env, sc, pid, seed)


def model_seat(model: str, temperature: float = 0.7, max_tokens: int = 700,
               reasoning: bool = False) -> SeatFactory:
    """A live OpenRouter seat. `max_tokens` is well above the suite's usual 384:
    a turn here is a rationale plus a package, not a bracketed token, and
    `openrouter_actor`'s docstring records what silent truncation looks like."""
    import openrouter_actor  # noqa: PLC0415

    def build(env, sc, pid, seed):  # noqa: ARG001
        return openrouter_actor.build(model, temperature=temperature,
                                      max_tokens=max_tokens, seed=seed,
                                      reasoning=reasoning)[0]
    return build


def play_episode(scenario: S.Scenario, arm: str, seats: Dict[int, SeatFactory],
                 seed: int = 0, max_turns: int = 16, max_steps: int = 60,
                 deception_license: bool = False,
                 arms_per_seat: Optional[Dict[int, str]] = None) -> Dict:
    env = DE.build_env(scenario, arm, max_turns=max_turns,
                       deception_license=deception_license, arms=arms_per_seat)
    sc = env.scenario                      # carries the arm's mandates
    wrapped = ta.wrappers.LLMObservationWrapper(env)
    wrapped.reset(num_players=2, seed=seed)

    actors = {p: seats[p](env, sc, p, seed) for p in (0, 1)}
    actions: Dict[int, List[str]] = {0: [], 1: []}
    invalid: Dict[int, int] = {0: 0, 1: 0}
    length_errors: Dict[int, int] = {0: 0, 1: 0}
    transcript: List[str] = []

    done, steps = False, 0
    while not done and steps < max_steps:
        steps += 1
        pid, obs = wrapped.get_observation()
        text = obs if isinstance(obs, str) else "\n".join(
            f"[{'GAME' if e[0] == ta.GAME_ID else f'Player {e[0]}'}] {e[1]}"
            for e in obs)
        msgs = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": text + core.BREVITY}]
        try:
            raw = actors[pid].act(msgs, {"turn": steps, "pid": pid})
        except Exception as e:  # noqa: BLE001 - one bad turn must not void the episode
            raw = ""
            invalid[pid] += 1
            transcript.append(f"--- ERROR p{pid}: {type(e).__name__}: {e}")
        actions[pid].append(raw)
        for m in _PROPOSE.finditer(raw or ""):
            if len(re.sub(r"[^A-Ea-e]", "", m.group(1))) != len(env.issues):
                length_errors[pid] += 1
        transcript.append(f"--- p{pid} ({env.briefs[pid].principal_role}'s agent)\n{raw}")
        before = env.state.error_count
        n_props = len(env.state.game_state["proposal_history"])
        done, _ = wrapped.step(raw)
        # Mirror the env's decoded echo into the saved trace. Without it the
        # transcript on disk shows only the raw letters and an off-by-one read
        # is invisible to whoever audits a flagged episode.
        history = env.state.game_state["proposal_history"]
        if len(history) > n_props:
            env_choices = history[-1]["choices"]
            transcript.append("--- GAME  package on the table: " + ", ".join(
                f"{i} {env.letter_choices[i][env_choices[i]]} ({env_choices[i]})"
                for i in env.issues))
        if env.state.game_state.get("outcome") is None and env.state.error_count > before:
            invalid[pid] += 1

    rewards, game_info = wrapped.close()
    gs = env.state.game_state
    broken_by = None
    if gs.get("principal_payoff") is None:
        # The error allowance ran out (or the loop hit `max_steps`).
        broken_by = next((p for p in (0, 1)
                          if env.state.game_info[p].get("invalid_move")), None)
        gs["principal_payoff"] = {0: sc.batna[0], 1: sc.batna[1]}
        gs["outcome"] = "invalid" if broken_by is not None else "no_deal"

    return {
        "scenario": sc.name, "family": sc.family, "arm": arm, "seed": seed,
        "arms_per_seat": {p: env.briefs[p].arm for p in (0, 1)},
        "outcome": gs["outcome"],
        "contract": gs.get("accepted_contract"),
        "payoff": {int(p): float(v) for p, v in gs["principal_payoff"].items()},
        "turns": int(env.state.turn),
        "steps": steps,
        "n_actions": {p: len(a) for p, a in actions.items()},
        "invalid": dict(invalid),
        "proposal_length_errors": dict(length_errors),
        "invalid_rate": {p: (invalid[p] / len(actions[p])) if actions[p] else None
                         for p in (0, 1)},
        "broken_by": broken_by,
        "ta_rewards": {int(k): float(v) for k, v in (rewards or {}).items()},
        "game_info": {int(p): dict(v) for p, v in (game_info or {}).items()},
        "actions": actions,
        "transcript": "\n".join(transcript),
    }


def reference_payoff(scenario: S.Scenario, arm: str, learner_id: int,
                     partner: str, seed: int = 0, max_turns: int = 16) -> Dict:
    """Replay the same cell with a perfectly faithful scripted seat in the
    learner's chair. The number a real policy is normalised against, produced by
    the SAME `play_episode` on the SAME seed, so it cannot drift from the
    situation it describes (`core.attach_references`' rule)."""
    seats = {learner_id: scripted_seat("principled"),
             1 - learner_id: scripted_seat(partner)}
    return play_episode(scenario, arm, seats, seed=seed, max_turns=max_turns)
