#!/usr/bin/env python3
"""Differential test: this port vs spiral's own `train_spiral.py`, same inputs.

The Tinker arm re-implements two pieces of `SelfPlayActor` that decide what the
model is actually trained on:

  - `extract_action`      raw model text -> a legal action (or a forfeit)
  - `prepare_trajectories` game outcome -> per-turn advantages, via RAE

Everything else (envs, template, valid-action parsers) is imported from spiral
directly and cannot drift. These two can, and both fail quietly: loosen the
action parser and the forfeit rate drops, which changes the reward distribution
without changing anything you would notice in a log line; get the RAE
read-then-update order backwards and the baseline is biased toward zero.

So: bind spiral's own unbound methods to a stub `self`, run both against
identical inputs, and diff.

This has to run under $SAT_VENV (py3.10 + oat + vllm), because importing
`train_spiral` pulls oat and vllm. That is the only thing here that needs the
heavy venv -- the arm itself never imports either.

    "$SAT_VENV/bin/python" test_parity.py --spiral-dir "$SPIRAL_DIR"
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).parent))

from config import build_config  # noqa: E402
from selfplay import (  # noqa: E402
    INVALID_ACTION,
    RoleBaseline,
    Sampled,
    game_to_training_turns,
    import_spiral,
    play_game,
)


def _stub_actor(cfg, role_baseline_ema=None, train_spiral=None):
    """A SimpleNamespace carrying exactly the attributes the two methods read."""
    helpers = {}
    if train_spiral is not None:
        # prepare_trajectories calls back into this one; bind spiral's real
        # implementation so the stub does not accidentally become the thing
        # under test.
        helpers["compute_token_level_rewards"] = (
            lambda ids, r: train_spiral.SelfPlayActor.compute_token_level_rewards(
                None, ids, r
            )
        )
    return SimpleNamespace(
        **helpers,
        args=SimpleNamespace(
            prompt_template=cfg.prompt_template,
            fixed_opponent="",
            reward_scaling=cfg.reward_scaling,
            use_role_baseline=cfg.use_role_baseline,
            use_intermediate_rewards=cfg.use_intermediate_rewards,
            gamma=cfg.gamma,
            filter_zero_adv=cfg.filter_zero_adv,
            ignore_no_eos=cfg.ignore_no_eos,
        ),
        role_baseline_ema=role_baseline_ema,
        online_model_player=0,
    )


# --- part 1: extract_action -------------------------------------------------

# Realistic model outputs. The awkward ones are the point: a bare word, a
# 5-word phrase (the bracket heuristic's boundary), a \boxed{} inside prose,
# nested/none, and text that is legal-looking but not in the action space.
RESPONSE_CORPUS = [
    "I should bet here. \\boxed{Bet}",
    "Reasoning: pot odds favour calling.\n\nFinal answer: \\boxed{Call}",
    "\\boxed{Check}",
    "\\boxed{Fold}",
    "check",
    "Check",
    "I will check now",
    "The best move here is definitely to just check quietly",  # >5 words
    "<think>hmm</think> \\boxed{Bet}",
    "\\boxed{ Bet }",
    "\\boxed{}",
    "",
    "no action at all",
    "\\boxed{Raise}",  # not in Kuhn's action space
    "\\boxed{[Bet]}",
    "Let me think.  \\boxed{Call}  and that's final.",
    "\\boxed{3}",
    "I'll play \\boxed{4} because the centre is open",
    "\\boxed{0}\n\\boxed{8}",  # last one wins
]


def test_extract_action(cfg, train_spiral, observations) -> tuple[int, int]:
    from spiral.agents.utils import get_valid_action_parser

    import selfplay

    actor = _stub_actor(cfg)
    checked = mismatches = 0

    for env_id, observation in observations:
        try:
            action_space = get_valid_action_parser(env_id)(observation)
        except Exception:
            continue
        for text in RESPONSE_CORPUS:
            theirs = train_spiral.SelfPlayActor.extract_action(
                actor, text, action_space
            )
            ours = selfplay.extract_action(text, action_space, cfg.prompt_template)
            checked += 1
            if theirs != ours:
                mismatches += 1
                print(
                    f"  MISMATCH [{env_id}] text={text!r}\n"
                    f"    spiral={theirs!r}\n    port  ={ours!r}"
                )

    # extract_chat_action has no action-space argument; check it separately.
    for text in RESPONSE_CORPUS:
        theirs = train_spiral.SelfPlayActor.extract_chat_action(actor, text)
        ours = selfplay.extract_chat_action(text)
        checked += 1
        if theirs != ours:
            mismatches += 1
            print(f"  MISMATCH [chat] text={text!r}\n    spiral={theirs!r}\n    port  ={ours!r}")

    return checked, mismatches


# --- part 2: prepare_trajectories (RAE + discounting + filtering) ------------


def _game_state_from(game, train_spiral):
    """Rebuild spiral's GameState from one of our GameResults."""
    from spiral.utils import GameState

    gs = GameState(max_context_length=32768, max_turns=50)
    ordered = sorted(
        (t for ts in game.turns.values() for t in ts), key=lambda t: t.turn_index
    )
    for t in ordered:
        gs.add_trajectory_data(
            t.player_id,
            {
                "prompt": "",
                "action": t.action,
                "action_is_valid": t.action_is_valid,
                "player_id": t.player_id,
                "turn": t.turn_index,
                "formatted_observation": "",
                "prompt_ids": t.prompt_ids,
                "response": t.response_text,
                "response_ids": t.response_ids,
                "response_logprobs": t.response_logprobs,
                "response_is_truncated": t.truncated,
            },
        )
        gs.turn_count += 1
    return gs


