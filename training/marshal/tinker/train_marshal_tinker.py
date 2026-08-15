#!/usr/bin/env python3
"""MARSHAL Kuhn Poker self-play on the Tinker training API.

MARSHAL upstream needs ROLL: ray, hydra, Megatron-LM + mcore_adapter, vLLM, and
8 GPUs with tensor_model_parallel_size 4. This runs the same self-play loop and
the same credit assignment with Tinker doing sampling and gradients remotely, so
the only thing local is the OpenSpiel game loop -- pure Python, CPU-only.

A policy step, mirroring ROLL's agentic pipeline:

  1. snapshot weights into a sampling client
  2. play `episodes_per_step` self-play hands; each yields 2 trainable rows
     (one per seat), each row a whole multi-turn chat
  3. MARSHAL credit assignment (advantage.py, driven by ROLL's own tensor code)
  4. one Datum per (episode, seat) -> forward_backward + optim_step

Usage:
    export TINKER_API_KEY=...
    python train_marshal_tinker.py --scale full
    python train_marshal_tinker.py --scale smoke --dry-run   # no API calls

Tinker call sequence follows https://github.com/Guanghan/JustTinker
(`scripts/tinker/justrl_math_reasoning.py`), with the same deliberate deviation
on token alignment documented in `make_datum` there and in ../../tinker/.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import statistics
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))

from advantage import compute_marshal_advantages  # noqa: E402
from config import SCALES, MarshalTinkerConfig, build_config  # noqa: E402
from selfplay import (  # noqa: E402
    EpisodeResult,
    Sampled,
    import_marshal,
    make_env,
    parse_response,
    play_episodes_concurrently,
)


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
    try:
        from tinker_cookbook import tokenizer_utils

        return tokenizer_utils.get_tokenizer(model_name)
    except Exception as e:  # noqa: BLE001
        print(f"[tokenizer] tinker_cookbook lookup failed ({e}); trying HF")
    try:
        from transformers import AutoTokenizer

        return AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    except Exception as e:  # noqa: BLE001
        raise SystemExit(f"could not load a tokenizer for {model_name!r}: {e}") from e


class TinkerSampler:
    """One call == one model turn, from an already-tokenised chat prompt.

    Unlike the SPIRAL arm this takes token ids, not text: MARSHAL's prompt is a
    growing chat rendered by `apply_chat_template`, and the episode loop needs
    those exact ids to compute how much of the prompt is new since the previous
    assistant turn.
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
        stop = tokenizer.encode("<|im_end|>", add_special_tokens=False)
        if not stop:
            raise SystemExit("tokenizer has no <|im_end|>; MARSHAL prompts are ChatML")
        kwargs = dict(max_tokens=max_tokens, temperature=temperature, stop=[stop[0]])
        try:
            self._params = tinker.SamplingParams(top_p=top_p, **kwargs)
        except TypeError:
            print("[sampler] SamplingParams has no top_p; ignoring it")
            self._params = tinker.SamplingParams(**kwargs)

    def __call__(self, prompt_ids: list[int]) -> Sampled | None:
        if len(prompt_ids) > self._max_prompt_tokens:
            return None
        result = self._client.sample(
            prompt=self._tinker.ModelInput.from_ints(list(prompt_ids)),
            sampling_params=self._params,
            num_samples=1,
        ).result()
        seq = result.sequences[0]
        ids = list(seq.tokens)
        lps = list(seq.logprobs) if seq.logprobs is not None else [0.0] * len(ids)
        return Sampled(
            response_ids=ids,
            response_logprobs=lps,
            text=self._tok.decode(ids, skip_special_tokens=True),
            truncated=getattr(seq, "stop_reason", None) == "length",
        )


class StubSampler:
    """Offline stand-in for --dry-run: emits a correctly-formatted random action.

    Occasionally emits a malformed response so the format-penalty path and the
    forfeit branch get exercised too.
    """

    def __init__(self, tokenizer: Any, rng: random.Random, enable_think: bool) -> None:
        self._tok = tokenizer
        self._rng = rng
        self._think = enable_think

    def __call__(self, prompt_ids: list[int]) -> Sampled | None:
        action = self._rng.choice(["<PASS>", "<BET>"])
        if self._rng.random() < 0.08:
            text = "I think I should bet."  # malformed on purpose
        elif self._think:
            text = f"<think>\nWeighing pot odds.\n</think><answer>{action}</answer>"
        else:
            text = f"<answer>{action}</answer>"
        ids = self._tok.encode(text, add_special_tokens=False)
        return Sampled(
            response_ids=list(ids),
            response_logprobs=[-0.5] * len(ids),
            text=text,
            truncated=False,
        )


