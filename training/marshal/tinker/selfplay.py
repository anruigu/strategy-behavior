"""MARSHAL Kuhn Poker self-play against the Tinker sampling API.

MARSHAL (https://arxiv.org/abs/2510.15414, ICLR 2026) is multi-agent self-play RL
on OpenSpiel games, built on ROLL. This is the GPU-free half of it: the game
loop, the chat construction, the action parser, and MARSHAL's two contributions
to credit assignment -- the turn-level advantage estimator and agent-specific
advantage normalization.

Everything game-facing is imported from the upstream MARSHAL checkout rather
than re-implemented, so the port cannot silently drift:

    roll.agentic.env.kuhn_poker.env     the OpenSpiel Kuhn env + prompt text
    roll.agentic.env.kuhn_poker.config  its config dataclass

Those two modules need only pyspiel / numpy / omegaconf / imageio / PIL -- NOT
ROLL's training stack (ray, hydra, Megatron, mcore_adapter), which is why this
arm installs in minutes rather than fighting a Megatron build.

## How this differs from the SPIRAL Tinker arm (../../tinker/)

Both play KuhnPoker self-play, which is the point -- it makes them comparable
against `results/`. They differ in almost everything else:

                  SPIRAL arm                     MARSHAL arm (here)
  env             TextArena KuhnPoker-v1         OpenSpiel kuhn_poker
                  5 rounds, ~9 model turns       1 hand, 2-3 model turns
  prompt          fresh single-turn re-render    growing multi-turn chat
  action format   \\boxed{bet}                    <think>..</think><answer><BET></answer>
  credit          RAE: per-(env,seat) EMA on     turn-level reward -> reverse
                  the final outcome              discounted return
  normalization   subtract the seat's EMA        per-player mean-centering of
                                                 rewards AND of advantages
  Datum           one per turn                   one per (episode, player),
                                                 multi-turn merged
"""

from __future__ import annotations

import re
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Protocol

# ROLL's parser returns these when the response does not match the required
# <think>..</think><answer>..</answer> shape. Copied from
# roll/agentic/rollout/env_manager.py::_parse_response.
INVALID = "INVALID"


def import_marshal(marshal_dir: str | Path) -> None:
    """Put a MARSHAL checkout on sys.path and import its Kuhn env.

    Imports the env module directly rather than `roll.agentic.env`, whose
    __init__ pulls in tictactoe/hanabi/connect_four/leduc as well. They are all
    equally light, but importing only what we use keeps the failure surface
    small and the error message pointed.
    """
    marshal_dir = Path(marshal_dir).expanduser().resolve()
    if not (marshal_dir / "roll" / "agentic" / "env" / "kuhn_poker" / "env.py").is_file():
        raise SystemExit(
            f"no MARSHAL checkout at {marshal_dir}\n"
            "  git clone https://github.com/thu-nics/MARSHAL $MARSHAL_DIR\n"
            "(set MARSHAL_DIR in ../../../config.sh, or pass --marshal-dir)"
        )
    if str(marshal_dir) not in sys.path:
        sys.path.insert(0, str(marshal_dir))
    try:
        import roll.agentic.env.kuhn_poker.env  # noqa: F401
    except ImportError as e:
        raise SystemExit(
            f"could not import MARSHAL's Kuhn env from {marshal_dir}: {e}\n"
            "This arm needs only pyspiel + numpy + omegaconf + imageio + pillow "
            "from ROLL's dependency set (not ray/hydra/Megatron); see "
            "requirements.txt."
        ) from e


def make_env(seed: int, built_in_opponent: str = "none", opponent_player: int = 1):
    from roll.agentic.env.kuhn_poker.config import KuhnPokerConfig
    from roll.agentic.env.kuhn_poker.env import KuhnPoker

    cfg = KuhnPokerConfig(
        seed=seed,
        render_mode="text",
        built_in_opponent=built_in_opponent,
        opponent_player=opponent_player,
    )
    return KuhnPoker(cfg)


# --- response parsing -------------------------------------------------------

