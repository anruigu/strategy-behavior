"""SPIRAL self-play against the Tinker sampling API.

This is the half of `train_spiral.py` that does not need GPUs: the TextArena
game loop, the prompt template, the action parser, and SPIRAL's role-conditioned
advantage baseline (RAE). It talks to a model only through a `TurnSampler`
callable, so the whole file is testable offline with a stub sampler
(`--dry-run` in train_tinker.py does exactly that).

Everything game-facing is imported from the upstream `spiral` checkout rather
than re-implemented, so this port cannot silently drift from the oat arms:

    spiral.envs                 KuhnPoker-v1 / PigDice-v1 / ... registration
    spiral.template             the exact prompt string the oat runs use
    spiral.agents.utils         per-env valid-action parsers
    spiral.agents.random        the `random` eval opponent
    spiral.utils                extract_boxed_answer

`spiral` is added to sys.path rather than pip-installed: `pip install -e spiral`
drags in oat, vllm and deepspeed, which is the entire multi-GB GPU stack this
port exists to avoid. The modules above need only `textarena`.
"""

from __future__ import annotations

import re
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Protocol

# Copied verbatim from train_spiral.py:55. Any action string the env would not
# accept is mapped to this sentinel, and producing it forfeits the game.
INVALID_ACTION = "[｜INVALID_ACTION｜]"

# train_spiral.py routes these through extract_chat_action() instead of the
# action-space check: they have no enumerable action space.
#
# IPD is here for a slightly different reason: it alternates a free-text
# communication turn with a [Cooperate]/[Defect] decision turn, so its action
# space is enumerable only half the time and a single per-env parser cannot
# describe it. Routing it freeform hands the raw text to the env, which applies
# exactly the rule the POC uses (`defect iff '[Defect]' appears, else
# cooperate`). The alternative -- an action-space check -- would forfeit every
# conversation turn as an invalid action, and would also punish the rambling
# no-token decisions that the POC instead counts as `invalid_decisions` and lets
# the env score as cooperate. Freeform keeps this arm comparable to T1/A2.
_FREEFORM_ACTION_ENVS = ("DontSayIt-v0", "SimpleNegotiation-v1")

# Envs scored on ABSOLUTE own payoff instead of the env's win/lose/draw reward.
#
# Every other env here is zero-sum, so set_winner()'s {+1,-1} is the whole story.
# IPD is general-sum and its terminal reward is set_winner(higher score), which
# maps BOTH mutual cooperation (30-30) and mutual defection (10-10) to a draw --
# a signal that cannot see welfare at all and only rewards out-scoring the
# opponent. Training the self-play ablation on that would make "the exploitation
# gradient erodes" true by construction.
#
# The POC's T1/A2 arms optimise `my_score` (ipd_exp/train_ipd.py), so this arm
# does too: only the OPPONENT differs, which is the point of the ablation.
#
# Scale: T1 standardises its group-relative advantages, `(r - mu) / sd`, landing
# them near +-1. RAE subtracts an EMA baseline but does NOT divide by a spread,
# so a raw 0..50 episode score would produce advantages ~25x larger than T1's at
# the same learning rate. Reporting the per-round mean (0..5) puts the shaped
# advantage back in T1's ballpark; `reward_scaling` remains the knob on top.
_ABSOLUTE_SCORE_ENVS = ("IteratedPrisonersDilemma-v1",)

# Envs whose action is the raw response text, with no \boxed{} contract at all.
# See extract_raw_action.
_RAW_ACTION_ENVS = ("IteratedPrisonersDilemma-v1",)


# Per-env prompt builders, overriding spiral's template entirely.
#
# spiral's `qwen3` template is raw ChatML written for a BASE model: it prepends
# "You are playing a two-player zero-sum game. Make valid actions to win.",
# asks the model to "reason step by step, and put your final answer within
# \boxed{}", and suppresses thinking only via a soft `/no_think` marker.
#
# All three are wrong for the IPD ablation:
#   * IPD is not zero-sum, and "win" is a framing that pushes toward defection
#     -- precisely the disposition being measured. T1/A2 train and are evaluated
#     under ipd_lib.NEUTRAL.
#   * the \boxed{} contract is not what ipd_exp's eval battery speaks, so a
#     checkpoint trained that way is format-mismatched to its own measurement.
#   * the soft marker does not work on Qwen3.5-9B here: measured, the <think>
#     block is still open at 2048 tokens, so no \boxed{} is emitted and every
#     game is a turn-1 forfeit (observed: invalid_action_rate 100%).
#     `tokenizer.apply_chat_template(..., enable_thinking=False)` is the
#     supported switch and is what ipd_exp/tinker_actor.py uses.
#
# Registering a builder here swaps in the POC's exact prompt, which is what
# makes the arm an ablation of the OPPONENT rather than of the prompt too.
_PROMPT_OVERRIDES: dict[str, Callable[[str], str]] = {}


