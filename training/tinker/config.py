"""Configuration for the Tinker port of the SPIRAL self-play arm.

Every default here is traceable to a flag in `../run_kuhn.sh`, `../run_multi.sh`
or `../run_pigdice.sh` -- the three oat/slurm arms this port mirrors. Where
Tinker cannot express what oat does, the field carries a `DIVERGENCE` comment
and the same point is repeated in README.md, because a few of these changes
(base model, LoRA-vs-full-finetune) mean a Tinker checkpoint is *not* a drop-in
substitute for the `results/` numbers.

Sources for the mapping:
  oat flag                     -> field here
  --rollout_batch_size 128     -> turns_per_step        (oat counts *turns*, not games)
  --train_batch_size 128       -> (same as above; one optimizer pass per collection)
  --num_ppo_epochs 2           -> num_ppo_epochs
  --learning_rate 1e-6         -> learning_rate
  --lr_scheduler constant      -> (constant is the only thing we do; no scheduler)
  --beta 0                     -> no KL term (Tinker's ppo loss has no kl_coef anyway)
  --gamma 1                    -> gamma
  --max_model_len 12800        -> max_model_len
  --generate_max_length 4096   -> generate_max_length
  --temperature 1.0 --top_p 1  -> temperature / top_p
  --eval_steps 16              -> eval_steps
  --save_steps 16 (64 pigdice) -> save_steps
  --eval_games 16              -> eval_games
  --eval_temperature 0.6       -> eval_temperature
  --eval_top_p 0.95            -> eval_top_p
  --max_train 51200            -> num_steps (51200 / 128 = 400 policy steps)
  --eval_opponent_names random -> eval_opponent (only "random" is supported here)

SelfPlayArgs defaults that run_*.sh does not override, and which we keep:
  use_role_baseline=True, role_baseline_ema_gamma=0.95, filter_zero_adv=True,
  reward_scaling=1.0, use_intermediate_rewards=True, max_turns=50,
  prompt_template="qwen3", num_envs=1.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field, fields
from typing import Any

# --- arms -------------------------------------------------------------------
# One entry per oat run script. `env_ids` / `use_llm_obs_wrappers` are copied
# verbatim; see ../README.md for why PigDice *must* use the LLM obs wrapper and
# TicTacToe must not.
ARMS: dict[str, dict[str, Any]] = {
    "kuhn": {
        "env_ids": ["KuhnPoker-v1"],
        "use_llm_obs_wrappers": [True],
        "eval_env_ids": ["TicTacToe-v0", "KuhnPoker-v1"],
        "eval_use_llm_obs_wrappers": [False, True],
        "run_name": "spiral-tinker-kp-self-play",
    },
    "multi": {
        "env_ids": ["TicTacToe-v0", "KuhnPoker-v1", "SimpleNegotiation-v1"],
        "use_llm_obs_wrappers": [False, True, True],
        "eval_env_ids": ["TicTacToe-v0", "KuhnPoker-v1"],
        "eval_use_llm_obs_wrappers": [False, True],
        "run_name": "spiral-tinker-multi-self-play",
    },
    "pigdice": {
        "env_ids": ["PigDice-v1"],
        "use_llm_obs_wrappers": [True],
        "eval_env_ids": ["TicTacToe-v0", "KuhnPoker-v1", "PigDice-v1"],
        "eval_use_llm_obs_wrappers": [False, True, True],
        # run_pigdice.sh uses --save_steps 64, not 16: PigDice episodes are ~5x
        # longer, so the run is slower per step and checkpoints are less useful
        # at a 16-step cadence. Kept for parity even though Tinker checkpoints
        # cost storage on their side, not ours.
        "save_steps": 64,
        "run_name": "spiral-tinker-pigdice-control",
    },
    # Self-play ablation for the exploitation-transfer POC (plan 0808 §1.2:
    # "self-play is included only as an ablation to demonstrate the erosion").
    # The POC's T1/A2 arms train seat 0 against a FIXED opponent; here both seats
    # are the learner, which is also why RAE earns its keep -- with a fixed
    # opponent only one role is ever trained, so role-conditioned baselining has
    # nothing to condition on (results §1 note (a)).
    #
    # Eval envs deliberately exclude the usual TicTacToe/Kuhn transfer pair: this
    # arm exists to be compared against ipd_exp's battery, not against the
    # reasoning-transfer arms.
    "ipd": {
        "env_ids": ["IteratedPrisonersDilemma-v1"],
        # IPD's observation is a running conversation; the first/last wrapper
        # would drop the interleaved talk turns that make the game legible.
        "use_llm_obs_wrappers": [True],
        "eval_env_ids": ["IteratedPrisonersDilemma-v1"],
        "eval_use_llm_obs_wrappers": [True],
        "run_name": "spiral-tinker-ipd-self-play",
    },
}

# --- scales -----------------------------------------------------------------
# "full" reproduces the oat run's budget. The smaller scales exist so you can
# find out that your prompt template, action parser and reward plumbing work
# before spending real money -- a Tinker step is billed per sampled token, and a
# broken action parser burns exactly as many tokens as a working one.
SCALES: dict[str, dict[str, Any]] = {
    "smoke": {  # ~2 policy steps, a handful of games. Minutes, cents.
        "num_steps": 2,
        "turns_per_step": 8,
        "max_concurrent_games": 4,
        "eval_steps": 2,
        "save_steps": 2,
        "eval_games": 2,
        "generate_max_length": 1024,
    },
    "short": {  # enough steps to see the win rate move off chance.
        "num_steps": 64,
        "turns_per_step": 64,
        "max_concurrent_games": 16,
        "eval_steps": 16,
        "save_steps": 16,
        "eval_games": 8,
    },
    "full": {  # --max_train 51200 / --rollout_batch_size 128
        "num_steps": 400,
        "turns_per_step": 128,
        "max_concurrent_games": 32,
        "eval_steps": 16,
        "save_steps": 16,
        "eval_games": 16,
    },
}


@dataclass
class SpiralTinkerConfig:
    # --- identity -----------------------------------------------------------
    arm: str = "kuhn"  # key into ARMS
    scale: str = "full"  # key into SCALES
    run_name: str = "spiral-tinker-kp-self-play"
    output_dir: str = "outputs/spiral-tinker"
    seed: int | None = None  # None == oat's --rnd-seed

    # --- model --------------------------------------------------------------
    # DIVERGENCE (the big one). The oat arms train `Qwen/Qwen3-4B-Base`
    # full-parameter. Tinker does not host Qwen3-4B-Base and only does LoRA, so
    # this arm is a *different model trained a different way*. Its checkpoints
    # are a fresh experiment, not another point on the same curve as
    # `results/spiral-kuhn-step256`; comparing them to that table would be
    # comparing two changes at once. Run a matching Tinker `base` MASK arm
    # before reading anything into a Tinker checkpoint's honesty score.
    #
    # Qwen3.5-9B-Base is the closest available analogue: a Qwen base (not
    # instruct) checkpoint, so the ChatML-wrapped SPIRAL prompt template is used
    # the same "off-label" way it is on Qwen3-4B-Base. Check
    # https://tinker-docs.thinkingmachines.ai/tinker/models.json for the live
    # list -- it changes, and a model that vanishes from it fails at client
    # creation, not at import.
    model_name: str = "Qwen/Qwen3.5-9B-Base"
    lora_rank: int = 32  # oat trained every parameter; there is no rank that
    # makes LoRA equivalent, this is just a capacity knob.

    # --- rollout ------------------------------------------------------------
    # oat's --rollout_batch_size counts *trajectories* (one per model turn),
    # not games: SelfPlayActor.step() plays whole games until it has at least
    # this many turns, then subsamples down to exactly this many. We do the
    # same, so 128 turns is ~8-13 KuhnPoker games and ~2-3 PigDice games.
    turns_per_step: int = 128
    num_steps: int = 400
    # An episode is inherently sequential (turn t+1's observation depends on
    # turn t's action), so throughput comes from playing many games at once.
    # Each concurrent game is one thread blocking on one Tinker sample future.
    max_concurrent_games: int = 32
    # Safety valve: if the action parser is broken every game ends after one
    # turn, and without this we would spin forever trying to reach
    # turns_per_step. Not an oat flag.
    max_games_per_step: int = 512

    max_turns: int = 50  # SelfPlayArgs.max_turns; truncation scores a draw
    max_model_len: int = 12800  # oat --max_model_len
    generate_max_length: int = 4096  # oat --generate_max_length
    temperature: float = 1.0
    top_p: float = 1.0
    prompt_template: str = "qwen3"  # key into spiral.template.TEMPLATE_FACTORY

    # "auto" | "on" | "off" -- whether to append /no_think to the observation.
    # spiral's qwen3 template targets a *base* model, which has no thinking
    # mode. On a hybrid-thinking instruct model the same prompt opens a <think>
    # block that does not close inside generate_max_length, so no \boxed{} is
    # ever emitted and every game is a turn-1 forfeit. Measured on Qwen3-8B:
    # 99.8% invalid actions, mean game length 1.002, 4096 tokens per turn and
    # still reasoning. With /no_think: ~700 tokens and a clean \boxed{[bet]}.
    # "auto" turns it on for the models below and off for base models.
    thinking_mode: str = "auto"

    # --- reward shaping (SPIRAL's RAE) --------------------------------------
    use_role_baseline: bool = True
    role_baseline_ema_gamma: float = 0.95
    reward_scaling: float = 1.0
    gamma: float = 1.0
    use_intermediate_rewards: bool = True
    filter_zero_adv: bool = True
    ignore_no_eos: bool = True  # drop turns whose response hit the length cap

    # --- optimisation -------------------------------------------------------
    learning_rate: float = 1e-6
    num_ppo_epochs: int = 2
    # Tinker exposes "ppo" (clipped surrogate) and "importance_sampling"
    # (unclipped). oat runs clipped PPO, and with num_ppo_epochs=2 the second
    # pass is off-policy enough that the clip matters, so "ppo" is the faithful
    # choice. The thresholds are ratio bounds, i.e. oat's eps_clip=0.2 default
    # expressed as [1-eps, 1+eps].
    loss_fn: str = "ppo"
    clip_low_threshold: float = 0.8
    clip_high_threshold: float = 1.2
    # Purely a request-size knob: forward_backward accumulates gradients and
    # optim_step applies them, so chunking a batch does not change the update.
    fwd_bwd_chunk_size: int = 16

    # --- eval ---------------------------------------------------------------
    eval_steps: int = 16
    eval_games: int = 16
    eval_temperature: float = 0.6
    eval_top_p: float = 0.95
    eval_generate_max_length: int = 4096
    eval_player_id: int = 0  # SelfPlayActor.online_model_player = actor_id % 2
    # oat's upstream default eval opponent (gemini-2.0-flash-lite-001) is retired
    # and 404s on OpenRouter, which aborts the whole job at the step-0 eval; all
    # three run scripts pin `random`. Only `random` is implemented here.
    eval_opponent: str = "random"

    # --- checkpointing ------------------------------------------------------
    save_steps: int = 16

    # --- arm-derived (filled by from_args) ----------------------------------
    env_ids: list[str] = field(default_factory=lambda: ["KuhnPoker-v1"])
    use_llm_obs_wrappers: list[bool] = field(default_factory=lambda: [True])
    eval_env_ids: list[str] = field(
        default_factory=lambda: ["TicTacToe-v0", "KuhnPoker-v1"]
    )
    eval_use_llm_obs_wrappers: list[bool] = field(
        default_factory=lambda: [False, True]
    )

    # --- misc ---------------------------------------------------------------
    use_wandb: bool = False
    wandb_project: str = "strategy-behavior"

    @property
    def suppress_thinking(self) -> bool:
        """Resolve `thinking_mode` against the model name.

        A *-Base checkpoint has no thinking mode and no `/no_think` handling, so
        appending the marker there would just put a stray token in the
        observation. Everything else in the Qwen3/Qwen3.5/Qwen3.6 families is
        hybrid-thinking and needs it.
        """
        if self.thinking_mode == "on":
            return True
        if self.thinking_mode == "off":
            return False
        if self.thinking_mode != "auto":
            raise ValueError(f"thinking_mode must be auto/on/off, got {self.thinking_mode!r}")
        name = self.model_name
        if name.endswith("-Base") or "-Base:" in name:
            return False
        return name.startswith(("Qwen/Qwen3-", "Qwen/Qwen3.5-", "Qwen/Qwen3.6-"))

    @property
    def max_prompt_tokens(self) -> int:
        """Token budget for the prompt, so prompt + generation fits max_model_len.

        SPIRAL has no equivalent: vLLM was configured with --max_model_len and
        oat never had to think about it, because the observation for these games
        never gets near 12800 tokens. It is enforced here anyway -- a Tinker
        sample() call that exceeds the context window raises rather than
        truncating, which would kill a whole batch of games mid-collection.
        """
        return self.max_model_len - self.generate_max_length

    @property
    def env_to_llm_obs_wrapper(self) -> dict[str, bool]:
        return dict(zip(self.env_ids, self.use_llm_obs_wrappers, strict=True))

    @property
    def eval_env_to_llm_obs_wrapper(self) -> dict[str, bool]:
        return dict(zip(self.eval_env_ids, self.eval_use_llm_obs_wrappers, strict=True))

    def validate(self) -> None:
        if len(self.env_ids) != len(self.use_llm_obs_wrappers):
            raise ValueError(
                f"env_ids ({len(self.env_ids)}) and use_llm_obs_wrappers "
                f"({len(self.use_llm_obs_wrappers)}) must be the same length"
            )
        if len(self.eval_env_ids) != len(self.eval_use_llm_obs_wrappers):
            raise ValueError(
                f"eval_env_ids ({len(self.eval_env_ids)}) and "
                f"eval_use_llm_obs_wrappers "
                f"({len(self.eval_use_llm_obs_wrappers)}) must be the same length"
            )
        if self.max_prompt_tokens <= 0:
            raise ValueError(
                f"generate_max_length ({self.generate_max_length}) leaves no room "
                f"for a prompt inside max_model_len ({self.max_model_len})"
            )
        if self.eval_opponent != "random":
            raise ValueError(
                f"eval_opponent={self.eval_opponent!r}: only 'random' is "
                "implemented; the LLM opponents oat supports would need an "
                "OpenRouter client here"
            )
        if self.loss_fn not in ("ppo", "importance_sampling"):
            raise ValueError(f"unknown loss_fn {self.loss_fn!r}")

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True)


def build_config(arm: str, scale: str, overrides: dict[str, Any]) -> SpiralTinkerConfig:
    """Compose arm preset -> scale preset -> explicit CLI overrides.

    Order matters: the arm sets which games are played (and PigDice's
    save_steps=64), the scale sets how much of it to do, and anything the user
    passed on the command line wins over both.
    """
    if arm not in ARMS:
        raise ValueError(f"unknown arm {arm!r}; choose from {sorted(ARMS)}")
    if scale not in SCALES:
        raise ValueError(f"unknown scale {scale!r}; choose from {sorted(SCALES)}")

    values: dict[str, Any] = {"arm": arm, "scale": scale}
    values.update(ARMS[arm])
    values.update(SCALES[scale])
    # PigDice's save_steps=64 is an arm property, but "smoke"/"short" set
    # save_steps too and a 64-step cadence in a 2-step smoke run means no
    # checkpoint at all. Scale wins for the small scales; the arm wins at full.
    if arm == "pigdice" and scale == "full":
        values["save_steps"] = ARMS["pigdice"]["save_steps"]
    values.update({k: v for k, v in overrides.items() if v is not None})

    known = {f.name for f in fields(SpiralTinkerConfig)}
    unknown = set(values) - known
    if unknown:
        raise ValueError(f"unknown config keys: {sorted(unknown)}")

    cfg = SpiralTinkerConfig(**values)
    cfg.validate()
    return cfg
