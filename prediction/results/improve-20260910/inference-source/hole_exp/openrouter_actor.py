"""OpenRouter sampling wrapper -- the frontier comparison arm.

`tinker_actor.TinkerActor` is the suite's normal actor and the only one training
uses; this exists so a screen can put a frontier model beside the Tinker base
models on the SAME environment, which is the only way to read a floor as "this
size of model does not find the corner" rather than "nothing finds the corner".

Interface-compatible with `TinkerActor` on the one method the environments call:

    act(messages, meta) -> str

and it keeps a `.last` trace list so calling code that reaches for tokens does
not crash. The entries carry no token ids -- OpenRouter returns text, not the
sampled ids -- so this actor CANNOT be used for training, only for measurement.
`build()` refuses a model that does not look like an OpenRouter id for exactly
that reason: a typo that silently fell back to a trainable path would put an
untrainable actor in a training loop.

**Reasoning is disabled by default, and that is load-bearing.** `tinker_actor`
holds CoT fixed with `enable_thinking=False` in every condition because varying
it is a confound. OpenRouter runs Anthropic extended thinking by DEFAULT, and it
bills those tokens against `max_tokens`: at the suite's 384 that silently ate the
reply on longer contexts, returning truncated or empty content with 0 API errors
and a 10-19% `invalid_rate` on the merchant screen -- a format artefact that
reads exactly like a model declining to act. `{"reasoning": {"enabled": False}}`
takes `reasoning_tokens` to 0 and matches the Tinker arms. `--reasoning` turns it
back on for a deliberate comparison; raise `max_tokens` with it if you do.

Two deliberate differences from the Tinker path, both unavoidable and both
recorded so a comparison is read with them in mind:

  - **No shared chat template.** Tinker renders with the model's own tokenizer;
    here the provider does it server-side. The messages are identical, the
    tokenisation is theirs.
  - **No logprobs, no seed.** Temperature is honoured; determinism is not
    available, so a frontier cell's numbers are a sample mean and nothing more.
"""
from __future__ import annotations

import os
import random
import time
from typing import Dict, List, Optional, Tuple

import core

# Frontier ids are namespaced by vendor on OpenRouter (`anthropic/...`,
# `openai/...`); Tinker base ids are not namespaced that way except for `Qwen/`
# and `openai/gpt-oss-*`, which are the two collisions worth excluding by hand.
_TINKER_LOOKALIKE = ("qwen/", "meta-llama/", "openai/gpt-oss", "moonshotai/",
                     "deepseek-ai/", "nvidia/", "thinkingmachines/")


def is_openrouter_model(model: str) -> bool:
    m = str(model).lower()
    if m.startswith("tinker://") or "/" not in m:
        return False
    return not m.startswith(_TINKER_LOOKALIKE)


class OpenRouterActor:
    """Samples one assistant turn at a time from OpenRouter chat-completions."""

    def __init__(self, model: str, temperature: float = 1.0,
                 max_tokens: int = 384, retries: int = 5,
                 seed: Optional[int] = None, reasoning: bool = False):
        from openai import OpenAI

        core.load_env_file()
        key = os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise SystemExit("OPENROUTER_API_KEY is not set (looked in "
                             "the environment and /workspace/allie/.env)")
        self.client = OpenAI(base_url="https://openrouter.ai/api/v1",
                             api_key=key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.retries = retries
        self.reasoning = reasoning
        self.rng = random.Random(seed)
        self.last: List[Dict] = []
        # `truncated` and `reasoning_tokens` are here so a floor can be told
        # apart from a budget artefact without re-running: a cell with a nonzero
        # invalid_rate AND a nonzero truncated count is a format problem, not a
        # disposition.
        self.usage = {"calls": 0, "prompt_tokens": 0, "completion_tokens": 0,
                      "reasoning_tokens": 0, "errors": 0, "truncated": 0,
                      "empty": 0, "blocked": 0}
        self.blocked_providers: Dict[str, int] = {}

    def act(self, messages: List[Dict[str, str]], meta: Optional[Dict] = None) -> str:
        """One assistant turn. `meta` is ignored, as in `TinkerActor.act`.

        A turn that will not come back after `retries` returns "" rather than
        raising: the environments score an unparseable turn as the honest branch
        and count it `invalid`, so a dropped call shows up in `invalid_rate`
        where a reader can see it, instead of killing the episode and biasing
        the cell toward whatever seeds happened to succeed.
        """
        delay = 2.0
        extra = ({} if self.reasoning
                 else {"extra_body": {"reasoning": {"enabled": False}}})
        for attempt in range(self.retries):
            try:
                r = self.client.chat.completions.create(
                    model=self.model, messages=messages,
                    temperature=self.temperature, max_tokens=self.max_tokens,
                    **extra)
                choice = r.choices[0]
                text = (choice.message.content or "").strip()
                u = getattr(r, "usage", None)
                self.usage["calls"] += 1
                fin = getattr(choice, "finish_reason", None)
                if fin == "length":
                    self.usage["truncated"] += 1
                # A PROVIDER GUARDRAIL, not the model. OpenRouter fans a model
                # out across hosts (Bedrock / Google / Azure / first-party) and
                # some apply their own content filter, which comes back as
                # finish_reason='content_filter' with empty content and no API
                # error. On merchant that fires from a few rounds in, once the
                # transcript has accumulated business-corner talk, and it is not
                # specific to the exploit branch -- the honest scripted policy
                # trips it too. Counted separately because it is a COVERAGE loss
                # (fewer decisions observed), not a decision: the environment
                # excludes an unparseable turn from the exploit-rate denominator,
                # so the rate stays honest while `capture` and `payoff` do not.
                if fin == "content_filter":
                    self.usage["blocked"] += 1
                    self.blocked_providers[str(
                        getattr(r, "provider", None) or "?")] = (
                        self.blocked_providers.get(str(
                            getattr(r, "provider", None) or "?"), 0) + 1)
                if not text:
                    self.usage["empty"] += 1
                if u is not None:
                    self.usage["prompt_tokens"] += int(getattr(u, "prompt_tokens", 0) or 0)
                    self.usage["completion_tokens"] += int(
                        getattr(u, "completion_tokens", 0) or 0)
                    det = getattr(u, "completion_tokens_details", None)
                    self.usage["reasoning_tokens"] += int(
                        getattr(det, "reasoning_tokens", 0) or 0)
                self.last.append({"prompt": None, "tokens": [], "logprobs": [],
                                  "text": text})
                return text
            except Exception:  # noqa: BLE001 -- rate limits, 5xx, transport
                self.usage["errors"] += 1
                if attempt == self.retries - 1:
                    self.last.append({"prompt": None, "tokens": [],
                                      "logprobs": [], "text": ""})
                    return ""
                time.sleep(delay * (1.0 + self.rng.random()))
                delay = min(delay * 2, 30.0)
        return ""

    def reset_trace(self):
        self.last = []


def build(model: str, temperature: float = 1.0, max_tokens: int = 384,
          seed: Optional[int] = None,
          reasoning: bool = False) -> Tuple[OpenRouterActor, None]:
    """Mirrors `tinker_actor.build`'s (actor, renderer) shape; no renderer here."""
    if not is_openrouter_model(model):
        raise SystemExit(
            f"{model!r} does not look like an OpenRouter model id. This actor "
            "is measurement-only (no token ids, so it cannot train); route "
            "Tinker base models and tinker:// checkpoints through "
            "tinker_actor.build instead.")
    return OpenRouterActor(model, temperature=temperature,
                           max_tokens=max_tokens, seed=seed,
                           reasoning=reasoning), None