def make_datum(tinker: Any, torch: Any, trace: Any, adv_row: Any) -> Any:
    """One Datum per (episode, seat), with every assistant turn in one sequence.

    Alignment is tinker-cookbook's: input = tokens[:-1], target = tokens[1:],
    and logprobs/advantages sliced [1:]. `advantage.py` already returns the
    advantage row in [1:] space (ROLL slices identically), so it drops in
    directly. Observation positions carry advantage 0, which is what masks them
    out of the loss.
    """
    tokens = list(trace.tokens)
    n = len(tokens)
    input_tokens = tokens[:-1]
    target_tokens = tokens[1:]
    logprobs = list(trace.logprobs)[1:]
    advantages = [float(x) for x in adv_row[: n - 1].tolist()]

    if not (len(input_tokens) == len(target_tokens) == len(logprobs) == len(advantages)):
        raise ValueError(
            f"length mismatch: in={len(input_tokens)} tgt={len(target_tokens)} "
            f"lp={len(logprobs)} adv={len(advantages)}"
        )

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


def collect(cfg: MarshalTinkerConfig, sampler_factory, tokenizer, rng) -> list[EpisodeResult]:
    seeds = [rng.randrange(2**31) for _ in range(cfg.episodes_per_step)]
    return play_episodes_concurrently(
        seeds,
        sampler_factory,
        tokenizer,
        max_workers=cfg.max_concurrent_episodes,
        max_turns=cfg.max_turns,
        enable_think=cfg.enable_think,
        action_sep=cfg.action_sep,
        special_tokens=[],
        format_penalty=cfg.format_penalty,
        max_prompt_tokens=cfg.max_prompt_tokens,
    )


def episode_metrics(episodes: list[EpisodeResult]) -> dict[str, float]:
    if not episodes:
        return {}
    traces = [t for ep in episodes for t in ep.traces.values()]
    turns = sum(len(t.spans) for t in traces)
    invalid = sum(t.n_invalid for t in traces)
    outcomes: dict[str, int] = {}
    for ep in episodes:
        outcomes[ep.outcome] = outcomes.get(ep.outcome, 0) + 1
    m = {
        "episodes": float(len(episodes)),
        "rows": float(len(traces)),
        "model_turns": float(turns),
        "mean_turns_per_episode": statistics.fmean(ep.n_turns for ep in episodes),
        "invalid_rate": invalid / turns if turns else 0.0,
        "truncated_rate": sum(t.n_truncated for t in traces) / turns if turns else 0.0,
        "prefix_breaks": float(sum(t.prefix_breaks for t in traces)),
        "mean_return_p0": statistics.fmean(ep.returns.get(0, 0.0) for ep in episodes),
    }
    for k, v in outcomes.items():
        m[f"outcome/{k}"] = v / len(episodes)
    return m