def register_prompt_override(env_id: str, builder: Callable[[str], str]) -> None:
    _PROMPT_OVERRIDES[env_id] = builder


def _absolute_score_rewards(env) -> dict[int, float] | None:
    """Per-round mean payoff per seat, or None if the env exposes no scores."""
    try:
        gs = env.state.game_state
        scores = gs["scores"]
        rounds = gs.get("num_rounds") or gs.get("current_round") or 1
        return {int(k): float(v) / max(int(rounds), 1) for k, v in scores.items()}
    except Exception:  # noqa: BLE001
        return None


def import_spiral(spiral_dir: str | Path) -> None:
    """Put an unpacked spiral checkout on sys.path and import its env registry.

    Raises with a pointed message rather than letting a bare ImportError
    surface: the two things that actually go wrong here are a wrong
    `$SPIRAL_DIR` and a spiral checkout without the PigDice parser patch, and
    neither is obvious from `ModuleNotFoundError: spiral`.
    """
    spiral_dir = Path(spiral_dir).expanduser().resolve()
    if not (spiral_dir / "spiral" / "envs" / "__init__.py").is_file():
        raise SystemExit(
            f"no spiral checkout at {spiral_dir}\n"
            "  git clone https://github.com/spiral-rl/spiral $SPIRAL_DIR\n"
            "(set SPIRAL_DIR in ../../config.sh, or pass --spiral-dir)"
        )
    if str(spiral_dir) not in sys.path:
        sys.path.insert(0, str(spiral_dir))
    try:
        import spiral.envs  # noqa: F401  (import registers the TextArena env ids)
    except ImportError as e:  # textarena missing, most likely
        raise SystemExit(
            f"could not import spiral from {spiral_dir}: {e}\n"
            "This port needs only `textarena` from spiral's dependency set "
            "(not oat/vllm/deepspeed); see requirements.txt."
        ) from e


def require_action_parser(env_id: str) -> None:
    """Fail at startup, not on the first rollout, if an env has no parser.

    Upstream spiral registers PigDice-v1 but never added it to
    `_VALID_ACTION_PARSER`; without `training/patches/action-parsers.patch`
    the run dies from `agent_act()` on the first turn. `sbatch_pigdice.sh` checks
    for this up front and so do we -- more so here, because by the time the
    first rollout happens we have already paid to create a Tinker LoRA client.
    """
    from spiral.agents.utils import get_valid_action_parser

    if env_id in _FREEFORM_ACTION_ENVS or env_id in _RAW_ACTION_ENVS:
        return
    try:
        get_valid_action_parser(env_id)
    except NotImplementedError as e:
        raise SystemExit(
            f"{e}\n"
            "If this is PigDice-v1, apply the parser patch to your spiral "
            "checkout:\n"
            "  git -C $SPIRAL_DIR apply "
            "$SAT_HOME/training/patches/action-parsers.patch"
        ) from e


# --- role-conditioned advantage estimation (RAE) ----------------------------


class _EMA:
    """spiral.utils.EMA, re-declared so this module imports without oat."""

    def __init__(self, decay: float) -> None:
        assert 0.0 < decay < 1.0, "Decay must be between 0 and 1"
        self.decay = decay
        self.value = 0.0

    def update(self, x: float) -> float:
        self.value = self.decay * self.value + (1 - self.decay) * x
        return self.value

    def get(self) -> float:
        return self.value


