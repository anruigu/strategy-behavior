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

# The sampling profile that gives Qwen3.8-27B healthy traces on the agentic
# merchant. Found by `tune_sampling.py`; the numbers behind it, 16 episodes each:
#
#   t1.0 / 384 / no stop     invalid 0.927   <- unusable, replies cut mid-call
#   t1.0 / 512 / stop "]"    invalid 0.417
#   t0.7 / p0.9 / 512 / stop invalid 0.023   <- this
#
# Both knobs are load-bearing and neither is sufficient alone: the stop sequence
# removes truncation (the model cannot ramble past its own action), and the lower
# entropy stops it looping before it gets there. Qwen3.6-27B is fine either way,
# which is why this went unnoticed until 3.6 was slated for retirement.
TUNED_TOOL_SAMPLING = {"temperature": 0.7, "top_p": 0.9, "max_tokens": 512,
                       "close_bracket": True}


class Renderer:
    """Chat-template renderer backed by the model's tokenizer.

    `reasoning_effort` matters on the Qwen3.8 templates, which accept
    'low' | 'medium' | 'xhigh' and **default to xhigh** whenever thinking is on
    or simply left undefined. That default is not a small thing: on the agentic
    merchant it made Qwen3.8-27B reason at maximum effort every turn, run past
    the token budget, and get cut off mid tool call, for a 74-93% invalid rate
    where Qwen3.6-27B sat at 1.6%. Passing it explicitly is the difference
    between a usable base model and an unusable one, so it is a first-class
    argument rather than something the caller is expected to know to override.
    """

    def __init__(self, tokenizer, enable_thinking: bool = False,
                 reasoning_effort: Optional[str] = None):
        self.tok = tokenizer
        self.enable_thinking = enable_thinking
        self.reasoning_effort = reasoning_effort

    def build(self, messages: List[Dict[str, str]]) -> tinker.ModelInput:
        kw = dict(tokenize=True, add_generation_prompt=True)
        if self.reasoning_effort:
            kw["reasoning_effort"] = self.reasoning_effort
        try:
            ids = self.tok.apply_chat_template(
                messages, enable_thinking=self.enable_thinking, **kw)
        except TypeError:
            # tokenizer/template without an enable_thinking kwarg
            kw.pop("reasoning_effort", None)
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
    """Samples one assistant turn at a time from a Tinker sampling client.

    `close_bracket` halts generation at the `]` that ends a bracketed action and
    puts the stripped `]` back. On the agentic `merchant` this is the single
    biggest lever on trace health for Qwen3.8-27B: without it the model rambles
    past its own tool call and is cut off mid-argument (invalid 0.80-0.97);
    with it, truncation goes to zero. Combined with top_p 0.9 / temperature 0.7
    it takes that model from unusable to a 0.000 invalid rate.

    It is safe for the other environments too -- every action in this suite is a
    bracketed token and the suite scores the LAST one -- but it is off by default
    so no existing cell's numbers move without someone asking for it. Do NOT
    enable it together with thinking: a `]` inside a <think> block stops
    generation before the answer is ever emitted.
    """

    def __init__(self, sampling_client, renderer: Renderer,
                 temperature: float = 1.0, max_tokens: int = 384,
                 seed: Optional[int] = None, top_p: float = 1.0,
                 close_bracket: bool = False):
        self.sc = sampling_client
        self.r = renderer
        self.close_bracket = close_bracket
        if close_bracket and renderer.enable_thinking:
            raise ValueError(
                "close_bracket with thinking enabled: a ']' inside the <think> "
                "block halts generation before the action is written")
        self.params = tinker.SamplingParams(
            max_tokens=max_tokens, temperature=temperature, top_p=top_p,
            stop=(["]"] if close_bracket else (renderer.stop_tokens() or None)),
            seed=seed)
        self.last: List[Dict] = []

    # The model's context. A prompt that plus max_tokens exceeds it is a
    # non-retryable 400 from the sampler, and it took down a 64-step run:
    # `mixed_think_nohole_d1_s0` degenerated into unparseable output, its
    # episodes stopped terminating early, and the transcript reached 65,624
    # tokens against a 65,536 window. The run died rather than the episode.
    CONTEXT = 65536

    def _sample_one(self, messages, num_samples=1):
        mi = self.r.build(messages)
        # Trim the request rather than let the sampler refuse it. A turn that
        # cannot fit is a turn the policy loses -- it comes back empty, the env
        # scores it invalid (i.e. the honest branch, and now charged for by
        # core.INVALID_COST), and the episode carries on. Killing the job
        # instead throws away every step since the last checkpoint, which is
        # the wrong trade for one over-long transcript.
        budget = self.CONTEXT - len(mi.to_ints()) - 8
        if budget <= 0:
            return mi, None
        params = self.params
        if params.max_tokens > budget:
            params = params.model_copy(update={"max_tokens": budget})
        resp = self.sc.sample(prompt=mi, num_samples=num_samples,
                              sampling_params=params)
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
        if resp is None:
            # No room left in the context for even one token. Forfeit
            # the turn: empty text is scored invalid -> honest by every
            # env, and nothing is appended to `self.last`, so the
            # trainer is not handed a zero-length sample to learn from.
            return ""
        seq = resp.sequences[0]
        text = self.r.tok.decode(seq.tokens, skip_special_tokens=True).strip()
        if self.close_bracket and "[" in text and not text.endswith("]"):
            # Tinker strips the stop string, so restore it -- otherwise the
            # parser sees an unterminated call and scores a perfectly good turn
            # invalid, which would make the best setting measure as the worst.
            text += "]"
        # `nmsg` is how the trainer maps a sampled turn back to the `Turn` it
        # came from. Nothing is appended when a turn is forfeited for want of
        # context (above), so position alone is not a safe key -- and
        # `cue_critic` has to featurise the RIGHT prefix or the baseline is
        # worse than no baseline. Every env's `Turn.messages` is the same list
        # that was passed here, so its length identifies the turn.
        self.last.append({"prompt": mi, "tokens": list(seq.tokens),
                          "logprobs": list(getattr(seq, "logprobs", []) or []),
                          "nmsg": len(messages)})
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
                          "tokens": ids, "logprobs": [-0.5] * len(ids),
                          "nmsg": len(messages)})
        return text

    def reset_trace(self):
        self.last = []


class _StubInput:
    def __init__(self, ints):
        self._ints = ints

    def to_ints(self):
        return list(self._ints)


def build(service_client, model_name: str, temperature: float = 1.0,
          max_tokens: int = 384, seed: Optional[int] = None,
          top_p: float = 1.0, close_bracket: bool = False,
          enable_thinking: bool = False, reasoning_effort: Optional[str] = None
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
    rend = Renderer(sc.get_tokenizer(), enable_thinking=enable_thinking,
                    reasoning_effort=reasoning_effort)
    return TinkerActor(sc, rend, temperature, max_tokens, seed,
                       top_p=top_p, close_bracket=close_bracket), rend