def run_eval(cfg: MarshalTinkerConfig, sampler_factory, tokenizer, rng) -> dict[str, float]:
    """Model vs MARSHAL's built-in CFR opponent, as both seats.

    This is the val configuration from the MARSHAL yaml (KuhnPoker-first /
    KuhnPoker-second, built_in_opponent: cfr). CFR is near-Nash, so ~50% is the
    ceiling, not a floor -- read movement toward 50% as improvement, unlike the
    SPIRAL arm's win rate against `random`.
    """
    from selfplay import play_episode_vs_opponent

    out: dict[str, float] = {}
    for seat in (0, 1):
        seeds = [rng.randrange(2**31) for _ in range(cfg.eval_episodes)]
        results = []
        for s in seeds:
            results.append(
                play_episode_vs_opponent(
                    s,
                    sampler_factory(),
                    tokenizer,
                    model_player=seat,
                    opponent=cfg.eval_opponent,
                    max_turns=cfg.max_turns,
                    enable_think=cfg.enable_think,
                    action_sep=cfg.action_sep,
                    special_tokens=[],
                    format_penalty=cfg.format_penalty,
                    max_prompt_tokens=cfg.max_prompt_tokens,
                )
            )
        n = max(1, len(results))
        wins = sum(1 for r in results if r.returns.get(seat, 0.0) > 0)
        mean_ret = statistics.fmean(r.returns.get(seat, 0.0) for r in results)
        turns = sum(len(t.spans) for r in results for t in r.traces.values())
        inval = sum(t.n_invalid for r in results for t in r.traces.values())
        out[f"eval/seat{seat}/win_rate"] = wins / n
        out[f"eval/seat{seat}/mean_return"] = mean_ret
        out[f"eval/seat{seat}/invalid_rate"] = inval / turns if turns else 0.0
    return out


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        description="MARSHAL Kuhn Poker self-play via the Tinker training API",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--scale", default="full", choices=sorted(SCALES))
    p.add_argument("--model", dest="model_name", default=None)
    p.add_argument("--lora-rank", dest="lora_rank", type=int, default=None)
    p.add_argument("--num-steps", dest="num_steps", type=int, default=None)
    p.add_argument("--episodes-per-step", dest="episodes_per_step", type=int, default=None)
    p.add_argument(
        "--max-concurrent-episodes", dest="max_concurrent_episodes", type=int, default=None
    )
    p.add_argument("--learning-rate", dest="learning_rate", type=float, default=None)
    p.add_argument("--num-ppo-epochs", dest="num_ppo_epochs", type=int, default=None)
    p.add_argument("--eval-steps", dest="eval_steps", type=int, default=None)
    p.add_argument("--eval-episodes", dest="eval_episodes", type=int, default=None)
    p.add_argument("--save-steps", dest="save_steps", type=int, default=None)
    p.add_argument("--generate-max-length", dest="generate_max_length", type=int, default=None)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--run-name", dest="run_name", default=None)
    p.add_argument("--output-dir", dest="output_dir", default=None)
    p.add_argument("--use-wb", dest="use_wandb", action="store_true", default=None)
    p.add_argument("--no-think", dest="enable_think", action="store_false", default=None)
    p.add_argument("--resume", default=None)
    p.add_argument("--marshal-dir", default=os.environ.get("MARSHAL_DIR", ""))
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    overrides = {
        k: v
        for k, v in vars(args).items()
        if k not in ("scale", "dry_run", "marshal_dir", "resume") and v is not None
    }
    cfg = build_config(args.scale, overrides)

    marshal_dir = args.marshal_dir or str(Path("/workspace/allie/MARSHAL"))
    import_marshal(marshal_dir)

    rng = random.Random(cfg.seed)
    random.seed(cfg.seed)

    run_dir = Path(cfg.output_dir) / f"{cfg.run_name}-{time.strftime('%Y%m%d_%H%M%S')}"
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "config.json").write_text(cfg.to_json())

    print("=" * 72)
    print(f"MARSHAL Kuhn self-play on Tinker  |  scale={cfg.scale}")
    print("=" * 72)
    print(f"model        : {cfg.model_name} (LoRA rank {cfg.lora_rank})")
    print(f"MARSHAL dir  : {marshal_dir}")
    print(f"steps        : {cfg.num_steps} x {cfg.episodes_per_step} episodes "
          f"({cfg.rows_per_step} rows)")
    print(f"credit       : turn-level reinforce (gamma {cfg.gamma}) + "
          f"per-seat norm ({cfg.advantage_norm})")
    print(f"lr           : {cfg.learning_rate}  (MARSHAL yaml: 1e-6, full-finetune)")
    print(f"run dir      : {run_dir}")
    print("=" * 72)

    if args.dry_run:
        return _dry_run(cfg, rng, run_dir)

    if not os.environ.get("TINKER_API_KEY"):
        raise SystemExit("TINKER_API_KEY is not set")

    tinker = _load_tinker()
    import torch

    tokenizer = load_tokenizer(cfg.model_name)
    print("connecting to Tinker ...")
    service_client = tinker.ServiceClient()
    training_client = service_client.create_lora_training_client(
        base_model=cfg.model_name, rank=cfg.lora_rank
    )
    if args.resume:
        print(f"resuming from {args.resume}")
        training_client.load_state(args.resume)

    history_path = run_dir / "history.jsonl"
    ckpt_path = run_dir / "checkpoints.jsonl"
    wb = _init_wandb(cfg, cfg.seed) if cfg.use_wandb else None

    for step in range(1, cfg.num_steps + 1):
        t0 = time.time()
        sampling_client = training_client.save_weights_and_get_sampling_client(
            name=f"{cfg.run_name}-step{step}"
        )

        def train_sampler(_client=sampling_client):
            return TinkerSampler(
                _client, tokenizer,
                max_tokens=cfg.generate_max_length,
                temperature=cfg.temperature,
                top_p=cfg.top_p,
                max_prompt_tokens=cfg.max_prompt_tokens,
            )

        episodes = collect(cfg, train_sampler, tokenizer, rng)
        collect_time = time.time() - t0
        metrics = episode_metrics(episodes)
        metrics.update({"step": step, "collect_time": collect_time})

        traces = [t for ep in episodes for t in ep.traces.values() if t.spans]
        if not traces:
            print(f"Step {step}: no trainable rows (invalid_rate="
                  f"{metrics.get('invalid_rate', 0):.0%})")
            _append(history_path, metrics)
            _log_wandb(wb, metrics, step)
            continue

        advantages, _mask, adv_metrics = compute_marshal_advantages(
            traces,
            gamma=cfg.gamma,
            lambd=cfg.lambd,
            reward_norm_method=cfg.reward_norm_method,
            separate_norm_for_selfplay=cfg.separate_norm_for_selfplay,
            whiten_rewards=cfg.whiten_rewards,
            advantage_norm=cfg.advantage_norm,
            whiten_advantages=cfg.whiten_advantages,
            advantage_clip=cfg.advantage_clip,
        )
        metrics.update(adv_metrics)

        data = [
            make_datum(tinker, torch, tr, advantages[i])
            for i, tr in enumerate(traces)
        ]

        loss_cfg = (
            {
                "clip_low_threshold": cfg.clip_low_threshold,
                "clip_high_threshold": cfg.clip_high_threshold,
            }
            if cfg.loss_fn == "ppo"
            else None
        )
        t1 = time.time()
        for _ in range(cfg.num_ppo_epochs):
            for i in range(0, len(data), cfg.fwd_bwd_chunk_size):
                _await(
                    training_client.forward_backward(
                        data=data[i : i + cfg.fwd_bwd_chunk_size],
                        loss_fn=cfg.loss_fn,
                        loss_fn_config=loss_cfg,
                    )
                )
            _await(training_client.optim_step(
                tinker.AdamParams(learning_rate=cfg.learning_rate)
            ))
        metrics["train_time"] = time.time() - t1
        metrics["step_time"] = time.time() - t0

        print(
            f"Step {step}/{cfg.num_steps} | eps {metrics['episodes']:.0f} | "
            f"rows {len(traces)} | turns/ep {metrics['mean_turns_per_episode']:.2f} | "
            f"invalid {metrics['invalid_rate']:.1%} | "
            f"|adv| {metrics.get('advantage_abs_mean', 0):.3f} | "
            f"{metrics['step_time']:.0f}s "
            f"({collect_time:.0f}s roll / {metrics['train_time']:.0f}s train)"
        )

        if cfg.eval_steps and step % cfg.eval_steps == 0:
            def eval_sampler(_client=sampling_client):
                return TinkerSampler(
                    _client, tokenizer,
                    max_tokens=cfg.eval_generate_max_length,
                    temperature=cfg.eval_temperature,
                    top_p=cfg.top_p,
                    max_prompt_tokens=cfg.max_prompt_tokens,
                )

            ev = run_eval(cfg, eval_sampler, tokenizer, rng)
            metrics.update(ev)
            for k, v in ev.items():
                print(f"    {k}: {v:+.3f}" if "return" in k else f"    {k}: {v:.1%}")

        if cfg.save_steps and step % cfg.save_steps == 0:
            _save_checkpoint(training_client, cfg, step, ckpt_path)

        _append(history_path, metrics)
        _log_wandb(wb, metrics, step)

    _save_checkpoint(training_client, cfg, cfg.num_steps, ckpt_path, final=True)
    print(f"\ndone. checkpoints: {ckpt_path}")
    print("Export for MASK with ../../tinker/export_lora.py "
          f"--checkpoints {ckpt_path} --step <N> --out <dir>")
    return 0