def test_prepare_trajectories(cfg, train_spiral, games) -> tuple[int, int]:
    from spiral.utils import EMA

    # Two independent baselines fed the same games in the same order, so any
    # divergence is in the shaping, not in what each one has seen.
    their_ema = {
        env_id: {0: EMA(cfg.role_baseline_ema_gamma), 1: EMA(cfg.role_baseline_ema_gamma)}
        for env_id in cfg.env_ids
    }
    actor = _stub_actor(cfg, their_ema, train_spiral)
    our_baseline = RoleBaseline(cfg.env_ids, cfg.role_baseline_ema_gamma)

    checked = mismatches = 0
    for game in games:
        gs = _game_state_from(game, train_spiral)
        theirs = train_spiral.SelfPlayActor.prepare_trajectories(
            actor, gs, game.rewards, game.env_id
        )
        ours = game_to_training_turns(
            game,
            our_baseline,
            reward_scaling=cfg.reward_scaling,
            gamma=cfg.gamma,
            use_intermediate_rewards=cfg.use_intermediate_rewards,
            filter_zero_adv=cfg.filter_zero_adv,
            ignore_no_eos=cfg.ignore_no_eos,
        )

        checked += 1
        # spiral puts the whole turn return on the last response token; the
        # advantage we hand Tinker is that same scalar. `loss_mask=False`
        # (a truncated response under --ignore_no_eos) means oat computes no
        # loss for that trajectory, which on Tinker is a zero advantage -- so
        # compare the *effective* per-turn gradient weight on both sides.
        their_adv = [t.rewards[-1] * (1.0 if t.loss_mask else 0.0) for t in theirs]
        our_adv = [t.advantage for t in ours]
        if len(their_adv) != len(our_adv):
            mismatches += 1
            print(
                f"  MISMATCH kept-turn count [{game.env_id}]: "
                f"spiral={len(their_adv)} port={len(our_adv)}"
            )
            continue
        for i, (a, b) in enumerate(zip(their_adv, our_adv)):
            if abs(a - b) > 1e-9:
                mismatches += 1
                print(f"  MISMATCH advantage[{i}] [{game.env_id}]: spiral={a} port={b}")
                break

    # The baselines themselves must also have tracked identically.
    ours_snap = our_baseline.snapshot()
    for env_id, per_seat in their_ema.items():
        for pid, ema in per_seat.items():
            checked += 1
            if abs(ema.get() - ours_snap[env_id][pid]) > 1e-9:
                mismatches += 1
                print(
                    f"  MISMATCH baseline [{env_id}][{pid}]: "
                    f"spiral={ema.get()} port={ours_snap[env_id][pid]}"
                )
    return checked, mismatches