class RoleBaseline:
    """SPIRAL's per-(game, seat) return baseline.

    A group-relative baseline (GRPO-style) does not work in two-player self-play:
    the two seats of a zero-sum game have systematically different expected
    returns (the dealer in Kuhn, the first mover in TicTacToe), so pooling them
    subtracts a baseline that is wrong for both. SPIRAL keeps one EMA per
    (env_id, player_id) instead.

    The read-then-update order is load-bearing and matches
    `SelfPlayActor.prepare_trajectories`: the baseline subtracted from a game's
    return must not include that game's own return, or the estimate is biased
    toward zero advantage.
    """

    def __init__(self, env_ids: list[str], decay: float) -> None:
        self._ema = {
            env_id: {0: _EMA(decay), 1: _EMA(decay)} for env_id in env_ids
        }

    def shape(self, env_id: str, player_id: int, reward: float) -> float:
        ema = self._ema[env_id][player_id]
        baseline = ema.get()
        ema.update(reward)
        return reward - baseline

    def snapshot(self) -> dict[str, dict[int, float]]:
        return {
            env_id: {pid: e.get() for pid, e in per_seat.items()}
            for env_id, per_seat in self._ema.items()
        }


# --- action extraction ------------------------------------------------------


def extract_action(text: str, action_space: list[str], template: str) -> str:
    """Port of `SelfPlayActor.extract_action` for the qwen3/llama_instruct path.

    Kept step-for-step identical, including the heuristics that look odd out of
    context, because the action parser is the single place where a "port" most
    easily becomes a different experiment: loosen the bracket heuristic and the
    invalid-action forfeit rate drops, which changes the reward distribution
    without changing anything you would notice in a log line.
    """
    if not text:
        return ""  # train_spiral.py returns "" (not INVALID_ACTION) for empty text

    from spiral.utils import extract_boxed_answer

    try:
        if template in ("qwen", "qwen3", "llama_instruct"):
            raw_action = extract_boxed_answer(text)
            if raw_action is None:
                raw_action = text.strip()
        elif template == "r1":
            answer_match = re.search(r"<answer>(.*?)</answer>", text, re.DOTALL)
            if answer_match:
                raw_action = answer_match.group(1).strip()
            elif re.search(r"<think>(.*?)</think>", text, re.DOTALL):
                think_end = text.find("</think>") + len("</think>")
                raw_action = text[think_end:].strip()
            else:
                raw_action = text.strip()
        else:
            raise NotImplementedError(f"no action extraction for template {template!r}")

        # 1. \boxed{roll} -> [roll]
        formatted_action = re.sub(r"\\boxed\{([^}]*)\}", r"[\1]", raw_action)

        # 2. a short unbracketed answer probably meant to be bracketed
        if "[" not in formatted_action and "]" not in formatted_action:
            if len(formatted_action.split()) <= 5:
                formatted_action = f"[{formatted_action}]"

        # 3. collapse whitespace
        formatted_action = re.sub(r"\s+", " ", formatted_action).strip()

        # 4. strictly enforce the action space
        if formatted_action not in action_space:
            return INVALID_ACTION
        return formatted_action
    except Exception:
        return INVALID_ACTION


def extract_raw_action(text: str) -> str:
    """The whole response IS the action; the env parses it.

    `_FREEFORM_ACTION_ENVS` still routes through `extract_chat_action`, which
    forfeits anything without a `\\boxed{}` -- fine for SimpleNegotiation, whose
    prompt asks for one, but wrong for IPD under ipd_exp's prompt, which does
    not. Routing IPD there produced a 100% invalid-action rate.

    ipd_exp/ipd_lib.py takes the sampled text verbatim and lets the env decide
    (`defect iff '[Defect]' appears, else cooperate`), and an empty response
    falls back to a cooperate/no-comment placeholder rather than forfeiting.
    Mirrored here so a rambling decision turn is scored the way T1 scores it --
    as a cooperate, counted in the invalid-decision statistic -- instead of
    ending the game.
    """
    stripped = text.strip()
    return stripped if stripped else "(no comment)"


def extract_chat_action(text: str) -> str:
    """Port of `SelfPlayActor.extract_chat_action` (SimpleNegotiation, DontSayIt).

    No action-space check: the env parses the trailing `[...]` itself. Only a
    missing or empty \\boxed{} forfeits.
    """
    from spiral.utils import extract_boxed_answer

    answer = extract_boxed_answer(text)
    if answer is None:
        return INVALID_ACTION
    raw_action = answer.strip()
    if raw_action.strip("\n ") == "":
        return INVALID_ACTION
    return raw_action


def action_from_response(response_text: str, observation: str, env_id: str, template: str) -> str:
    if env_id in _RAW_ACTION_ENVS:
        return extract_raw_action(response_text)
    if env_id in _FREEFORM_ACTION_ENVS:
        return extract_chat_action(response_text)
    from spiral.agents.utils import get_valid_action_parser

    action_space = get_valid_action_parser(env_id)(observation)
    return extract_action(response_text, action_space, template)