def _await(x):
    return x.result() if hasattr(x, "result") else x


def _save_checkpoint(training_client, cfg, step, ckpt_path, final=False):
    label = f"{cfg.run_name}-step{step}" + ("-final" if final else "")
    state = training_client.save_state(label)
    sampler = training_client.save_weights_for_sampler(name=label)
    rec = {
        "step": step,
        "label": label,
        "final": final,
        "base_model": cfg.model_name,
        "lora_rank": cfg.lora_rank,
        "state_path": _path_of(state),
        "sampler_path": _path_of(sampler),
        "saved_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    _append(ckpt_path, rec)
    print(f"    [save] step {step} -> {rec['sampler_path']}")


def _path_of(result):
    try:
        v = result.result() if hasattr(result, "result") else result
    except Exception as e:  # noqa: BLE001
        return f"<unresolved: {e}>"
    return getattr(v, "path", None) or str(v)


def _append(path: Path, rec: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, default=str) + "\n")


def _init_wandb(cfg: MarshalTinkerConfig, seed: int):
    """Mirror of ../../tinker/train_tinker.py so both arms land in one workspace.

    Same project (`strategy-behavior`) and entity as every other strategy-game
    run; the `marshal` tag is what separates this arm inside it.
    """
    try:
        import wandb  # noqa: PLC0415
    except ImportError:
        print("[wandb] not installed; continuing without it")
        return None
    return wandb.init(
        project=cfg.wandb_project,
        name=cfg.run_name,
        tags=["marshal", "tinker"],
        config={**asdict(cfg), "seed": seed},
    )


