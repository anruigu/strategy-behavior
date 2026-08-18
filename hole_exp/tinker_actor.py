"""Tinker sampling wrapper. Ported from `power_exp/tinker_actor.py`.

Two deliberate differences from that copy, both about this package's interface:
`act` takes the suite's `meta` dict instead of an `in_decision` flag, and
`StubActor` exists so the whole training loop can be exercised offline.

Renders chat messages to tokens with the model's own chat template and samples.
Returns the sampled token ids alongside the text because the RL trainer needs
them (we train on exactly the tokens that were sampled).

CoT handling is held FIXED across every condition (thinking disabled) -- the
plan lists varying CoT presence by condition as a confound.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import tinker


class Renderer:
    """Chat-template renderer backed by the model's tokenizer."""

    def __init__(self, tokenizer, enable_thinking: bool = False):
        self.tok = tokenizer
        self.enable_thinking = enable_thinking

    def build(self, messages: List[Dict[str, str]]) -> tinker.ModelInput:
        kw = dict(tokenize=True, add_generation_prompt=True)
        try:
            ids = self.tok.apply_chat_template(
                messages, enable_thinking=self.enable_thinking, **kw)
        except TypeError:
            # tokenizer/template without an enable_thinking kwarg
            ids = self.tok.apply_chat_template(messages, **kw)
        # transformers may return a BatchEncoding/dict rather than a flat list
        if hasattr(ids, "input_ids"):
            ids = ids.input_ids
        elif isinstance(ids, dict):
            ids = ids["input_ids"]
        if hasattr(ids, "tolist"):
            ids = ids.tolist()
        if ids and isinstance(ids[0], list):
            ids = ids[0]
        return tinker.ModelInput.from_ints([int(i) for i in ids])

    def stop_tokens(self) -> List[int]:
        out = []
        for name in ("<|im_end|>", "<|endoftext|>"):
            try:
                t = self.tok.convert_tokens_to_ids(name)
                if isinstance(t, int) and t >= 0:
                    out.append(t)
            except Exception:
                pass
        eos = getattr(self.tok, "eos_token_id", None)
        if isinstance(eos, int):
            out.append(eos)
        return sorted(set(out))


class TinkerActor:
    """Samples one assistant turn at a time from a Tinker sampling client."""

    def __init__(self, sampling_client, renderer: Renderer,
                 temperature: float = 1.0, max_tokens: int = 384,
                 seed: Optional[int] = None):
        self.sc = sampling_client
        self.r = renderer
        self.params = tinker.SamplingParams(
            max_tokens=max_tokens, temperature=temperature,
            stop=renderer.stop_tokens() or None, seed=seed)
        self.last: List[Dict] = []

    def _sample_one(self, messages, num_samples=1):
        mi = self.r.build(messages)
        resp = self.sc.sample(prompt=mi, num_samples=num_samples,
                              sampling_params=self.params)
        if hasattr(resp, "result"):  # APIFuture
            resp = resp.result()
        return mi, resp

    def act(self, messages: List[Dict[str, str]], meta: Optional[Dict] = None) -> str:
        """One assistant turn.

        `meta` is the suite's per-turn context dict (round, pool, private values,
        ...). The actor ignores it -- it is there for scripted policies, which
        share this signature so that a reference episode and a sampled episode
        are the same code path with a different callable.
        """
        mi, resp = self._sample_one(messages)
        seq = resp.sequences[0]
        text = self.r.tok.decode(seq.tokens, skip_special_tokens=True).strip()
        self.last.append({"prompt": mi, "tokens": list(seq.tokens),
                          "logprobs": list(getattr(seq, "logprobs", []) or [])})
        return text

    def reset_trace(self):
        self.last = []


class StubActor:
    """A no-API actor for `--dry-run`: mixes the two scripted references.

    Plays real episodes and produces real records, so a dry run exercises the
    environment, the action parsing, the reference machinery, the advantage
    computation and the metric plumbing -- everything except the tokens. The
    mix is deliberate: a stub that always played one reference would give every
    group a zero-variance return and the trainer would report "no data" for
    reasons that have nothing to do with the model.
    """

    def __init__(self, spec, seed: int = 0, p_exploit: float = 0.5):
        import random as _random

        self.honest = spec.scripted("honest")
        self.exploit = spec.scripted("exploit")
        self.rng = _random.Random(seed)
        self.p_exploit = p_exploit
        self.last: List[Dict] = []

    def act(self, messages: List[Dict[str, str]], meta: Optional[Dict] = None) -> str:
        text = (self.exploit if self.rng.random() < self.p_exploit
                else self.honest)(messages, meta or {})
        # Token ids the trainer can shape a Datum from without a tokenizer.
        ids = [1 + (ord(ch) % 97) for ch in text[:32]] or [1]
        self.last.append({"prompt": _StubInput(list(range(len(messages) + 2))),
                          "tokens": ids, "logprobs": [-0.5] * len(ids)})
        return text

    def reset_trace(self):
        self.last = []


class _StubInput:
    def __init__(self, ints):
        self._ints = ints

    def to_ints(self):
        return list(self._ints)


def build(service_client, model_name: str, temperature: float = 1.0,
          max_tokens: int = 384, seed: Optional[int] = None
          ) -> Tuple[TinkerActor, Renderer]:
    """`model_name` is either a base model id or a `tinker://` checkpoint path.

    Trained checkpoints from train_ipd.py's save_weights_for_sampler come back as
    `tinker://<id>:train:0/sampler_weights/<label>-stepNNNN`, and those load with
    model_path=, not base_model=. Dispatch on the scheme so the same eval harness
    scores the baselines and the RL arms without a second code path.
    """
    if str(model_name).startswith("tinker://"):
        sc = service_client.create_sampling_client(model_path=model_name)
    else:
        sc = service_client.create_sampling_client(base_model=model_name)
    rend = Renderer(sc.get_tokenizer())
    return TinkerActor(sc, rend, temperature, max_tokens, seed), rend