# --- rollout types ----------------------------------------------------------


@dataclass
class Sampled:
    """One model turn, as returned by the sampler."""

    prompt_ids: list[int]
    response_ids: list[int]
    response_logprobs: list[float]
    text: str
    truncated: bool  # stop_reason == "length"


class TurnSampler(Protocol):
    def __call__(self, prompt_text: str) -> Sampled | None:
        """Sample one action. Returns None if the prompt exceeds the budget."""
        ...


@dataclass
class Turn:
    player_id: int
    turn_index: int
    prompt_ids: list[int]
    response_ids: list[int]
    response_logprobs: list[float]
    response_text: str
    action: str
    action_is_valid: bool
    truncated: bool


@dataclass
class GameResult:
    env_id: str
    turns: dict[int, list[Turn]] = field(default_factory=lambda: {0: [], 1: []})
    rewards: dict[int, float] = field(default_factory=dict)
    num_turns: int = 0
    # "normal" | "invalid_action" | "turn_limit" | "context_limit" | "error"
    outcome: str = "normal"
    error: str | None = None

    @property
    def num_invalid(self) -> int:
        return sum(
            1 for ts in self.turns.values() for t in ts if not t.action_is_valid
        )


# --- the game loop ----------------------------------------------------------


def play_game(
    env_id: str,
    use_llm_obs_wrapper: bool,
    sampler: TurnSampler,
    *,
    seed: int,
    max_turns: int,
    template: str,
    model_player_id: int | None = None,
    opponent_act: Callable[[str], str] | None = None,
    no_think: bool = False,
) -> GameResult:
    """Play one game; by default the same policy occupies both seats.

    Pass `model_player_id` + `opponent_act` to play the eval configuration
    instead: the model takes one seat and a fixed opponent (`RandomAgent`) takes
    the other. Opponent turns are stepped into the env but not recorded, so the
    returned `turns` only ever contain model turns.

    Follows `SelfPlayActor.play_game_vectorized` for a single env, including the
    two reward overrides that are easy to miss:

      - an invalid action ends the game immediately with {offender: -1.5,
        other: +0.5}. That is harsher than a loss (-1) on purpose: the model
        should prefer losing legally to emitting something unparseable.
      - hitting max_turns scores a draw (0/0) for both seats, so a stalling
        policy gains nothing.

    `context_limit` is new here (see `Sampled | None`): oat let vLLM's
    --max_model_len handle it, but a Tinker sample() call whose prompt exceeds
    the context window raises, which would take down every game sharing the
    thread pool. We score it as a draw and count it, so a run that starts
    hitting the cap shows up in the metrics instead of as a crash.
    """
    from spiral.envs import make_env

    result = GameResult(env_id=env_id)
    env = make_env(env_id, use_llm_obs_wrapper=use_llm_obs_wrapper)
    env.reset(num_players=2, seed=seed)
    # oat sets this so a malformed action is a forfeit rather than a re-prompt;
    # the invalid-action penalty below assumes it.
    env.state.error_allowance = 0

    rewards: dict[int, float] | None = None
    turn_count = 0

    if (model_player_id is None) != (opponent_act is None):
        raise ValueError("model_player_id and opponent_act must be given together")

    try:
        while True:
            player_id, observation = env.get_observation()
            is_model_turn = model_player_id is None or player_id == model_player_id

            if is_model_turn:
                _override = _PROMPT_OVERRIDES.get(env_id)
                prompt_text = (
                    _override(observation)
                    if _override is not None
                    else _format_observation(observation, template, no_think)
                )
                sampled = sampler(prompt_text)
                if sampled is None:
                    rewards = {0: 0.0, 1: 0.0}
                    result.outcome = "context_limit"
                    break

                action = action_from_response(
                    sampled.text, observation, env_id, template
                )
                result.turns[player_id].append(
                    Turn(
                        player_id=player_id,
                        turn_index=turn_count,
                        prompt_ids=sampled.prompt_ids,
                        response_ids=sampled.response_ids,
                        response_logprobs=sampled.response_logprobs,
                        response_text=sampled.text,
                        action=action,
                        action_is_valid=action != INVALID_ACTION,
                        truncated=sampled.truncated,
                    )
                )
            else:
                assert opponent_act is not None
                action = opponent_act(observation)

            turn_count += 1
            done, _info = env.step(action=action)
            if action == INVALID_ACTION:
                rewards = {0: 0.5, 1: 0.5}
                rewards[player_id] = -1.5
                result.outcome = "invalid_action"
                break
            if done:
                break

            if turn_count >= max_turns:
                rewards = {0: 0.0, 1: 0.0}
                result.outcome = "turn_limit"
                break

        if rewards is None:
            closed = env.close()
            # textarena <=0.6.4 returns just the reward dict; the newer checkout
            # in /workspace/allie/TextArena returns (rewards, info). Unpacking
            # blind means .items() raises on the tuple, which the except below
            # would swallow as an "error" game scored 0/0 -- i.e. every single
            # game silently zero-reward. Handle both shapes.
            if isinstance(closed, tuple):
                closed = closed[0] if closed else None
            rewards = closed or {0: 0.0, 1: 0.0}

        # General-sum envs are scored on own payoff, overriding the win/lose/draw
        # reward AND the turn-limit / context-limit draws above: a game that ran
        # 8 of 10 rounds still earned real points, and calling that 0 would train
        # the policy to treat a truncated game as a neutral outcome.
        if env_id in _ABSOLUTE_SCORE_ENVS:
            abs_rewards = _absolute_score_rewards(env)
            if abs_rewards is not None:
                rewards = abs_rewards
    except Exception as e:  # a single bad game must not kill the batch
        result.outcome = "error"
        result.error = f"{type(e).__name__}: {e}"
        rewards = {0: 0.0, 1: 0.0}

    result.rewards = {int(k): float(v) for k, v in rewards.items()}
    result.num_turns = turn_count
    return result