# roll/agentic/rollout/env_manager.py::_parse_response. The anchored ^...$ and
# the exact tag shape are load-bearing: the prompt threatens "Responses that do
# not follow the format will result in immediate loss of the game", and the
# format_penalty below is what makes that true. Loosen this regex and you
# change the reward distribution, not just the parse rate.
_THINK_RE = re.compile(r"^<think>(.*?)</think>\s*<answer>(.*?)</answer>$", re.DOTALL)
_NOTHINK_RE = re.compile(r"^<answer>(.*?)</answer>$", re.DOTALL)


def parse_response(
    response: str, enable_think: bool, action_sep: str, special_tokens: list[str]
) -> tuple[str, list[str]]:
    """Port of ROLL's `_parse_response`.

    Returns (normalised_response_text, actions). `actions` is empty exactly when
    the format check failed, which is what the caller turns into a forfeit.
    """
    pattern = _THINK_RE if enable_think else _NOTHINK_RE
    match = pattern.search(response.strip())
    if not match:
        return (INVALID, [])

    if enable_think:
        think_content, action_content = match.group(1), match.group(2)
    else:
        think_content, action_content = "", match.group(1)

    for tok in special_tokens:
        action_content = action_content.replace(tok, "").strip()
        think_content = think_content.replace(tok, "").strip()

    actions = [a.strip() for a in action_content.split(action_sep) if a.strip()]
    # ROLL keeps only the first action per turn (max_actions = 1).
    actions = actions[:1]
    return (action_content, actions)


def action_to_id(action_text: str, legal_actions: dict[int, str]) -> int | None:
    """Map '<BET>' back to the OpenSpiel action id, or None if not legal.

    Matching is exact against the strings the prompt advertises. ROLL's env does
    the same lookup; anything else is a forfeit rather than a nearest match,
    because a nearest match would quietly rescue malformed outputs and depress
    the format-penalty rate the algorithm depends on.
    """
    for aid, text in legal_actions.items():
        if text == action_text:
            return aid
    return None


# --- rollout types ----------------------------------------------------------


@dataclass
class Sampled:
    response_ids: list[int]
    response_logprobs: list[float]
    text: str
    truncated: bool


class TurnSampler(Protocol):
    def __call__(self, prompt_ids: list[int]) -> Sampled | None: ...


@dataclass
class PlayerTrace:
    """One player's whole episode as a single growing token sequence.

    `tokens` is the full chat (system + user + assistant + user + ...) as it
    would be tokenised at the end of the episode. `spans` marks the assistant
    stretches, which are the only positions that carry advantage.
    """

    player_id: int
    tokens: list[int] = field(default_factory=list)
    logprobs: list[float] = field(default_factory=list)
    # (start, end) half-open index pairs into `tokens`, one per assistant turn
    spans: list[tuple[int, int]] = field(default_factory=list)
    turn_scores: list[float] = field(default_factory=list)
    n_invalid: int = 0
    n_truncated: int = 0
    # Non-zero when re-tokenising the grown chat changed already-emitted tokens,
    # which would break the prefix assumption the merged Datum relies on.
    prefix_breaks: int = 0


@dataclass
class EpisodeResult:
    traces: dict[int, PlayerTrace]
    returns: dict[int, float]
    n_turns: int = 0
    outcome: str = "normal"  # normal | invalid_action | turn_limit | context_limit | error
    error: str | None = None


# --- the episode loop -------------------------------------------------------


