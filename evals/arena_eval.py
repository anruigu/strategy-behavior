"""One eval harness, both self-play protocols, any checkpoint.

The two questions we need answered cannot be answered by the training scripts'
own evals, because each arm evaluates its own checkpoint under its own protocol
against its own opponent:

    SPIRAL  -> TextArena KuhnPoker-v1, 5 rounds, vs `random`
    MARSHAL -> OpenSpiel kuhn_poker,   1 hand,   vs `cfr`

So "SPIRAL scored 37.5% and MARSHAL scored -0.23" compares nothing. What is
needed is the same protocol applied across checkpoints:

  Q1  Does the Tinker port reproduce local?   -> fix the protocol, vary the
      *implementation* (oat/ROLL vs Tinker) at a matched training step.
  Q2  Is SPIRAL or MARSHAL better?            -> fix the protocol, vary the
      *algorithm*, with model / rank / rows-per-step already matched.

This script is the fixed-protocol side of both. It serves neither model nor
opinion: it points at an OpenAI-compatible vLLM endpoint, plays whichever
protocols you ask for, and writes counts plus Wilson intervals so the reader can
see when two numbers are not actually different.

Both game loops are imported from the training arms rather than rewritten -- the
whole point is that the policy is judged by the *same* code that trained it, so
a scoring bug cannot flatter one arm over the other. Only the sampler is
swapped: vLLM instead of Tinker.

Usage:
    python arena_eval.py --base-url http://localhost:8000/v1 \
        --model spiral-tinker-64 --protocols spiral,marshal --games 200 \
        --out results/arena/spiral-tinker-64.json
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import statistics
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests

REPO = Path(__file__).resolve().parent.parent
SPIRAL_ARM = REPO / "training" / "tinker"
MARSHAL_ARM = REPO / "training" / "marshal" / "tinker"


def _load_arm(name: str, path: Path):
    """Import an arm's selfplay.py under an explicit module name.

    Both arms name the file `selfplay.py`, so a plain `sys.path` + `import
    selfplay` binds whichever one is imported first and silently serves it to
    the other protocol -- which surfaces as `cannot import name
    play_episode_vs_opponent`, or worse, does not surface at all. Load by path
    under distinct names instead. Neither module imports its siblings, so this
    is safe.
    """
    import importlib.util  # noqa: PLC0415

    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# --- statistics -------------------------------------------------------------


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """95% Wilson interval for a binomial proportion.

    Wilson rather than normal-approximation because these evals routinely land
    at 0 or 1 invalid actions out of a few hundred turns, where the normal
    interval is degenerate (width zero) and would read as certainty.
    """
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, centre - half), min(1.0, centre + half))


def mean_ci(xs: list[float], z: float = 1.96) -> tuple[float, float, float]:
    """(mean, lo, hi) via the normal interval on the standard error."""
    if not xs:
        return (0.0, 0.0, 0.0)
    m = statistics.fmean(xs)
    if len(xs) < 2:
        return (m, m, m)
    se = statistics.stdev(xs) / math.sqrt(len(xs))
    return (m, m - z * se, m + z * se)


# --- the sampler ------------------------------------------------------------


@dataclass
class _Sampled:
    """Structurally compatible with both arms' `Sampled`.

    The two arms declare their own dataclasses with different field sets
    (SPIRAL carries `prompt_ids`, MARSHAL does not). Neither loop does an
    isinstance check, so one class carrying the union of the fields satisfies
    both.
    """

    prompt_ids: list[int]
    response_ids: list[int]
    response_logprobs: list[float]
    text: str
    truncated: bool


class VLLMSampler:
    """One call == one model turn, against an OpenAI-compatible completions API.

    Accepts *either* a prompt string (SPIRAL's loop) or a list of token ids
    (MARSHAL's), because the two arms build prompts differently and we want to
    reuse both loops unmodified. vLLM's /v1/completions takes both forms.

    We use /v1/completions and not /v1/chat/completions deliberately. Both arms
    render their own ChatML -- SPIRAL through spiral's template, MARSHAL through
    an incremental ChatBuilder -- and letting the server apply a chat template on
    top would wrap an already-wrapped prompt. The eval has to see exactly the
    prompt the training loop saw or it is measuring a different policy.
    """

    def __init__(
        self,
        base_url: str,
        model: str,
        tokenizer: Any,
        *,
        max_tokens: int,
        temperature: float,
        top_p: float,
        max_prompt_tokens: int,
        timeout: float = 600.0,
    ) -> None:
        self._url = base_url.rstrip("/") + "/completions"
        self._model = model
        self._tok = tokenizer
        self._max_tokens = max_tokens
        self._temperature = temperature
        self._top_p = top_p
        self._max_prompt_tokens = max_prompt_tokens
        self._timeout = timeout
        im_end = tokenizer.encode("<|im_end|>", add_special_tokens=False)
        if not im_end:
            raise SystemExit("tokenizer has no <|im_end|>; both arms emit ChatML")
        self._stop_ids = [im_end[0]]
        self._session = requests.Session()
        self._lock = threading.Lock()
        self.over_budget = 0
        self.errors = 0

    def __call__(self, prompt: str | list[int]) -> _Sampled | None:
        if isinstance(prompt, str):
            prompt_ids = self._tok.encode(prompt, add_special_tokens=False)
        else:
            prompt_ids = list(prompt)
        if len(prompt_ids) > self._max_prompt_tokens:
            with self._lock:
                self.over_budget += 1
            return None

        payload = {
            "model": self._model,
            "prompt": prompt_ids,
            "max_tokens": self._max_tokens,
            "temperature": self._temperature,
            "top_p": self._top_p,
            "stop_token_ids": self._stop_ids,
            # vLLM strips the stop token by default; both arms were trained on
            # sequences that *include* it, and MARSHAL's ChatBuilder decides
            # whether to re-open the assistant turn by checking for it.
            "include_stop_str_in_output": True,
            "n": 1,
        }
        for attempt in range(4):
            try:
                r = self._session.post(self._url, json=payload, timeout=self._timeout)
                r.raise_for_status()
                break
            except Exception:  # noqa: BLE001 - transient server-side 5xx / timeouts
                if attempt == 3:
                    with self._lock:
                        self.errors += 1
                    return None
                time.sleep(2 * (attempt + 1))
        choice = r.json()["choices"][0]
        text = choice["text"]
        # vLLM's completions API returns text, not ids. Re-encoding is exact
        # enough for eval -- unlike training, nothing here depends on the ids
        # round-tripping bit-for-bit, only on the decoded conversation being
        # the one the model actually produced.
        response_ids = self._tok.encode(text, add_special_tokens=False)
        return _Sampled(
            prompt_ids=prompt_ids,
            response_ids=response_ids,
            response_logprobs=[0.0] * len(response_ids),
            text=text,
            truncated=choice.get("finish_reason") == "length",
        )


# --- protocol A: SPIRAL's TextArena KuhnPoker vs random ---------------------


def eval_spiral_protocol(
    sampler_factory,
    *,
    games: int,
    env_id: str,
    max_turns: int,
    template: str,
    no_think: bool,
    workers: int,
    seed: int,
) -> dict[str, Any]:
    """TextArena `KuhnPoker-v1`, 5 rounds, model vs a uniform-random opponent.

    Played from BOTH seats and reported separately as well as pooled. The
    training arm only ever evaluated seat 0, which in a game with a first-mover
    disadvantage is half a measurement.

    Read this the way SPIRAL intends: `random` is weak, so a high win rate means
    "the policy has learned the game at all". It does NOT mean the policy is
    near-optimal -- an equilibrium Kuhn policy declines to exploit and scores
    *lower* here than a crude exploiter.
    """
    sp = _load_arm("spiral_arm_selfplay", SPIRAL_ARM / "selfplay.py")

    # spiral is not pip-installed (installing it drags in oat/vllm/deepspeed);
    # the arm puts the checkout on sys.path at startup, and this harness has to
    # do the same before `spiral.*` resolves.
    sp.import_spiral(os.environ.get("SPIRAL_DIR", "/workspace/allie/spiral"))
    play_games_concurrently = sp.play_games_concurrently
    from spiral.agents.random import RandomAgent  # noqa: PLC0415

    rng = random.Random(seed)
    out: dict[str, Any] = {"protocol": "spiral", "env_id": env_id, "seats": {}}
    pooled_wins = pooled_n = pooled_inval = pooled_turns = 0
    pooled_clean_wins = pooled_clean_n = 0
    pooled_returns: list[float] = []
    pooled_clean_returns: list[float] = []

    for seat in (0, 1):
        specs = [(env_id, True, rng.randrange(2**31)) for _ in range(games)]
        results = play_games_concurrently(
            specs,
            sampler_factory,
            max_workers=workers,
            max_turns=max_turns,
            template=template,
            model_player_id=seat,
            opponent_factory=lambda eid: RandomAgent(eid),
            no_think=no_think,
        )
        n = len(results)
        wins = sum(
            1 for g in results if g.rewards.get(seat, 0) > g.rewards.get(1 - seat, 0)
        )
        draws = sum(
            1 for g in results if g.rewards.get(seat, 0) == g.rewards.get(1 - seat, 0)
        )
        rets = [float(g.rewards.get(seat, 0.0)) for g in results]
        turns = sum(len(g.turns[seat]) for g in results)
        inval = sum(1 for g in results for t in g.turns[seat] if not t.action_is_valid)
        # Clean games only: every model turn parsed. This separates "learned to
        # play Kuhn" from "learned to emit \boxed{}" -- an invalid action
        # forfeits, so a policy that only ever fixed its formatting posts a
        # higher win rate without its card play having changed at all. If
        # win_rate and win_rate_clean move together, it is strategy; if only
        # win_rate moves, it is format compliance.
        clean = [
            g for g in results if all(t.action_is_valid for t in g.turns[seat])
        ]
        clean_wins = sum(
            1 for g in clean if g.rewards.get(seat, 0) > g.rewards.get(1 - seat, 0)
        )
        clean_rets = [float(g.rewards.get(seat, 0.0)) for g in clean]
        clo, chi = wilson(clean_wins, len(clean))
        cm, cmlo, cmhi = mean_ci(clean_rets)
        lo, hi = wilson(wins, n)
        m, mlo, mhi = mean_ci(rets)
        out["seats"][seat] = {
            "n_games": n,
            "wins": wins,
            "draws": draws,
            "win_rate": wins / max(1, n),
            "win_rate_ci95": [lo, hi],
            "mean_return": m,
            "mean_return_ci95": [mlo, mhi],
            "n_clean": len(clean),
            "win_rate_clean": clean_wins / max(1, len(clean)),
            "win_rate_clean_ci95": [clo, chi],
            "mean_return_clean": cm,
            "mean_return_clean_ci95": [cmlo, cmhi],
            "model_turns": turns,
            "invalid_actions": inval,
            "invalid_rate": inval / max(1, turns),
            "mean_game_len": statistics.fmean(
                [float(sum(len(g.turns[p]) for p in (0, 1))) for g in results]
            )
            if results
            else 0.0,
        }
        pooled_wins += wins
        pooled_n += n
        pooled_inval += inval
        pooled_turns += turns
        pooled_returns += rets
        pooled_clean_wins += clean_wins
        pooled_clean_n += len(clean)
        pooled_clean_returns += clean_rets

    lo, hi = wilson(pooled_wins, pooled_n)
    m, mlo, mhi = mean_ci(pooled_returns)
    clo, chi = wilson(pooled_clean_wins, pooled_clean_n)
    cm, cmlo, cmhi = mean_ci(pooled_clean_returns)
    out["pooled"] = {
        "n_games": pooled_n,
        "win_rate": pooled_wins / max(1, pooled_n),
        "win_rate_ci95": [lo, hi],
        "mean_return": m,
        "mean_return_ci95": [mlo, mhi],
        "n_clean": pooled_clean_n,
        "win_rate_clean": pooled_clean_wins / max(1, pooled_clean_n),
        "win_rate_clean_ci95": [clo, chi],
        "mean_return_clean": cm,
        "mean_return_clean_ci95": [cmlo, cmhi],
        "invalid_rate": pooled_inval / max(1, pooled_turns),
    }
    return out


# --- protocol B: MARSHAL's OpenSpiel Kuhn vs CFR ----------------------------


def eval_marshal_protocol(
    sampler_factory,
    tokenizer,
    *,
    games: int,
    opponent: str,
    max_turns: int,
    enable_think: bool,
    action_sep: str,
    format_penalty: float,
    max_prompt_tokens: int,
    workers: int,
    seed: int,
) -> dict[str, Any]:
    """OpenSpiel `kuhn_poker`, one hand, model vs the built-in CFR bot.

    CFR is near-Nash, so this is the informative direction: ~50% win rate and a
    mean return near Kuhn's game value (-1/18 for the first mover, +1/18 for the
    second) is the CEILING. You cannot beat CFR at Kuhn; you can only fail to
    lose to it.

    Two returns are reported and the difference between them matters:
      mean_return        -- every hand, forfeits scored as the env scores them
      mean_return_valid  -- only hands where the model never blew the format
    MARSHAL's own eval reports the first, and early in training that number is
    dominated by truncation forfeits rather than by card play. The gap between
    the two is the size of that contamination.
    """
    ma = _load_arm("marshal_arm_selfplay", MARSHAL_ARM / "selfplay.py")
    ma.import_marshal(os.environ.get("MARSHAL_DIR", "/workspace/allie/MARSHAL"))
    play_episode_vs_opponent = ma.play_episode_vs_opponent

    rng = random.Random(seed)
    out: dict[str, Any] = {"protocol": "marshal", "opponent": opponent, "seats": {}}
    pooled_wins = pooled_n = pooled_inval = pooled_turns = 0
    pooled_returns: list[float] = []
    pooled_valid: list[float] = []

    for seat in (0, 1):
        seeds = [rng.randrange(2**31) for _ in range(games)]

        def one(s: int, seat: int = seat):
            return play_episode_vs_opponent(
                s,
                sampler_factory(),
                tokenizer,
                model_player=seat,
                opponent=opponent,
                max_turns=max_turns,
                enable_think=enable_think,
                action_sep=action_sep,
                special_tokens=[],
                format_penalty=format_penalty,
                max_prompt_tokens=max_prompt_tokens,
            )

        # MARSHAL's own run_eval loops serially. A Kuhn hand is 2-3 turns, so at
        # n=200 per seat that is ~500 blocking round-trips; a pool makes it
        # ~500/workers instead without touching the episode semantics.
        with ThreadPoolExecutor(max_workers=workers) as pool:
            results = list(pool.map(one, seeds))

        n = len(results)
        wins = sum(1 for r in results if r.returns.get(seat, 0.0) > 0)
        rets = [float(r.returns.get(seat, 0.0)) for r in results]
        valid = [
            float(r.returns.get(seat, 0.0)) for r in results if r.outcome == "normal"
        ]
        turns = sum(len(t.spans) for r in results for t in r.traces.values())
        inval = sum(t.n_invalid for r in results for t in r.traces.values())
        lo, hi = wilson(wins, n)
        m, mlo, mhi = mean_ci(rets)
        vm, vlo, vhi = mean_ci(valid)
        outcomes: dict[str, int] = {}
        for r in results:
            outcomes[r.outcome] = outcomes.get(r.outcome, 0) + 1
        out["seats"][seat] = {
            "n_episodes": n,
            "wins": wins,
            "win_rate": wins / max(1, n),
            "win_rate_ci95": [lo, hi],
            "mean_return": m,
            "mean_return_ci95": [mlo, mhi],
            "n_valid": len(valid),
            "mean_return_valid": vm,
            "mean_return_valid_ci95": [vlo, vhi],
            "model_turns": turns,
            "invalid_actions": inval,
            "invalid_rate": inval / max(1, turns),
            "outcomes": outcomes,
        }
        pooled_wins += wins
        pooled_n += n
        pooled_inval += inval
        pooled_turns += turns
        pooled_returns += rets
        pooled_valid += valid

    lo, hi = wilson(pooled_wins, pooled_n)
    m, mlo, mhi = mean_ci(pooled_returns)
    vm, vlo, vhi = mean_ci(pooled_valid)
    out["pooled"] = {
        "n_episodes": pooled_n,
        "win_rate": pooled_wins / max(1, pooled_n),
        "win_rate_ci95": [lo, hi],
        "mean_return": m,
        "mean_return_ci95": [mlo, mhi],
        "n_valid": len(pooled_valid),
        "mean_return_valid": vm,
        "mean_return_valid_ci95": [vlo, vhi],
        "invalid_rate": pooled_inval / max(1, pooled_turns),
    }
    return out


# --- driver -----------------------------------------------------------------


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--base-url", default="http://localhost:8000/v1")
    ap.add_argument("--model", required=True, help="served model / LoRA module name")
    ap.add_argument("--tokenizer", default="Qwen/Qwen3-8B")
    ap.add_argument("--label", default=None, help="name for this row in the report")
    ap.add_argument("--protocols", default="spiral,marshal")
    ap.add_argument("--games", type=int, default=200, help="per seat, per protocol")
    ap.add_argument("--workers", type=int, default=32)
    ap.add_argument("--seed", type=int, default=1234)
    ap.add_argument("--max-tokens", type=int, default=4096)
    ap.add_argument("--temperature", type=float, default=0.6)
    ap.add_argument("--top-p", type=float, default=0.95)
    ap.add_argument("--sequence-length", type=int, default=32768)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    from transformers import AutoTokenizer  # noqa: PLC0415

    tok = AutoTokenizer.from_pretrained(args.tokenizer, trust_remote_code=True)
    max_prompt = max(1, min(args.sequence_length, 32768) - args.max_tokens)

    def make_sampler(_env_id: str | None = None) -> VLLMSampler:
        return VLLMSampler(
            args.base_url,
            args.model,
            tok,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
            top_p=args.top_p,
            max_prompt_tokens=max_prompt,
        )

    label = args.label or args.model
    report: dict[str, Any] = {
        "label": label,
        "model": args.model,
        "tokenizer": args.tokenizer,
        "games_per_seat": args.games,
        "sampling": {
            "temperature": args.temperature,
            "top_p": args.top_p,
            "max_tokens": args.max_tokens,
        },
        "seed": args.seed,
        "results": {},
    }

    wanted = [p.strip() for p in args.protocols.split(",") if p.strip()]
    for proto in wanted:
        t0 = time.time()
        print(f"[{label}] protocol={proto} games={args.games}/seat ...", flush=True)
        if proto == "spiral":
            # `no_think=True`: Qwen3-8B opens a <think> block that does not close
            # inside the budget on this prompt, and every unclosed turn is scored
            # as an invalid action. This matches how the SPIRAL arm trained.
            res = eval_spiral_protocol(
                make_sampler,
                games=args.games,
                env_id="KuhnPoker-v1",
                max_turns=50,
                template="qwen3",
                no_think=True,
                workers=args.workers,
                seed=args.seed,
            )
        elif proto == "marshal":
            # `enable_think=True`: MARSHAL's prompt *requires* <think>...</think>
            # before <answer>, so suppressing thinking here would fail the format
            # check on every turn. The two protocols genuinely differ on this.
            res = eval_marshal_protocol(
                lambda: make_sampler(),
                tok,
                games=args.games,
                opponent="cfr",
                max_turns=50,
                enable_think=True,
                action_sep="||",
                format_penalty=0.05,
                max_prompt_tokens=max_prompt,
                workers=args.workers,
                seed=args.seed,
            )
        else:
            raise SystemExit(f"unknown protocol {proto!r}")
        res["wall_seconds"] = round(time.time() - t0, 1)
        report["results"][proto] = res
        p = res["pooled"]
        print(
            f"[{label}] {proto}: win {p['win_rate']:.1%} "
            f"[{p['win_rate_ci95'][0]:.1%}, {p['win_rate_ci95'][1]:.1%}]  "
            f"return {p['mean_return']:+.3f}  invalid {p['invalid_rate']:.1%}  "
            f"({res['wall_seconds']:.0f}s)",
            flush=True,
        )

    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(report, indent=2))
    print(f"[{label}] wrote {outp}")


if __name__ == "__main__":
    main()
