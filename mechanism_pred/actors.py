"""Endpoint resolution + a flat-context chat actor for the frontier roster.

Endpoint routing is NOT re-derived here. `hole_exp/run_referee_crossplay.py`
already carries the two facts that are properties of this account rather than
of any one wave -- OpenRouter's moderation layer answers `anthropic/claude-opus-5`
with `finish_reason='content_filter'` and empty content, and `claude-opus-5`
rejects `temperature` outright -- so `endpoint_for` is imported from there and
the roster stays in one place. A preflight call per model runs before any wave
commits money, for the same reason it does there: an empty reply is scored as a
failed turn, so a dead endpoint reads as a model that will not negotiate.

`gemini-3.1-pro-preview` DOES answer through OpenRouter on this key today
(probed 2026-09-01), unlike the flash tier the referee roster had to route
direct -- so it is left on the shared route.

Flat context, like `run_referee_crossplay.Actor`: every turn is one
`(system, user)` pair carrying the whole visible history. A negotiation seat's
view is append-only, so a growing message list would say the same thing at
quadratic cost, and a retry cannot half-apply a turn.
"""
from __future__ import annotations

import pathlib
import random
import sys
import threading
import time
from typing import Dict, List, Optional, Tuple

_HOLE = pathlib.Path("/home/allie/strategy-behavior/hole_exp")
if str(_HOLE) not in sys.path:
    sys.path.insert(0, str(_HOLE))
import run_referee_crossplay as RC  # noqa: E402

MODELS = {"claude": RC.MODELS["claude"], "gpt": RC.MODELS["gpt"],
          "gemini": RC.MODELS["gemini"]}


def reasoning_body(base_url: str, effort: str) -> Dict:
    """`reasoning: <effort>` in the form THIS endpoint accepts (see RC)."""
    if "generativelanguage.googleapis.com" in base_url:
        return {"reasoning_effort": effort}
    return {"reasoning": {"effort": effort}}


class Actor:
    """One chat completion per call, retrying with a doubling token cap.

    A TRUNCATED reply is retried, not accepted. This is the expensive choice and
    it is the right one: every caller here needs the WHOLE reply. A cut-off
    negotiation turn loses the bracketed action tokens that usually sit at the
    end of it, so the seat silently does nothing that turn; a cut-off judge
    reply is invalid JSON and the whole episode goes unannotated. Both failures
    are invisible downstream -- they read as a passive player and a missing
    label, not as a budget artefact. The 1400-token pilot truncated 13 of 33
    calls and lost one of two judge annotations exactly this way.

    The doubling is not politeness either. `reasoning.effort` bills thinking
    against the same `max_tokens`, and api.anthropic.com's OpenAI-compatible
    surface reports `reasoning_tokens: 0` while spending them, so the budget
    vanishes with nothing in the usage record to show where it went. Retrying at
    the same ceiling just buys the same truncated reply again.
    """

    def __init__(self, model_key: str, temperature: Optional[float] = 0.7,
                 max_tokens: int = 4000, retries: int = 4,
                 effort: str = "medium"):
        from openai import OpenAI

        r = RC.endpoint_for(model_key)
        self.model_key = model_key
        self.model = r.model_id
        self.client = OpenAI(base_url=r.base_url, api_key=r.api_key, timeout=300.0)
        self.temperature = temperature if r.temperature else None
        self.max_tokens = max_tokens
        self.retries = retries
        self.reasoning = reasoning_body(r.base_url, effort)
        self.usage = {"calls": 0, "prompt_tokens": 0, "completion_tokens": 0,
                      "reasoning_tokens": 0, "errors": 0, "empty": 0,
                      "truncated": 0, "widened": 0, "filtered": 0,
                      "truncated_final": 0}
        self.lock = threading.Lock()

    def act(self, system: str, prompt: str) -> Tuple[str, Dict]:
        msgs = [{"role": "system", "content": system},
                {"role": "user", "content": prompt}]
        last, meta = "", {}
        for attempt in range(self.retries):
            try:
                cap = self.max_tokens * (2 ** attempt)
                r = self.client.chat.completions.create(
                    model=self.model, messages=msgs, max_tokens=cap,
                    extra_body=self.reasoning,
                    **({} if self.temperature is None
                       else {"temperature": self.temperature}))
                msg = r.choices[0].message if r.choices else None
                txt = (msg.content or "") if msg else ""
                fin = r.choices[0].finish_reason if r.choices else None
                meta = RC._reasoning_of(msg)
                meta["finish_reason"] = fin
                u = getattr(r, "usage", None)
                with self.lock:
                    self.usage["calls"] += 1
                    if u:
                        self.usage["prompt_tokens"] += u.prompt_tokens or 0
                        self.usage["completion_tokens"] += u.completion_tokens or 0
                        d = getattr(u, "completion_tokens_details", None)
                        rt = getattr(d, "reasoning_tokens", 0) or 0
                        self.usage["reasoning_tokens"] += rt
                        meta["reasoning_tokens"] = rt
                    if not txt.strip():
                        self.usage["empty"] += 1
                    if fin == "length":
                        self.usage["truncated"] += 1
                    if fin == "content_filter":
                        self.usage["filtered"] += 1
                    if attempt:
                        self.usage["widened"] += 1
                if txt.strip() and fin != "length":
                    return txt, meta
                # Keep the longest partial seen, so an exhausted retry returns
                # the best available text rather than the last (possibly
                # shortest) one.
                if len(txt) > len(last):
                    last = txt
                if fin == "content_filter":
                    break
            except Exception as e:  # noqa: BLE001
                with self.lock:
                    self.usage["errors"] += 1
                meta = {"error": f"{type(e).__name__}: {str(e)[:300]}"}
                if attempt == self.retries - 1:
                    break
                time.sleep(1.5 * (2 ** attempt) + random.random())
        if last.strip():
            with self.lock:
                self.usage["truncated_final"] += 1
        return last, meta


def preflight(actors: Dict[str, Actor]) -> Dict[str, str]:
    """One real call per model before a wave commits money."""
    bad = {}
    for k, a in sorted(actors.items()):
        txt, _ = a.act("You are terse.", "Reply with exactly: PONG")
        if not txt.strip():
            bad[k] = "content_filter" if a.usage["filtered"] else "empty or transport error"
    return bad