class ChatBuilder:
    """Incrementally tokenises a growing ChatML conversation.

    ROLL renders each player's whole episode as one chat and trains on all the
    assistant turns at once, so the natural Tinker representation is one Datum
    per (episode, player) with several action spans -- the multi-turn case in
    tinker-cookbook's `trajectory_to_data`. That is only valid if turn t+1's
    tokenisation extends turn t's as a strict prefix. ChatML is append-only so
    it normally does, but a tokeniser can still merge across the boundary; when
    that happens we count it in `prefix_breaks` and keep the longest valid
    prefix rather than silently mis-aligning the advantages.
    """

    def __init__(self, tokenizer: Any, system: str, user: str) -> None:
        self._tok = tokenizer
        text = tokenizer.apply_chat_template(
            [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            add_generation_prompt=True,
            tokenize=False,
        )
        self._ids: list[int] = tokenizer.encode(text, add_special_tokens=False)
        self._im_end: int = tokenizer.encode("<|im_end|>", add_special_tokens=False)[0]
        self._needs_im_end = False

    def prompt_ids(self) -> list[int]:
        return list(self._ids)

    def commit_response(self, response_ids: list[int]) -> None:
        """Append the tokens the model actually emitted, verbatim.

        Tinker returns the stop token as part of the sequence -- a sampled turn
        ends ...`</answer>`, `<|im_end|>`. So the assistant turn is already
        closed and the next delta must NOT re-open it; emitting a second
        <|im_end|> desynchronises the ChatML from turn 2 onward, and the model
        then answers into a malformed conversation and fails the format check.
        That showed up as a 54% invalid-action rate with no error anywhere.

        A truncated turn (stop_reason == "length") has no <|im_end|>, so track
        it per turn rather than assuming either way.

        Placing the turn reward on the last response token also lands it exactly
        on <|im_end|>, which is where ROLL's `get_masks_and_scores` puts it.
        """
        self._ids.extend(response_ids)
        self._needs_im_end = not (response_ids and response_ids[-1] == self._im_end)

    def add_user(self, content: str) -> None:
        """Append the ChatML delta for one more user turn + generation prompt.

        Deliberately NOT `apply_chat_template` over a growing message list.
        Re-rendering re-tokenises the assistant turns, and a decoded->re-encoded
        response does not always reproduce the token ids that were sampled --
        measured at 5 breaks in 31 turns on Qwen3-8B. Every break either
        mis-aligns the advantages against the logprobs or (with the guard in
        `_append_turn`) throws away the earlier turns of that episode.

        Appending the delta instead means the sequence we train on is exactly
        the sequence we sampled from, token for token, so the prefix property
        the merged Datum needs holds by construction. The sampler stops at
        <|im_end|> without emitting it, so the delta re-opens with it.
        """
        opener = "<|im_end|>\n" if self._needs_im_end else "\n"
        delta = (
            f"{opener}<|im_start|>user\n{content}<|im_end|>\n"
            "<|im_start|>assistant\n"
        )
        self._ids.extend(self._tok.encode(delta, add_special_tokens=False))


def play_episode(
    seed: int,
    sampler: TurnSampler,
    tokenizer: Any,
    *,
    max_turns: int,
    enable_think: bool,
    action_sep: str,
    special_tokens: list[str],
    format_penalty: float,
    max_prompt_tokens: int,
) -> EpisodeResult:
    """Play one self-play Kuhn hand; the policy occupies both seats.

    Reward shape, following ROLL's agentic pipeline:
      - every turn gets a score. Non-terminal turns score 0 unless the response
        failed the format check, which scores -format_penalty.
      - the terminal turn additionally carries the player's game return, which
        for OpenSpiel kuhn_poker is the chips won/lost (+/-1 or +/-2).
      - a format failure ends the episode immediately, mirroring the prompt's
        "responses that do not follow the format will result in immediate loss".
    """
    result = EpisodeResult(traces={}, returns={})
    env = make_env(seed=seed, built_in_opponent="none")

    try:
        obs, _execute = env.reset(seed=seed)

        # Chats are built lazily: the first user turn has to carry the rules
        # prefix AND the opening game state in one block, so it cannot be
        # constructed before we know what that seat sees.
        chats: dict[int, ChatBuilder] = {}
        traces: dict[int, PlayerTrace] = {0: PlayerTrace(0), 1: PlayerTrace(1)}
        result.traces = traces

        observation = obs["observation"]
        legal = obs["legal_actions"]
        pending_obs = {0: observation, 1: observation}
        turn_count = 0

        while True:
            pid = env.current_player
            trace = traces[pid]
            turn_msg = _turn_user_message(pending_obs[pid], legal)
            if pid not in chats:
                prefix = env.get_prompt(think=enable_think, player_id=pid)
                chats[pid] = ChatBuilder(
                    tokenizer, prefix["system"], prefix["user"] + turn_msg
                )
            else:
                chats[pid].add_user(turn_msg)
            chat = chats[pid]
            prompt_ids = chat.prompt_ids()
            if len(prompt_ids) > max_prompt_tokens:
                result.outcome = "context_limit"
                break

            sampled = sampler(prompt_ids)
            if sampled is None:
                result.outcome = "context_limit"
                break

            _append_turn(trace, prompt_ids, sampled)
            if sampled.truncated:
                trace.n_truncated += 1

            content, actions = parse_response(
                sampled.text, enable_think, action_sep, special_tokens
            )
            chat.commit_response(sampled.response_ids)
            turn_count += 1
            result.n_turns = turn_count

            action_id = (
                action_to_id(actions[0], legal) if actions else None
            )
            if action_id is None:
                # Format failure or an illegal/unparseable action: penalise this
                # turn and end the hand. The offender forfeits the pot.
                trace.n_invalid += 1
                trace.turn_scores.append(-format_penalty)
                result.outcome = "invalid_action"
                result.returns = {pid: -1.0, 1 - pid: 1.0}
                break

            trace.turn_scores.append(0.0)
            # NOTE: env.step() returns execute_results ONLY -- a list of per-move
            # dicts -- not (obs, results). reset() *does* return a 2-tuple, so
            # the two are not symmetric.
            execute_results = env.step(action_id)
            done = env.state.is_terminal()

            if done:
                returns = env.state.returns()
                result.returns = {0: float(returns[0]), 1: float(returns[1])}
                break

            if turn_count >= max_turns:
                result.outcome = "turn_limit"
                result.returns = {0: 0.0, 1: 0.0}
                break

            legal = env.get_all_actions()
            nxt = env.current_player
            pending_obs[nxt] = _observation_after(env, execute_results)

        if not result.returns:
            result.returns = {0: 0.0, 1: 0.0}

        # Fold each player's game return into their final turn's score. ROLL's
        # env emits per-step rewards that sum to the game return; collapsing
        # them onto the last turn is equivalent for Kuhn, where every
        # intermediate step reward is zero.
        for pid, trace in traces.items():
            if trace.turn_scores:
                trace.turn_scores[-1] += result.returns.get(pid, 0.0)

    except Exception as e:  # one bad hand must not kill the batch
        result.outcome = "error"
        result.error = f"{type(e).__name__}: {e}"
        if not result.returns:
            result.returns = {0: 0.0, 1: 0.0}
    return result


def _turn_user_message(observation: str, legal_actions: dict[int, str]) -> str:
    actions = ", ".join(f"`{t}`" for t in legal_actions.values())
    return (
        f"CURRENT GAME STATE:\n{observation}\n\n"
        f"LEGAL ACTIONS: {actions}\n\n"
        "Choose one legal action."
    )


def _observation_after(env: Any, execute_results: list[dict]) -> str:
    """Text of what the next player sees, from the last move applied.

    Each entry of execute_results already carries the rendered observation
    after that move, so the last entry is the current state. Falls back to
    env.render() only if the env ever stops populating it.
    """
    if execute_results:
        last = execute_results[-1]
        if isinstance(last, dict) and last.get("observation"):
            obs = last["observation"]
            return obs if isinstance(obs, str) else str(obs)
    return env.render()


def _append_turn(trace: PlayerTrace, prompt_ids: list[int], sampled: Sampled) -> None:
    """Extend the player's single growing sequence with (new obs tokens, response).

    `delta_ob_len` is the number of prompt tokens that are new since the last
    assistant turn -- the same quantity tinker-cookbook computes when merging
    consecutive turns into one Datum.
    """
    n = len(trace.tokens)
    if prompt_ids[:n] != trace.tokens:
        # Re-tokenising changed earlier tokens. Keep the longest common prefix
        # and re-anchor; the alternative is advantages landing on the wrong
        # positions, which is silent.
        common = 0
        for a, b in zip(trace.tokens, prompt_ids):
            if a != b:
                break
            common += 1
        trace.prefix_breaks += 1
        del trace.tokens[common:]
        del trace.logprobs[common:]
        trace.spans[:] = [(s, e) for s, e in trace.spans if e <= common]
        n = common

    delta_ob = prompt_ids[n:]
    trace.tokens.extend(delta_ob)
    trace.logprobs.extend([0.0] * len(delta_ob))

    start = len(trace.tokens)
    trace.tokens.extend(sampled.response_ids)
    trace.logprobs.extend(sampled.response_logprobs)
    trace.spans.append((start, len(trace.tokens)))


def play_episodes_concurrently(
    seeds: list[int],
    sampler_factory: Callable[[], TurnSampler],
    tokenizer: Any,
    *,
    max_workers: int,
    **kwargs: Any,
) -> list[EpisodeResult]:
    """Play episodes in parallel; results come back in `seeds` order.

    Order matters for reproducibility: the per-player normalisation below is
    computed over the whole batch, so a nondeterministic batch order would make
    a seeded run irreproducible.
    """
    if not seeds:
        return []
    workers = max(1, min(max_workers, len(seeds)))

    def _run(seed: int) -> EpisodeResult:
        return play_episode(seed, sampler_factory(), tokenizer, **kwargs)

    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(_run, seeds))


