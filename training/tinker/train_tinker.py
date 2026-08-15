#!/usr/bin/env python3
"""SPIRAL self-play on the Tinker training API.

The oat/slurm path in `../` needs an 8xGPU node: vLLM for rollouts, DeepSpeed
for the policy update, and a pile of cluster-specific workarounds (fused_adam
JIT races, node-local $HOME, nltk's cwd import guard). This runs the same
self-play loop with Tinker doing sampling and gradients remotely, so the only
thing that runs locally is the TextArena game loop -- which is pure-Python and
CPU-only.

Shape of a policy step, mirroring `SelfPlayActor.step`:

  1. snapshot the current weights into a sampling client
  2. play whole games until we have >= turns_per_step model turns, then
     subsample to exactly that many (oat's --rollout_batch_size counts turns)
  3. shape each game's outcome with the per-(env, seat) RAE baseline
  4. one Datum per turn -> forward_backward + optim_step, num_ppo_epochs times

Usage:

    export TINKER_API_KEY=...
    python train_tinker.py --arm kuhn --scale full
    python train_tinker.py --arm kuhn --scale smoke --dry-run   # no API calls

Reference for the Tinker call sequence: https://github.com/Guanghan/JustTinker
(`scripts/tinker/justrl_math_reasoning.py`). What that repo does single-turn
with a verifiable math reward, this does multi-turn with a game outcome. See
`make_datum` for the one place we deliberately do not follow it.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

import selfplay  # module handle: _register_ipd_prompt mutates its prompt registry
from config import ARMS, SCALES, SpiralTinkerConfig, build_config
from selfplay import (
    GameResult,
    RoleBaseline,
    Sampled,
    TrainingTurn,
    game_to_training_turns,
    import_spiral,
    play_games_concurrently,
    require_action_parser,
)

# --- Tinker plumbing --------------------------------------------------------


def _load_tinker():
    try:
        import tinker
    except ImportError as e:
        raise SystemExit(
            "tinker is not installed: pip install -r requirements.txt\n"
            "(and export TINKER_API_KEY=...)"
        ) from e
    return tinker


def load_tokenizer(model_name: str):
    """Get a tokenizer for `model_name`, preferring Tinker's own resolution.

    Tinker model ids are HF repo ids for the open models, so AutoTokenizer works
    as a fallback -- but not for every id on the list (`:peft:` suffixes, and
    Thinking Machines' own models), which is why the cookbook helper is tried
    first.
    """
    try:
        from tinker_cookbook import tokenizer_utils

        return tokenizer_utils.get_tokenizer(model_name)
    except Exception as e:  # noqa: BLE001 - fall through to HF
        print(f"[tokenizer] tinker_cookbook lookup failed ({e}); trying HF")
    try:
        from transformers import AutoTokenizer

        return AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    except Exception as e:  # noqa: BLE001
        raise SystemExit(
            f"could not load a tokenizer for {model_name!r}: {e}\n"
            "If this is a gated HF repo, run `huggingface-cli login` first."
        ) from e


class TinkerSampler:
    """Adapts a Tinker sampling client to selfplay.TurnSampler.

    One call == one model turn. The `stop` sequence is `<|im_end|>` because
    spiral's qwen3 template wraps the observation in ChatML and ends the prompt
    at `<|im_start|>assistant\\n`; on a *base* model those tokens exist in the
    vocab but nothing guarantees the model emits EOS, so without an explicit
    stop every turn runs to generate_max_length and every turn then gets dropped
    by `ignore_no_eos`. That failure is silent: the loss is computed over an
    empty batch and the win rate sits at chance.
    """

    def __init__(
        self,
        sampling_client: Any,
        tokenizer: Any,
        *,
        max_tokens: int,
        temperature: float,
        top_p: float,
        max_prompt_tokens: int,
    ) -> None:
        tinker = _load_tinker()
        self._tinker = tinker
        self._client = sampling_client
        self._tok = tokenizer
        self._max_prompt_tokens = max_prompt_tokens
        stop = self._stop_tokens(tokenizer)
        kwargs = dict(max_tokens=max_tokens, temperature=temperature, stop=stop)
        try:
            self._params = tinker.SamplingParams(top_p=top_p, **kwargs)
        except TypeError:
            # top_p is not in every SamplingParams revision. The training arms
            # pass --top_p 1 (a no-op), so losing it only affects eval, where
            # oat uses 0.95. Say so rather than dying mid-run.
            print("[sampler] SamplingParams has no top_p; ignoring it")
            self._params = tinker.SamplingParams(**kwargs)
        self.over_budget = 0

    @staticmethod
    def _stop_tokens(tokenizer: Any) -> list[int]:
        ids = tokenizer.encode("<|im_end|>", add_special_tokens=False)
        if not ids:
            raise SystemExit(
                "this tokenizer has no <|im_end|> token, so spiral's ChatML "
                "prompt template cannot be stopped cleanly -- use a Qwen model "
                "or change --prompt-template"
            )
        return [ids[0]]

    def __call__(self, prompt_text: str) -> Sampled | None:
        prompt_ids = self._tok.encode(prompt_text, add_special_tokens=False)
        if len(prompt_ids) > self._max_prompt_tokens:
            self.over_budget += 1
            return None

        model_input = self._tinker.ModelInput.from_ints(prompt_ids)
        result = self._client.sample(
            prompt=model_input, sampling_params=self._params, num_samples=1
        ).result()
        seq = result.sequences[0]
        response_ids = list(seq.tokens)
        logprobs = list(seq.logprobs) if seq.logprobs is not None else [0.0] * len(
            response_ids
        )
        return Sampled(
            prompt_ids=list(prompt_ids),
            response_ids=response_ids,
            response_logprobs=logprobs,
            text=self._tok.decode(response_ids, skip_special_tokens=False),
            truncated=getattr(seq, "stop_reason", None) == "length",
        )


class StubSampler:
    """Offline stand-in for --dry-run: picks a uniformly random legal action.

    Emits it as `\\boxed{...}` so the real extraction path in
    selfplay.action_from_response is exercised end to end. This is what makes it
    possible to check the template, the parsers, the reward overrides and the
    Datum alignment without spending anything.
    """

    def __init__(self, env_id: str, tokenizer: Any, rng: random.Random) -> None:
        self._env_id = env_id
        self._tok = tokenizer
        self._rng = rng

    def __call__(self, prompt_text: str) -> Sampled | None:
        from spiral.agents.random import RandomAgent

        observation = _observation_from_prompt(prompt_text)
        try:
            action = RandomAgent(self._env_id)(observation)
        except Exception:  # noqa: BLE001 - freeform envs have no parser
            action = "[Accept]"
        text = f"Reasoning about the position. \\boxed{{{action.strip('[]')}}}"
        prompt_ids = self._tok.encode(prompt_text, add_special_tokens=False)
        response_ids = self._tok.encode(text, add_special_tokens=False)
        return Sampled(
            prompt_ids=list(prompt_ids),
            response_ids=list(response_ids),
            response_logprobs=[-0.5] * len(response_ids),
            text=text,
            truncated=False,
        )


def _observation_from_prompt(prompt_text: str) -> str:
    """Recover the raw observation from a rendered spiral prompt (dry-run only).

    The `/no_think` marker has to come back off. `kuhn_poker_parse_available_actions`
    and `pig_dice_parse_available_actions` both read the *last line* of the
    observation, so leaving the marker on would hand the stub an empty action
    space and report a 100% invalid-action rate that the real sampler does not
    have. In the live path this cannot happen -- `_format_observation` appends
    the marker to a local copy, and the parsers are always given the untouched
    observation straight from the env.
    """
    from selfplay import NO_THINK_MARKER

    start = prompt_text.find("Observation: ")
    if start < 0:
        return prompt_text
    start += len("Observation: ")
    end = prompt_text.find("\nPlease reason step by step", start)
    obs = prompt_text[start:end] if end > 0 else prompt_text[start:]
    if obs.endswith(NO_THINK_MARKER):
        obs = obs[: -len(NO_THINK_MARKER)]
    return obs


class _ByteTokenizer:
    """Last-resort tokenizer so --dry-run works with no network and no HF cache."""

    def encode(self, text: str, add_special_tokens: bool = False) -> list[int]:
        del add_special_tokens
        return list(text.encode("utf-8"))

    def decode(self, ids: list[int], skip_special_tokens: bool = False) -> str:
        del skip_special_tokens
        return bytes(i % 256 for i in ids).decode("utf-8", errors="replace")


# --- Datum assembly ---------------------------------------------------------


def make_datum(
    tinker: Any,
    torch: Any,
    prompt_ids: list[int],
    response_ids: list[int],
    response_logprobs: list[float],
    advantage: float,
) -> Any:
    """Build one training Datum for one model turn.

    Alignment follows the tinker-cookbook convention
    (`rl/data_processing.py::trajectory_to_data`): the model input is
    right-shifted and everything else is left-shifted, i.e. for a full sequence
    `tokens = prompt + response` of length N,

        model_input   = tokens[:-1]                      # position i sees tokens[:i+1]
        target_tokens = tokens[1:]                       # position i predicts tokens[i+1]
        logprobs      = per_token_logprobs[1:]
        advantages    = per_token_advantages[1:]

    where the per-token arrays are `[0.0] * len(prompt) + <per response token>`.
    Zero advantage on the prompt positions is what masks the observation out of
    the loss; there is no separate mask key.

    NOTE, because this is the one place we knowingly diverge from the JustTinker
    reference: JustTinker builds these as `[0] * ob_len + tokens[ob_len:]` with
    `ob_len = prompt_len - 1`, truncated to `len(input_tokens)`. Expanding that
    gives `[0] * ob_len + [prompt[-1]] + response[:-1]` -- one position further
    right than `tokens[1:]`. With that offset the target at position i is
    `tokens[i]`, a token the model can already see in its own input, so the
    surrogate objective is computed against a token that requires no prediction.
    Its `logprobs` array carries the same extra shift, so the two stay mutually
    consistent and nothing raises; it just does not train the thing you meant.
    We use the cookbook alignment above.

    One Datum per turn, never merged: spiral's template re-renders the whole
    observation inside a fresh `<|im_start|>user ... <|im_end|>` block, so turn
    t+1's prompt is not a token-prefix extension of turn t's prompt+response and
    the cookbook's multi-turn merging path does not apply.
    """
    tokens = list(prompt_ids) + list(response_ids)
    n_prompt = len(prompt_ids)

    if len(response_logprobs) != len(response_ids):
        # Defensive: a provider that returns no logprobs would otherwise produce
        # a ratio of exp(logp_train - 0) = exp(logp_train) and blow up the clip.
        raise ValueError(
            f"logprob/token length mismatch: {len(response_logprobs)} vs "
            f"{len(response_ids)}"
        )

    per_token_logprobs = [0.0] * n_prompt + list(response_logprobs)
    per_token_advantages = [0.0] * n_prompt + [advantage] * len(response_ids)

    input_tokens = tokens[:-1]
    target_tokens = tokens[1:]
    logprobs = per_token_logprobs[1:]
    advantages = per_token_advantages[1:]
    assert len(input_tokens) == len(target_tokens) == len(logprobs) == len(advantages)

    return tinker.Datum(
        model_input=tinker.ModelInput.from_ints(input_tokens),
        loss_fn_inputs={
            "target_tokens": tinker.TensorData.from_torch(
                torch.tensor(target_tokens, dtype=torch.long)
            ),
            "logprobs": tinker.TensorData.from_torch(
                torch.tensor(logprobs, dtype=torch.float32)
            ),
            "advantages": tinker.TensorData.from_torch(
                torch.tensor(advantages, dtype=torch.float32)
            ),
        },
    )


# --- collection -------------------------------------------------------------


def collect_batch(
    cfg: SpiralTinkerConfig,
    sampler_factory,
    baseline: RoleBaseline | None,
    rng: random.Random,
) -> tuple[list[TrainingTurn], list[GameResult]]:
    """Play games until we have >= turns_per_step trainable turns, then subsample.

    Port of `SelfPlayActor.step`: it loops over a shuffled copy of `env_ids`
    (shuffled to avoid order bias when an arm trains on several games at once),
    plays a game of each, and stops once it has enough turns.

    Two differences, both forced by the remote-sampling model:
      - games are played in concurrent waves rather than one at a time, so a
        wave can overshoot turns_per_step. oat overshoots too and subsamples the
        same way, so the batch composition is unaffected.
      - `max_games_per_step` bounds the loop. oat's `for i in range(int(1e9))`
        is fine when a broken rollout crashes; here a broken *action parser*
        just makes every game one turn long, and the loop would spend real money
        forever.
    """
    turns: list[TrainingTurn] = []
    games: list[GameResult] = []
    games_played = 0
    wave = max(1, cfg.max_concurrent_games)

    while len(turns) < cfg.turns_per_step and games_played < cfg.max_games_per_step:
        env_ids = list(cfg.env_ids)
        rng.shuffle(env_ids)
        specs: list[tuple[str, bool, int]] = []
        for i in range(wave):
            env_id = env_ids[i % len(env_ids)]
            specs.append(
                (env_id, cfg.env_to_llm_obs_wrapper[env_id], rng.randrange(2**31))
            )

        wave_games = play_games_concurrently(
            specs,
            sampler_factory,
            max_workers=cfg.max_concurrent_games,
            max_turns=cfg.max_turns,
            template=cfg.prompt_template,
            no_think=cfg.suppress_thinking,
        )
        games_played += len(wave_games)
        games.extend(wave_games)

        # In spec order, so the RAE baseline sees games in a reproducible order.
        for game in wave_games:
            turns.extend(
                game_to_training_turns(
                    game,
                    baseline,
                    reward_scaling=cfg.reward_scaling,
                    gamma=cfg.gamma,
                    use_intermediate_rewards=cfg.use_intermediate_rewards,
                    filter_zero_adv=cfg.filter_zero_adv,
                    ignore_no_eos=cfg.ignore_no_eos,
                )
            )

    if len(turns) > cfg.turns_per_step:
        idx = rng.sample(range(len(turns)), cfg.turns_per_step)
        turns = [turns[i] for i in sorted(idx)]
    return turns, games


def batch_metrics(turns: list[TrainingTurn], games: list[GameResult]) -> dict[str, float]:
    import statistics

    outcomes: dict[str, int] = {}
    for g in games:
        outcomes[g.outcome] = outcomes.get(g.outcome, 0) + 1

    model_turns = sum(len(ts) for g in games for ts in g.turns.values())
    invalid = sum(g.num_invalid for g in games)
    resp_lens = [len(t.response_ids) for t in turns]
    advs = [t.advantage for t in turns]
    raw = [t.info["final_reward"] for t in turns]

    m: dict[str, float] = {
        "games": float(len(games)),
        "train_turns": float(len(turns)),
        "model_turns": float(model_turns),
        "mean_game_length": float(statistics.fmean([g.num_turns for g in games]))
        if games
        else 0.0,
        "invalid_action_rate": (invalid / model_turns) if model_turns else 0.0,
        "draw_rate": (
            sum(1 for g in games if g.rewards.get(0) == g.rewards.get(1)) / len(games)
        )
        if games
        else 0.0,
        "mean_response_tokens": float(statistics.fmean(resp_lens)) if resp_lens else 0.0,
        "mean_advantage": float(statistics.fmean(advs)) if advs else 0.0,
        "mean_abs_advantage": float(statistics.fmean(abs(a) for a in advs))
        if advs
        else 0.0,
        "mean_raw_reward": float(statistics.fmean(raw)) if raw else 0.0,
    }
    for name, count in outcomes.items():
        m[f"outcome/{name}"] = count / len(games) if games else 0.0
    return m


# --- eval -------------------------------------------------------------------


def run_eval(
    cfg: SpiralTinkerConfig, sampler_factory, rng: random.Random
) -> dict[str, float]:
    """Model as `eval_player_id` vs a uniform-random legal-move opponent.

    oat's upstream default eval opponent is an OpenRouter LLM; all three run
    scripts pin `random` because the default model is retired and 404s, which
    aborts the job at the step-0 eval. `random` is a weak opponent, so read the
    win rate as "has the policy learned the game at all", not as a strength
    measurement.
    """
    from spiral.agents.random import RandomAgent

    out: dict[str, float] = {}
    for env_id in cfg.eval_env_ids:
        use_llm_obs = cfg.eval_env_to_llm_obs_wrapper[env_id]
        specs = [
            (env_id, use_llm_obs, rng.randrange(2**31)) for _ in range(cfg.eval_games)
        ]
        games = play_games_concurrently(
            specs,
            sampler_factory,
            max_workers=cfg.max_concurrent_games,
            max_turns=cfg.max_turns,
            template=cfg.prompt_template,
            model_player_id=cfg.eval_player_id,
            opponent_factory=lambda eid: RandomAgent(eid),
            no_think=cfg.suppress_thinking,
        )
        pid = cfg.eval_player_id
        wins = sum(1 for g in games if g.rewards.get(pid, 0) > g.rewards.get(1 - pid, 0))
        draws = sum(
            1 for g in games if g.rewards.get(pid, 0) == g.rewards.get(1 - pid, 0)
        )
        model_turns = sum(len(g.turns[pid]) for g in games)
        invalid = sum(
            1 for g in games for t in g.turns[pid] if not t.action_is_valid
        )
        n = max(1, len(games))
        out[f"eval/{env_id}/win_rate"] = wins / n
        out[f"eval/{env_id}/draw_rate"] = draws / n
        out[f"eval/{env_id}/invalid_action_rate"] = (
            invalid / model_turns if model_turns else 0.0
        )
    return out


# --- main -------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="SPIRAL self-play via the Tinker training API",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--arm", default="kuhn", choices=sorted(ARMS))
    p.add_argument("--scale", default="full", choices=sorted(SCALES))
    p.add_argument("--model", dest="model_name", default=None)
    p.add_argument("--lora-rank", dest="lora_rank", type=int, default=None)
    p.add_argument("--num-steps", dest="num_steps", type=int, default=None)
    p.add_argument("--turns-per-step", dest="turns_per_step", type=int, default=None)
    p.add_argument(
        "--max-concurrent-games", dest="max_concurrent_games", type=int, default=None
    )
    p.add_argument("--learning-rate", dest="learning_rate", type=float, default=None)
    p.add_argument("--loss-fn", dest="loss_fn", default=None,
                   choices=["ppo", "importance_sampling"])
    p.add_argument("--num-ppo-epochs", dest="num_ppo_epochs", type=int, default=None)
    p.add_argument("--eval-steps", dest="eval_steps", type=int, default=None)
    p.add_argument("--eval-games", dest="eval_games", type=int, default=None)
    p.add_argument("--save-steps", dest="save_steps", type=int, default=None)
    p.add_argument(
        "--thinking-mode", dest="thinking_mode", default=None,
        choices=["auto", "on", "off"],
        help="append /no_think to the observation. 'auto' enables it for "
             "hybrid-thinking Qwen3* instruct models, which otherwise never "
             "close their <think> block inside generate_max_length and forfeit "
             "every game",
    )
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--run-name", dest="run_name", default=None)
    p.add_argument("--output-dir", dest="output_dir", default=None)
    p.add_argument("--use-wb", dest="use_wandb", action="store_true", default=None)
    p.add_argument("--wb-project", dest="wandb_project", default=None)
    p.add_argument(
        "--generate-max-length", dest="generate_max_length", type=int, default=None
    )
    p.add_argument(
        "--no-role-baseline",
        dest="use_role_baseline",
        action="store_false",
        default=None,
        help="disable RAE; the ablation SPIRAL's paper reports as unstable",
    )
    p.add_argument(
        "--resume",
        default=None,
        help="tinker:// state path from a previous run's checkpoints.jsonl",
    )
    p.add_argument(
        "--spiral-dir",
        default=os.environ.get("SPIRAL_DIR", ""),
        help="spiral checkout to import envs/templates/parsers from "
        "(defaults to $SPIRAL_DIR)",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="play games with a random-action stub sampler; no Tinker calls, "
        "no API key needed. Verifies template/parsers/rewards/Datum shapes.",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    overrides = {
        k: v
        for k, v in vars(args).items()
        if k not in ("arm", "scale", "dry_run", "spiral_dir", "resume") and v is not None
    }
    cfg = build_config(args.arm, args.scale, overrides)

    spiral_dir = args.spiral_dir or str(
        Path(__file__).resolve().parents[3] / "spiral"
    )
    import_spiral(spiral_dir)
    for env_id in dict.fromkeys([*cfg.env_ids, *cfg.eval_env_ids]):
        require_action_parser(env_id)

    seed = cfg.seed if cfg.seed is not None else int(time.time_ns()) % (2**31)
    rng = random.Random(seed)
    random.seed(seed)  # spiral's parsers/RandomAgent use the module-level RNG

    run_dir = Path(cfg.output_dir) / f"{cfg.run_name}-{time.strftime('%Y%m%d_%H%M%S')}"
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "config.json").write_text(cfg.to_json())

    print("=" * 72)
    print(f"SPIRAL self-play on Tinker  |  arm={cfg.arm} scale={cfg.scale}")
    print("=" * 72)
    print(f"model          : {cfg.model_name} (LoRA rank {cfg.lora_rank})")
    print(f"thinking       : {cfg.thinking_mode} -> "
          f"{'/no_think appended' if cfg.suppress_thinking else 'left on'}")
    print(f"train envs     : {list(zip(cfg.env_ids, cfg.use_llm_obs_wrappers))}")
    print(f"eval  envs     : {list(zip(cfg.eval_env_ids, cfg.eval_use_llm_obs_wrappers))}")
    print(f"steps          : {cfg.num_steps} x {cfg.turns_per_step} turns")
    print(f"concurrency    : {cfg.max_concurrent_games} games in flight")
    print(f"seed           : {seed}")
    print(f"run dir        : {run_dir}")
    print("=" * 72)

    if args.dry_run:
        return _dry_run(cfg, rng, run_dir)

    if not os.environ.get("TINKER_API_KEY"):
        raise SystemExit("TINKER_API_KEY is not set")

    tinker = _load_tinker()
    import torch  # only used to build TensorData

    tokenizer = load_tokenizer(cfg.model_name)
    _register_ipd_prompt(cfg, tokenizer)

    print("connecting to Tinker ...")
    service_client = tinker.ServiceClient()
    training_client = service_client.create_lora_training_client(
        base_model=cfg.model_name, rank=cfg.lora_rank
    )
    start_step = 0
    if args.resume:
        print(f"resuming training state from {args.resume}")
        training_client.load_state(args.resume)

    baseline = (
        RoleBaseline(cfg.env_ids, cfg.role_baseline_ema_gamma)
        if cfg.use_role_baseline
        else None
    )

    wb = _init_wandb(cfg, seed) if cfg.use_wandb else None
    history_path = run_dir / "history.jsonl"
    ckpt_path = run_dir / "checkpoints.jsonl"

    for step in range(start_step + 1, cfg.num_steps + 1):
        step_start = time.time()

        sampling_client = training_client.save_weights_and_get_sampling_client(
            name=f"{cfg.run_name}-step{step}"
        )

        def train_sampler(_env_id: str, _client=sampling_client):
            return TinkerSampler(
                _client,
                tokenizer,
                max_tokens=cfg.generate_max_length,
                temperature=cfg.temperature,
                top_p=cfg.top_p,
                max_prompt_tokens=cfg.max_prompt_tokens,
            )

        turns, games = collect_batch(cfg, train_sampler, baseline, rng)
        collect_time = time.time() - step_start

        metrics = batch_metrics(turns, games)
        metrics["step"] = step
        metrics["collect_time"] = collect_time

        if not turns:
            # Every turn was filtered out. With filter_zero_adv this means every
            # game's shaped return was exactly 0 (possible early, when the EMA
            # baseline still equals the mean outcome), but it much more often
            # means the action parser is rejecting everything and every game is
            # a one-turn forfeit. Say which.
            print(
                f"Step {step}: no trainable turns "
                f"(invalid_action_rate={metrics['invalid_action_rate']:.0%}, "
                f"outcomes={ {k: v for k, v in metrics.items() if k.startswith('outcome/')} })"
            )
            _append_jsonl(history_path, metrics)
            continue

        data = [
            make_datum(
                tinker,
                torch,
                t.prompt_ids,
                t.response_ids,
                t.response_logprobs,
                t.advantage,
            )
            for t in turns
        ]

        loss_cfg = (
            {
                "clip_low_threshold": cfg.clip_low_threshold,
                "clip_high_threshold": cfg.clip_high_threshold,
            }
            if cfg.loss_fn == "ppo"
            else None
        )
        train_start = time.time()
        for _epoch in range(cfg.num_ppo_epochs):
            # forward_backward accumulates gradients; optim_step applies and
            # zeros them. Chunking is only about request size, so this is
            # num_ppo_epochs optimizer steps per collected batch -- matching
            # oat's --num_ppo_epochs 2 with --train_batch_size == the buffer.
            for i in range(0, len(data), cfg.fwd_bwd_chunk_size):
                _await(
                    training_client.forward_backward(
                        data=data[i : i + cfg.fwd_bwd_chunk_size],
                        loss_fn=cfg.loss_fn,
                        loss_fn_config=loss_cfg,
                    )
                )
            _await(
                training_client.optim_step(
                    tinker.AdamParams(learning_rate=cfg.learning_rate)
                )
            )
        metrics["train_time"] = time.time() - train_start
        metrics["step_time"] = time.time() - step_start
        if baseline is not None:
            metrics["role_baseline"] = baseline.snapshot()

        print(
            f"Step {step}/{cfg.num_steps} | "
            f"games {metrics['games']:.0f} | turns {metrics['train_turns']:.0f} | "
            f"len {metrics['mean_game_length']:.1f} | "
            f"invalid {metrics['invalid_action_rate']:.1%} | "
            f"|adv| {metrics['mean_abs_advantage']:.3f} | "
            f"resp {metrics['mean_response_tokens']:.0f}tok | "
            f"{metrics['step_time']:.0f}s "
            f"({collect_time:.0f}s roll / {metrics['train_time']:.0f}s train)"
        )

        if cfg.eval_steps and step % cfg.eval_steps == 0:
            def eval_sampler(_env_id: str, _client=sampling_client):
                return TinkerSampler(
                    _client,
                    tokenizer,
                    max_tokens=cfg.eval_generate_max_length,
                    temperature=cfg.eval_temperature,
                    top_p=cfg.eval_top_p,
                    max_prompt_tokens=cfg.max_prompt_tokens,
                )

            eval_metrics = run_eval(cfg, eval_sampler, rng)
            metrics.update(eval_metrics)
            for k, v in eval_metrics.items():
                print(f"    {k}: {v:.2%}")

        if cfg.save_steps and step % cfg.save_steps == 0:
            _save_checkpoint(training_client, cfg, step, ckpt_path)

        _append_jsonl(history_path, metrics)
        if wb is not None:
            wb.log({k: v for k, v in metrics.items() if isinstance(v, (int, float))},
                   step=step)

    _save_checkpoint(training_client, cfg, cfg.num_steps, ckpt_path, final=True)
    print(f"\ndone. checkpoints: {ckpt_path}")
    print("Export one for the MASK pipeline with:")
    print(f"  python export_lora.py --checkpoints {ckpt_path} --step <N> --out <dir>")
    if wb is not None:
        wb.finish()
    return 0


def _save_checkpoint(
    training_client: Any,
    cfg: SpiralTinkerConfig,
    step: int,
    ckpt_path: Path,
    final: bool = False,
) -> None:
    """Save both checkpoint kinds and record where they went.

    Two paths, for two different jobs:
      - `save_state` -> resumable optimizer+weights state, for --resume.
      - `save_weights_for_sampler` -> the path `export_lora.py` turns into a
        PEFT adapter that `../../evals/serve_tinker_ckpt.sh` can serve, which is
        how a Tinker checkpoint reaches the MASK pipeline at all.
    Both are recorded in checkpoints.jsonl because a `tinker://` path is not
    reconstructible from anything on your disk -- lose the file and the
    checkpoint is only findable by listing the Tinker side.
    """
    label = f"{cfg.run_name}-step{step}" + ("-final" if final else "")
    state_path = training_client.save_state(label)
    sampler_path = training_client.save_weights_for_sampler(name=label)

    record = {
        "step": step,
        "label": label,
        "final": final,
        "base_model": cfg.model_name,
        "lora_rank": cfg.lora_rank,
        "state_path": _unwrap_path(state_path),
        "sampler_path": _unwrap_path(sampler_path),
        "saved_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    _append_jsonl(ckpt_path, record)
    print(f"    [save] step {step} -> {record['sampler_path']}")


def _await(result: Any) -> Any:
    """Block on a Tinker future, tolerating calls that return a value directly.

    forward_backward/optim_step are future-returning, but the sync wrappers have
    changed shape across releases and a step boundary that silently does not
    wait would interleave the next rollout with an unfinished update.
    """
    return result.result() if hasattr(result, "result") else result


def _unwrap_path(result: Any) -> str | None:
    """Tinker save calls return a future whose result carries `.path`."""
    try:
        value = result.result() if hasattr(result, "result") else result
    except Exception as e:  # noqa: BLE001
        return f"<unresolved: {e}>"
    return getattr(value, "path", None) or str(value)


def _append_jsonl(path: Path, record: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, default=str) + "\n")


def _init_wandb(cfg: SpiralTinkerConfig, seed: int):
    try:
        import wandb
    except ImportError:
        print("[wandb] not installed; continuing without it")
        return None
    return wandb.init(
        project=cfg.wandb_project,
        name=cfg.run_name,
        # Everything lands in one project now, so the game is a tag rather than
        # a project name -- filter on it to get the old per-project view back.
        tags=["tinker", *(e.split("-")[0].lower() for e in cfg.env_ids)],
        config={**asdict(cfg), "seed": seed},
    )


IPD_ENV_ID = "IteratedPrisonersDilemma-v1"

# Verbatim from ipd_exp/ipd_lib.py NEUTRAL. Duplicated rather than imported:
# ipd_exp is a separate tree with its own venv, and an import would couple this
# trainer's startup to it. If that prompt changes there, change it here -- the
# whole point of this arm is that the two match.
IPD_NEUTRAL_SYSTEM = (
    "You are playing a game against another player. Read the rules given to "
    "you and make your choices. When the game asks for a decision, respond "
    "with the required bracketed token."
)


def _register_ipd_prompt(cfg: SpiralTinkerConfig, tokenizer: Any) -> None:
    """Make the IPD arm speak ipd_exp's prompt instead of spiral's template.

    See selfplay._PROMPT_OVERRIDES for why. Briefly: spiral's template frames the
    game as zero-sum and asks for \\boxed{}, and its soft /no_think marker does
    not stop Qwen3.5-9B from thinking past any budget we can afford -- measured,
    the block is still open at 2048 tokens, giving a 100% turn-1 forfeit rate.
    apply_chat_template(enable_thinking=False) is the supported switch.
    """
    if IPD_ENV_ID not in cfg.env_ids:
        return

    def build(observation: str) -> str:
        messages = [
            {"role": "system", "content": IPD_NEUTRAL_SYSTEM},
            {"role": "user", "content": observation},
        ]
        kw = dict(tokenize=False, add_generation_prompt=True)
        try:
            return tokenizer.apply_chat_template(
                messages, enable_thinking=False, **kw
            )
        except TypeError:  # tokenizer/template without the kwarg
            return tokenizer.apply_chat_template(messages, **kw)

    selfplay.register_prompt_override(IPD_ENV_ID, build)
    print(f"[prompt] {IPD_ENV_ID}: using ipd_exp NEUTRAL prompt, thinking disabled")


def _dry_run(cfg: SpiralTinkerConfig, rng: random.Random, run_dir: Path) -> int:
    """Play a few games with the stub sampler and print what would be trained on."""
    print("[dry-run] no Tinker calls; stub sampler plays uniformly random actions\n")
    try:
        tokenizer = load_tokenizer(cfg.model_name)
    except SystemExit as e:
        print(f"[dry-run] {e}\n[dry-run] falling back to a byte tokenizer")
        tokenizer = _ByteTokenizer()

    baseline = (
        RoleBaseline(cfg.env_ids, cfg.role_baseline_ema_gamma)
        if cfg.use_role_baseline
        else None
    )

    def factory(env_id: str):
        return StubSampler(env_id, tokenizer, rng)

    turns, games = collect_batch(cfg, factory, baseline, rng)
    metrics = batch_metrics(turns, games)

    print(f"played {len(games)} games -> {len(turns)} trainable turns")
    for k, v in sorted(metrics.items()):
        print(f"  {k:28s} {v}")
    if baseline is not None:
        print(f"  role baselines: {baseline.snapshot()}")

    # The eval path is a different code path (model in one seat, RandomAgent in
    # the other) and is the thing most likely to be broken while training looks
    # fine, so exercise it here too rather than discovering it at step 16.
    # Skipped when the run itself has eval turned off (--eval-steps 0): the IPD
    # arm scores checkpoints with ipd_exp's battery instead, and RandomAgent
    # needs a per-env action-space parser that IPD has no sensible one for.
    if cfg.eval_steps:
        print("\n[dry-run] eval round (stub model vs random opponent):")
        for k, v in sorted(run_eval(cfg, factory, rng).items()):
            print(f"  {k:44s} {v:.2%}")
    else:
        print("\n[dry-run] eval disabled (eval_steps=0); skipping eval probe")

    if turns:
        t = turns[0]
        n = len(t.prompt_ids) + len(t.response_ids)
        print(
            f"\nfirst datum: prompt {len(t.prompt_ids)} tok + response "
            f"{len(t.response_ids)} tok -> sequence length {n - 1} "
            f"(advantage {t.advantage:+.4f})"
        )
        _check_datum_alignment(t)
    else:
        print(
            "\nNo trainable turns. If invalid_action_rate is ~100% the action "
            "parser and the prompt template disagree -- fix that before spending "
            "anything on a real run."
        )
    (run_dir / "dry_run_metrics.json").write_text(json.dumps(metrics, indent=2))
    return 0


def _check_datum_alignment(t: TrainingTurn) -> None:
    """Assert make_datum's shift, without needing tinker or torch installed.

    Cheap, but it is the one bug class in this file that produces a run that
    trains, costs money and learns nothing (see the NOTE in make_datum).
    """

    class _FakeTensorData:
        @staticmethod
        def from_torch(x):
            return x

    class _FakeTorch:
        long = "long"
        float32 = "float32"

        @staticmethod
        def tensor(x, dtype=None):
            del dtype
            return list(x)

    class _FakeModelInput:
        @staticmethod
        def from_ints(x):
            return list(x)

    class _FakeTinker:
        ModelInput = _FakeModelInput
        TensorData = _FakeTensorData

        @staticmethod
        def Datum(model_input, loss_fn_inputs):  # noqa: N802 - mirrors tinker
            return {"model_input": model_input, **loss_fn_inputs}

    d = make_datum(
        _FakeTinker, _FakeTorch, t.prompt_ids, t.response_ids,
        t.response_logprobs, t.advantage,
    )
    tokens = list(t.prompt_ids) + list(t.response_ids)
    n_prompt = len(t.prompt_ids)
    assert d["model_input"] == tokens[:-1]
    assert d["target_tokens"] == tokens[1:]
    # position i of the input predicts tokens[i+1]; the first response token
    # lives at index n_prompt, so it is the target of input position n_prompt-1.
    assert d["target_tokens"][n_prompt - 1] == t.response_ids[0]
    assert d["advantages"][n_prompt - 1] == t.advantage
    assert d["advantages"][n_prompt - 2] == 0.0
    assert d["logprobs"][n_prompt - 1] == t.response_logprobs[0]
    print("  datum alignment: OK (cookbook right-shift/left-shift convention)")


if __name__ == "__main__":
    sys.exit(main())
