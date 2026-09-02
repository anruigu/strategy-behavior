#!/usr/bin/env python
"""An Anthropic-API actor with the same shape as `run_referee_crossplay.Actor`.

    from anthropic_actor import AnthropicActor, load_anthropic_key
    actor = AnthropicActor(model="claude-opus-5", max_tokens=1200)
    reply = actor.act(system_prompt, game_prompt)

WHY A SEPARATE MODULE. `run_referee_crossplay.Actor` talks to OpenRouter through
the OpenAI SDK, and every number on disk -- the SPARTAN baseline, the wave
curves, `opponent_sim_data/`, `onset_data/` -- came through it. Converting that
class in place would make the existing tags unreproducible, so the OpenRouter
path stays exactly as it is and this is a drop-in alternative next to it. The
two expose the same surface (`.act(system, prompt) -> str` and a `.usage` dict),
so a caller swaps provider without any other change.

WHAT SWITCHING PROVIDER COSTS. `qwen3.8-27b` is the training target: it is the
model the MARSHAL runs train, the model the SPARTAN baseline measures, and the
reference every later checkpoint is read against. A Claude number is not
comparable to any of those -- it answers a different question ("can a stronger
model find this hole") and must not be pooled into a qwen tag or curve.

THE KEY IS NOT IN `~/.bashrc`. That file holds only a marker comment,
`# migrated to ~/.research_env (mode 0600): ANTHROPIC_API_KEY`; the value lives
in `~/.research_env` alongside `OPENROUTER_API_KEY`. `load_anthropic_key`
therefore reads the environment first and that file second, which is the same
resolution order `run_referee_crossplay.load_key` uses for OpenRouter.
"""
from __future__ import annotations

import os
import pathlib
import re
import threading
from typing import Dict, Optional, Tuple

ENV_FILE = pathlib.Path.home() / ".research_env"

# Anthropic list price, USD per million tokens, for the models this is likely to
# be pointed at. Used only for the cost estimate a runner prints before
# sampling; `usage` below carries the real token counts.
PRICING: Dict[str, Tuple[float, float]] = {
    "claude-opus-5": (5.00, 25.00),
    "claude-sonnet-5": (2.00, 10.00),
    "claude-haiku-4-5": (1.00, 5.00),
}
DEFAULT_MODEL = "claude-opus-5"