def play_episode_vs_opponent(
    seed: int,
    sampler: TurnSampler,
    tokenizer: Any,
    *,
    model_player: int,
    opponent: str,
    max_turns: int,
    enable_think: bool,
    action_sep: str,
    special_tokens: list[str],
    format_penalty: float,
    max_prompt_tokens: int,
) -> EpisodeResult:
    """Eval episode: the model takes one seat, MARSHAL's built-in bot the other.

    This is the val configuration from the MARSHAL yaml (KuhnPoker-first /
    KuhnPoker-second with `built_in_opponent: cfr`). The env drives the opponent
    itself inside reset()/step(), so this loop only ever samples for
    `model_player`.

    CFR is near-Nash, so ~50% win rate / ~0 mean return is the *ceiling* for a
    Kuhn player, not a floor. Read movement toward it as improvement -- the
    opposite of how you read the SPIRAL arm's win rate against `random`.
    """
    result = EpisodeResult(traces={}, returns={})
    env = make_env(
        seed=seed, built_in_opponent=opponent, opponent_player=1 - model_player
    )
    try:
        obs, _execute = env.reset(seed=seed)
        prefix = env.get_prompt(think=enable_think, player_id=model_player)
        chat = None
        trace = PlayerTrace(player_id=model_player)
        result.traces = {model_player: trace}

        observation = obs["observation"]
        legal = obs["legal_actions"]
        turn_count = 0

        while not env.state.is_terminal():
            if env.current_player != model_player:
                # Should not happen -- the env auto-plays the built-in opponent
                # inside reset()/step() -- but bail rather than sample for the
                # opponent's seat if the env ever changes that contract.
                break

            turn_msg = _turn_user_message(observation, legal)
            if chat is None:
                chat = ChatBuilder(
                    tokenizer, prefix["system"], prefix["user"] + turn_msg
                )
            else:
                chat.add_user(turn_msg)
            prompt_ids = chat.prompt_ids()
            if len(prompt_ids) > max_prompt_tokens:
                result.outcome = "context_limit"
                break

            sampled = sampler(prompt_ids)
            if sampled is None:
                result.outcome = "context_limit"
                break

            _append_turn(trace, prompt_ids, sampled)
            if sampled.truncated:
                trace.n_truncated += 1
            _content, actions = parse_response(
                sampled.text, enable_think, action_sep, special_tokens
            )
            chat.commit_response(sampled.response_ids)
            turn_count += 1
            result.n_turns = turn_count

            action_id = action_to_id(actions[0], legal) if actions else None
            if action_id is None:
                trace.n_invalid += 1
                trace.turn_scores.append(-format_penalty)
                result.outcome = "invalid_action"
                result.returns = {model_player: -1.0, 1 - model_player: 1.0}
                break

            trace.turn_scores.append(0.0)
            execute_results = env.step(action_id)
            if env.state.is_terminal():
                break
            if turn_count >= max_turns:
                result.outcome = "turn_limit"
                result.returns = {0: 0.0, 1: 0.0}
                break
            legal = env.get_all_actions()
            observation = _observation_after(env, execute_results)

        if not result.returns:
            rets = env.state.returns()
            result.returns = {0: float(rets[0]), 1: float(rets[1])}
        if trace.turn_scores:
            trace.turn_scores[-1] += result.returns.get(model_player, 0.0)
    except Exception as e:
        result.outcome = "error"
        result.error = f"{type(e).__name__}: {e}"
        if not result.returns:
            result.returns = {0: 0.0, 1: 0.0}
    return result