# --- driver -----------------------------------------------------------------


class _StubSampler:
    """Random legal action, emitted as \\boxed{...} -- same as --dry-run."""

    def __init__(self, env_id, rng):
        self.env_id = env_id
        self.rng = rng

    def __call__(self, prompt_text):
        from spiral.agents.random import RandomAgent

        start = prompt_text.find("Observation: ") + len("Observation: ")
        end = prompt_text.find("\nPlease reason step by step", start)
        observation = prompt_text[start:end] if end > 0 else prompt_text[start:]
        try:
            action = RandomAgent(self.env_id)(observation)
        except Exception:
            action = "[Accept]"
        # Mix in the responses the parser finds hardest, at a realistic rate.
        roll = self.rng.random()
        if roll < 0.10:
            text = action.strip("[]")  # unbracketed bare word
        elif roll < 0.15:
            text = "I am not going to answer that"  # forfeit
        else:
            text = f"Thinking about it. \\boxed{{{action.strip('[]')}}}"
        ids = [ord(c) % 1000 for c in text] or [0]
        return Sampled(
            prompt_ids=[1, 2, 3],
            response_ids=ids,
            response_logprobs=[-0.5] * len(ids),
            text=text,
            truncated=self.rng.random() < 0.05,
        )


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--arm", default="kuhn")
    p.add_argument("--games", type=int, default=12)
    p.add_argument("--seed", type=int, default=5)
    p.add_argument("--spiral-dir", default="")
    args = p.parse_args(argv)

    cfg = build_config(args.arm, "full", {})
    spiral_dir = args.spiral_dir or str(Path(__file__).resolve().parents[3] / "spiral")
    import_spiral(spiral_dir)

    print("importing train_spiral (pulls oat + vllm; slow) ...")
    import train_spiral  # noqa: PLC0415

    rng = random.Random(args.seed)
    random.seed(args.seed)

    print(f"\nplaying {args.games} games on arm={args.arm} ...")
    games = []
    observations = []
    for i in range(args.games):
        env_id = cfg.env_ids[i % len(cfg.env_ids)]
        game = play_game(
            env_id,
            cfg.env_to_llm_obs_wrapper[env_id],
            _StubSampler(env_id, rng),
            seed=rng.randrange(2**31),
            max_turns=cfg.max_turns,
            template=cfg.prompt_template,
        )
        games.append(game)
        # Recover observations for the extract_action corpus: the parsers key
        # off the observation, so use ones that really occurred.
        for ts in game.turns.values():
            for _t in ts[:2]:
                observations.append((env_id, _t.response_text))
    observations = observations[:6]

    # Real observations for the parser corpus, straight from a fresh env.
    from spiral.envs import make_env

    real_obs = []
    for env_id in cfg.env_ids:
        env = make_env(env_id, use_llm_obs_wrapper=cfg.env_to_llm_obs_wrapper[env_id])
        env.reset(num_players=2, seed=args.seed)
        _pid, obs = env.get_observation()
        real_obs.append((env_id, obs))

    total = fails = 0
    print("\n[1/2] extract_action / extract_chat_action")
    c, m = test_extract_action(cfg, train_spiral, real_obs)
    print(f"      {c} comparisons, {m} mismatches")
    total += c
    fails += m

    print("\n[2/2] prepare_trajectories (RAE + discounting + filtering)")
    c, m = test_prepare_trajectories(cfg, train_spiral, games)
    print(f"      {c} comparisons, {m} mismatches")
    total += c
    fails += m

    kept = sum(
        len(
            game_to_training_turns(
                g, None,
                reward_scaling=cfg.reward_scaling, gamma=cfg.gamma,
                use_intermediate_rewards=cfg.use_intermediate_rewards,
                filter_zero_adv=False, ignore_no_eos=cfg.ignore_no_eos,
            )
        )
        for g in games
    )
    print(
        f"\ncorpus: {len(games)} games, "
        f"{sum(g.num_turns for g in games)} turns, {kept} trainable, "
        f"{sum(g.num_invalid for g in games)} forfeits"
    )
    print("=" * 60)
    print(f"{'PASS' if fails == 0 else 'FAIL'}: {total - fails}/{total} matched")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