def load_anthropic_key() -> str:
    """`ANTHROPIC_API_KEY` from the environment, else from `~/.research_env`."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return key
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            m = re.match(r'\s*(?:export\s+)?ANTHROPIC_API_KEY\s*=\s*"?([^"\s]+)',
                         line)
            if m:
                return m.group(1)
    raise SystemExit(
        "ANTHROPIC_API_KEY not set and not found in ~/.research_env. "
        "Note ~/.bashrc only carries a marker comment for it, not the value.")


class AnthropicActor:
    """One Anthropic message per decision. Stateless, like the OpenRouter Actor.

    Stateless matters and is not a detail: every prompt the engines build is
    self-contained, so a retry cannot half-apply a turn. It is ALSO the thing
    that makes these numbers differ from a MARSHAL training rollout, where
    `referee_env` accumulates a real multi-turn conversation per seat
    (`builders[pid].add_user(prompt)`). On `gen_sovereign_vaults` the stateless
    path measured 0.00-0.08 and the accumulating path 0.29 at step 0, so the
    two are not interchangeable readings of "the base rate".
    """

    def __init__(self, model: str = DEFAULT_MODEL, temperature: float = 1.0,
                 max_tokens: int = 1200, effort: str = "low",
                 thinking: bool = True, fallbacks: bool = True,
                 api_key: Optional[str] = None, retries: int = 4):
        import anthropic
        self.model, self.max_tokens = model, max_tokens
        # `temperature` is REMOVED on Opus 5 / Sonnet 5 / Fable 5 and returns a
        # 400 if sent, so it is accepted here for signature parity with the
        # OpenRouter Actor and deliberately never forwarded. Depth is
        # controlled by `effort` instead.
        self.temperature = temperature
        self.effort, self.thinking, self.want_fallbacks = effort, thinking, fallbacks
        # The SDK already retries 408/409/429/5xx with backoff; let it, rather
        # than wrapping a second loop around it.
        self.client = anthropic.Anthropic(
            api_key=api_key or load_anthropic_key(), max_retries=retries)
        self.usage = {"calls": 0, "prompt_tokens": 0, "completion_tokens": 0,
                      "reasoning_tokens": 0, "errors": 0, "empty": 0,
                      "truncated": 0, "widened": 0, "refusals": 0}
        self.lock = threading.Lock()

    def act(self, system: str, prompt: str) -> str:
        return self.act_full(system, prompt)[0]

    def act_full(self, system: str, prompt: str) -> Tuple[str, dict]:
        """(visible_text, meta). `meta` carries stop_reason and any thinking."""
        import anthropic

        kwargs = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "system": system,
            "messages": [{"role": "user", "content": prompt}],
            # `effort` lives inside output_config, not top level. `low` mirrors
            # the wave runs' `reasoning_effort: low`, which is the closest this
            # gets to the training configuration.
            "output_config": {"effort": self.effort},
        }
        if self.thinking:
            kwargs["thinking"] = {"type": "adaptive"}

        try:
            if self.want_fallbacks:
                # A game prompt is benign, but a policy decline would otherwise
                # return an empty reply that the engine scores as the HONEST
                # fallback move -- a refusal reading as "chose not to cheat".
                # Routing by category avoids maintaining a model list.
                msg = self.client.beta.messages.create(
                    betas=["server-side-fallback-2026-07-01"],
                    fallbacks="default", **kwargs)
            else:
                msg = self.client.messages.create(**kwargs)
        except anthropic.APIStatusError as e:
            with self.lock:
                self.usage["errors"] += 1
            raise RuntimeError(
                f"anthropic {e.status_code}: {getattr(e, 'message', e)}") from e
        except anthropic.APIConnectionError as e:
            with self.lock:
                self.usage["errors"] += 1
            raise RuntimeError(f"anthropic connection error: {e}") from e

        text, think = [], []
        for b in msg.content:
            if b.type == "text":
                text.append(b.text)
            elif b.type == "thinking":
                think.append(getattr(b, "thinking", "") or "")
        out = "".join(text).strip()

        with self.lock:
            self.usage["calls"] += 1
            u = msg.usage
            self.usage["prompt_tokens"] += int(getattr(u, "input_tokens", 0) or 0)
            self.usage["completion_tokens"] += int(getattr(u, "output_tokens", 0) or 0)
            if msg.stop_reason == "refusal":
                self.usage["refusals"] += 1
            if msg.stop_reason == "max_tokens":
                self.usage["truncated"] += 1
            if not out:
                self.usage["empty"] += 1

        meta = {"stop_reason": msg.stop_reason,
                "reasoning": "\n".join(think) or None,
                "model": getattr(msg, "model", self.model)}
        # `stop_details` is populated only on a refusal; guard before reading.
        if msg.stop_reason == "refusal" and getattr(msg, "stop_details", None):
            meta["refusal_category"] = getattr(msg.stop_details, "category", None)
        return out, meta


def estimate_usd(model: str, calls: int, in_tok: float = 1.5e3,
                 out_tok: float = 250) -> Optional[float]:
    """Rough list-price cost for `calls` decisions, or None for unknown models."""
    p = PRICING.get(model)
    if not p:
        return None
    pin, pout = p
    return calls * (in_tok * pin + out_tok * pout) / 1e6


if __name__ == "__main__":
    a = AnthropicActor(max_tokens=300)
    txt, meta = a.act_full(
        "You are playing a game. Reply only with the bracketed action.",
        "Reply with [declare: n], an integer from 1 to 10.")
    print("model:", meta["model"], "| stop:", meta["stop_reason"])
    print("reply:", repr(txt))
    print("usage:", a.usage)