def _log_wandb(wb, metrics: dict, step: int) -> None:
    """Eval keys are already merged into `metrics`, so this ships them too."""
    if wb is None:
        return
    wb.log(
        {k: v for k, v in metrics.items() if isinstance(v, (int, float))}, step=step
    )


def _dry_run(cfg, rng, run_dir) -> int:
    print("[dry-run] no Tinker calls; stub sampler plays random legal actions\n")
    try:
        tokenizer = load_tokenizer(cfg.model_name)
    except SystemExit as e:
        raise SystemExit(f"[dry-run] needs a real tokenizer for chat templating: {e}")

    def factory():
        return StubSampler(tokenizer, rng, cfg.enable_think)

    episodes = collect(cfg, factory, tokenizer, rng)
    metrics = episode_metrics(episodes)
    traces = [t for ep in episodes for t in ep.traces.values() if t.spans]
    print(f"played {len(episodes)} episodes -> {len(traces)} trainable rows")
    for k, v in sorted(metrics.items()):
        print(f"  {k:28s} {v}")

    if traces:
        advantages, mask, adv_metrics = compute_marshal_advantages(
            traces,
            gamma=cfg.gamma, lambd=cfg.lambd,
            reward_norm_method=cfg.reward_norm_method,
            separate_norm_for_selfplay=cfg.separate_norm_for_selfplay,
            whiten_rewards=cfg.whiten_rewards,
            advantage_norm=cfg.advantage_norm,
            whiten_advantages=cfg.whiten_advantages,
        )
        print("\nMARSHAL advantages:")
        for k, v in sorted(adv_metrics.items()):
            print(f"  {k:28s} {v:.4f}")
        tr = traces[0]
        print(f"\nfirst row: seat {tr.player_id}, {len(tr.tokens)} tokens, "
              f"{len(tr.spans)} assistant turns, scores {tr.turn_scores}")
        nz = (advantages[0].abs() > 0).sum().item()
        print(f"  non-zero advantage positions: {nz} "
              f"(response tokens: {int(mask[0].sum().item())})")
        assert nz <= int(mask[0].sum().item()) + 1, "advantage leaked outside response"
        print("  advantage confined to assistant spans: OK")
    (run_dir / "dry_run_metrics.json").write_text(json.dumps(metrics, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