# Qwen3 / Qwen3.5 hybrid-thinking models honour this soft switch in the user
# turn; it makes them emit an empty <think></think> and answer directly.
NO_THINK_MARKER = "\n/no_think"


def _format_observation(
    observation: str, template: str, no_think: bool = False
) -> str:
    """Render spiral's prompt template, optionally suppressing the think block.

    Why the switch exists: spiral's `qwen3` template was written for a *base*
    model (Qwen3-4B-Base), which has no thinking mode, so it ends the prompt at
    `<|im_start|>assistant\\n` and asks for `\\boxed{}`. Point the same template
    at a hybrid-thinking instruct model and it opens a `<think>` block that does
    not close inside `generate_max_length` -- measured on Qwen/Qwen3-8B, a
    round-1 KuhnPoker decision runs past 4096 tokens still reasoning. No
    `\\boxed{}` is ever emitted, `extract_action` falls through to the whole
    response text, and that is not in the action space, so *every game is a
    turn-1 forfeit*. Observed rate: 99.8% invalid actions, mean game length
    1.002. With `/no_think` the same prompt returns in ~700 tokens with a clean
    `\\boxed{[bet]}`.

    This is a real divergence from the oat run scripts, and it has to be applied
    on BOTH sides for a Tinker-vs-local comparison to be matched -- see
    ../patches/qwen3-no-think-template.patch.
    """
    from spiral.template import TEMPLATE_FACTORY

    if no_think:
        observation = observation + NO_THINK_MARKER
    return TEMPLATE_FACTORY[template](observation, system_prompt=None)


def play_games_concurrently(
    specs: list[tuple[str, bool, int]],
    sampler_factory: Callable[[str], TurnSampler],
    *,
    max_workers: int,
    max_turns: int,
    template: str,
    model_player_id: int | None = None,
    opponent_factory: Callable[[str], Callable[[str], str]] | None = None,
    no_think: bool = False,
) -> list[GameResult]:
    """Play `specs` = [(env_id, use_llm_obs_wrapper, seed), ...] in parallel.

    An episode is sequential, so all of the throughput here comes from having
    many episodes in flight: each worker thread runs one game and blocks on one
    Tinker sample future at a time. With 32 workers and ~12 turns per KuhnPoker
    game, a 128-turn batch is ~12 sequential round-trips of wall-clock rather
    than ~128.

    Results come back in `specs` order, not completion order. That matters: the
    RAE baseline is updated once per game, so consuming games in a
    nondeterministic order would make a seeded run irreproducible.

    `sampler_factory(env_id)` is called once per game rather than shared, in
    case a sampler carries per-game state; the underlying Tinker sampling client
    is shared and does the actual request multiplexing.
    """
    if not specs:
        return []
    workers = max(1, min(max_workers, len(specs)))

    def _run(spec: tuple[str, bool, int]) -> GameResult:
        env_id, use_llm_obs, seed = spec
        opponent = opponent_factory(env_id) if opponent_factory is not None else None
        return play_game(
            env_id,
            use_llm_obs,
            sampler_factory(env_id),
            seed=seed,
            max_turns=max_turns,
            template=template,
            model_player_id=model_player_id,
            opponent_act=opponent,
            no_think=no_think,
        )

    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(_run, specs))


