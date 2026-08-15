"""Config for the Tinker port of MARSHAL's Kuhn Poker self-play arm.

Every default traces to `examples/kuhn_poker/agentic_val_kuhn_poker_selfplay.yaml`
in the MARSHAL checkout. Where Tinker cannot express a ROLL setting the field
carries a DIVERGENCE note and it is repeated in README.md.

  ROLL / MARSHAL yaml                      -> field here
  rollout_batch_size: 128                  -> episodes_per_step * 2 (self-play: 2 rows/episode)
  env_groups: 64, group_size: 1            -> episodes_per_step = 64
  max_steps: 200                           -> num_steps
  save_steps: 20 / eval_steps: 5           -> save_steps / eval_steps
  learning_rate: 1e-6                      -> learning_rate (see note)
  ppo_epochs: 1                            -> num_ppo_epochs
  adv_estimator: reinforce, gamma 1        -> gamma (lambd unused by reinforce)
  whiten_advantages / whiten_rewards: true -> whiten_advantages / whiten_rewards
  advantage_norm: mean                     -> advantage_norm
  reward_normalization.method: mean        -> reward_norm_method
  ...separate_norm_for_selfplay: true      -> separate_norm_for_selfplay
  pg_clip: 0.2 / pg_clip_high: 0.20        -> clip_low_threshold / clip_high_threshold
  format_penalty: 0.05                     -> format_penalty
  enable_think: True                       -> enable_think
  action_sep: "||"                         -> action_sep
  max_actions_per_traj: 50                 -> max_turns
  max_new_tokens: 4096                     -> generate_max_length
  temperature 0.6 / top_p 0.99 / top_k 100 -> temperature / top_p (top_k: see note)
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, fields
from typing import Any

SCALES: dict[str, dict[str, Any]] = {
    "smoke": {  # minutes, cents -- prove the plumbing before spending
        "num_steps": 2,
        "episodes_per_step": 4,
        "max_concurrent_episodes": 4,
        "eval_steps": 2,
        "save_steps": 2,
        "eval_episodes": 4,
        "generate_max_length": 2048,
    },
    "short": {
        "num_steps": 64,
        "episodes_per_step": 32,
        "max_concurrent_episodes": 32,
        "eval_steps": 16,
        "save_steps": 16,
        "eval_episodes": 24,
    },
    "full": {  # max_steps 200, env_groups 64
        "num_steps": 200,
        "episodes_per_step": 64,
        "max_concurrent_episodes": 32,
        "eval_steps": 5,
        "save_steps": 20,
        "eval_episodes": 48,
    },
}


@dataclass
class MarshalTinkerConfig:
    # --- identity -----------------------------------------------------------
    scale: str = "full"
    run_name: str = "marshal-tinker-kuhn-selfplay"
    output_dir: str = "outputs/marshal-tinker"
    seed: int = 42  # MARSHAL yaml: seed 42

    # --- model --------------------------------------------------------------
    # DIVERGENCE. MARSHAL trains Qwen3-4B full-parameter via Megatron. Tinker
    # neither hosts Qwen3-4B nor does full finetuning. Qwen3-8B is chosen to
    # match ../../tinker/ (the SPIRAL Tinker arm), so the two Tinker arms differ
    # only in algorithm+env and are directly comparable to each other. Neither
    # is directly comparable to results/, which is Qwen3-4B-Base full-finetune.
    model_name: str = "Qwen/Qwen3-8B"
    lora_rank: int = 32

    # --- rollout ------------------------------------------------------------
    # ROLL's rollout_batch_size 128 == env_groups 64 x 2 seats, since self-play
    # yields one trainable row per player per episode.
    episodes_per_step: int = 64
    num_steps: int = 200
    max_concurrent_episodes: int = 32
    max_turns: int = 50  # max_actions_per_traj
    sequence_length: int = 32768
    generate_max_length: int = 4096
    temperature: float = 0.6
    top_p: float = 0.99
    # DIVERGENCE: MARSHAL sets top_k 100; Tinker's SamplingParams has no top_k.
    # At top_p 0.99 the truncation top_k would add is small, but it is a real
    # difference in the sampling distribution.

    enable_think: bool = True
    action_sep: str = "||"
    format_penalty: float = 0.05

    # --- MARSHAL credit assignment -----------------------------------------
    gamma: float = 1.0
    lambd: float = 0.95  # unused by the reinforce estimator; kept for parity
    reward_norm_method: str = "mean"
    separate_norm_for_selfplay: bool = True
    whiten_rewards: bool = True
    advantage_norm: str | None = "mean"
    whiten_advantages: bool = True
    advantage_clip: float | None = None  # yaml has it commented out

    # --- optimisation -------------------------------------------------------
    # NOTE, and this is the first thing to change if a run looks flat: MARSHAL's
    # 1e-6 is a *full-parameter* Megatron learning rate. A rank-32 LoRA
    # typically needs ~10x that. We default to 1e-5 and document the deviation
    # rather than faithfully reproducing a number that does not transfer across
    # the finetuning method. Pass --learning-rate 1e-6 for literal fidelity.
    learning_rate: float = 1e-5
    num_ppo_epochs: int = 1  # ppo_epochs: 1
    loss_fn: str = "ppo"
    clip_low_threshold: float = 0.8  # pg_clip 0.2  -> 1-0.2
    clip_high_threshold: float = 1.2  # pg_clip_high 0.20 -> 1+0.20
    fwd_bwd_chunk_size: int = 8
    # DIVERGENCE: MARSHAL uses use_kl_loss=True with kl_loss_coef=0.20, a
    # differentiable KL against a frozen reference. Tinker's ppo /
    # importance_sampling losses expose no KL term and there is no reference
    # model handle, so this arm trains with NO KL constraint. 0.20 is a strong
    # coefficient, so expect this arm to drift from the base policy faster than
    # MARSHAL's does. Also unavailable: dual_clip_loss (dual_clip_loss: true).

    # --- eval ---------------------------------------------------------------
    eval_steps: int = 5
    eval_episodes: int = 48
    # MARSHAL's val set plays KuhnPoker-first / KuhnPoker-second against the
    # built-in CFR (near-Nash) opponent -- a far stronger and more informative
    # baseline than SPIRAL's `random`. Win rate vs CFR near 50% is the ceiling.
    eval_opponent: str = "cfr"
    eval_temperature: float = 0.6
    eval_generate_max_length: int = 4096

    # --- checkpointing ------------------------------------------------------
    save_steps: int = 20

    # --- misc ---------------------------------------------------------------
    use_wandb: bool = False
    wandb_project: str = "strategy-behavior"
    thinking_mode: str = "auto"  # see ../../tinker/config.py; MARSHAL prompts
    # already ask for <think>, so `auto` resolves to OFF here -- suppressing the
    # model's native thinking would fight the required response format.

    @property
    def rows_per_step(self) -> int:
        return self.episodes_per_step * 2

    @property
    def max_prompt_tokens(self) -> int:
        return max(1, min(self.sequence_length, 32768) - self.generate_max_length)

    def validate(self) -> None:
        if self.loss_fn not in ("ppo", "importance_sampling"):
            raise ValueError(f"unknown loss_fn {self.loss_fn!r}")
        if self.reward_norm_method not in ("mean", "mean_std", "identity", "none"):
            raise ValueError(f"unknown reward_norm_method {self.reward_norm_method!r}")
        if self.advantage_norm not in ("mean", "mean_std", None):
            raise ValueError(f"unknown advantage_norm {self.advantage_norm!r}")
        if self.max_prompt_tokens <= 0:
            raise ValueError("generate_max_length leaves no room for a prompt")

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True)


def build_config(scale: str, overrides: dict[str, Any]) -> MarshalTinkerConfig:
    if scale not in SCALES:
        raise ValueError(f"unknown scale {scale!r}; choose from {sorted(SCALES)}")
    values: dict[str, Any] = {"scale": scale}
    values.update(SCALES[scale])
    values.update({k: v for k, v in overrides.items() if v is not None})

    known = {f.name for f in fields(MarshalTinkerConfig)}
    unknown = set(values) - known
    if unknown:
        raise ValueError(f"unknown config keys: {sorted(unknown)}")
    cfg = MarshalTinkerConfig(**values)
    cfg.validate()
    return cfg