# --- turn -> training example ----------------------------------------------


@dataclass
class TrainingTurn:
    """A turn that survived filtering, with its RAE-shaped advantage."""

    env_id: str
    player_id: int
    prompt_ids: list[int]
    response_ids: list[int]
    response_logprobs: list[float]
    advantage: float
    info: dict[str, Any]


def game_to_training_turns(
    game: GameResult,
    baseline: RoleBaseline | None,
    *,
    reward_scaling: float,
    gamma: float,
    use_intermediate_rewards: bool,
    filter_zero_adv: bool,
    ignore_no_eos: bool,
) -> list[TrainingTurn]:
    """Port of `SelfPlayActor.prepare_trajectories`.

    Both seats are trained (self-play has no fixed opponent here), each with its
    own RAE baseline. `use_intermediate_rewards` discounts a turn by
    gamma**(turns_from_end); all three run scripts pass --gamma 1, so by default
    every turn of a game carries the same advantage and this is a no-op -- kept
    because it is the flag you would reach for first if credit assignment
    across a 50-turn PigDice game turned out to be the problem.
    """
    out: list[TrainingTurn] = []
    for player_id in (0, 1):
        player_turns = game.turns[player_id]

        player_reward = game.rewards.get(player_id, 0.0) * reward_scaling
        raw_reward = player_reward
        if baseline is not None:
            # Before the empty check, deliberately. spiral iterates both seats
            # unconditionally and updates the EMA from `rewards[player_id]`
            # whether or not that seat ever moved -- and a seat routinely does
            # not, because an invalid action on turn 0 ends the game before the
            # opponent acts. Skipping the update there makes the two baselines
            # diverge within a handful of games (caught by test_parity.py).
            player_reward = baseline.shape(game.env_id, player_id, player_reward)

        if not player_turns:
            continue

        for i, turn in enumerate(player_turns):
            if use_intermediate_rewards:
                turns_from_end = len(player_turns) - i - 1
                advantage = player_reward * (gamma**turns_from_end)
            else:
                advantage = player_reward

            # A zero advantage contributes no gradient but a full forward pass;
            # oat drops those turns to make the batch cheaper and less noisy.
            # Evaluated on the pre-mask advantage, matching spiral's ordering.
            if filter_zero_adv and advantage == 0:
                continue
            if not turn.response_ids:
                continue

            # A response cut off by the length cap has no terminating token, so
            # its last-token credit lands on an arbitrary mid-thought token.
            # spiral does NOT drop these -- it sets TransitionData.loss_mask=False
            # and keeps them, so they still occupy a slot in the rollout batch.
            # Tinker has no mask key; the equivalent is a zero advantage, which
            # zeroes the PPO surrogate for every token of the turn. Keeping the
            # turn (rather than dropping it) matters because we subsample to
            # exactly turns_per_step: drop it and a live turn takes its slot, so
            # the batch would carry more gradient signal than oat's does.
            # Cost: a forward/backward pass billed for zero gradient, on the
            # order of the truncation rate.
            masked = ignore_no_eos and turn.truncated
            if masked:
                advantage = 0.0

            out.append(
                TrainingTurn(
                    env_id=game.env_id,
                    player_id=player_id,
                    prompt_ids=turn.prompt_ids,
                    response_ids=turn.response_ids,
                    response_logprobs=turn.response_logprobs,
                    advantage=float(advantage),
                    info={
                        "turn": turn.turn_index,
                        "game_length": game.num_turns,
                        "action_is_valid": turn.action_is_valid,
                        "loss_masked": masked,
                        "final_reward": raw_reward,
                        "shaped_reward": player_reward,
                        "outcome": game.outcome,
                        "draw": game.rewards.get(0) == game.rewards.get(1) == 0,
                    },
                )
            )
    return out
