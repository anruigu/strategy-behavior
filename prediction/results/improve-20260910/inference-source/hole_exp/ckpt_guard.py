"""Assert a named checkpoint actually loaded, before a sweep spends anything.

    from ckpt_guard import assert_differs_from_base
    assert_differs_from_base(ckpt_dir, tag="A-sweep")

WHY THIS EXISTS. `tinker_local.service.LocalServiceClient.create_sampling_client`
used to discard its arguments and hand back base weights for every checkpoint
anyone named. That has been fixed and now raises -- but the class of bug it
represents cannot be fixed by one patch, because **a checkpoint whose adapter
failed to load is indistinguishable from base weights by every downstream
metric**. Every curve comes out clean, plausible, and about the wrong policy.

So the guard is not "did the call succeed". It is "does the thing that came
back actually behave differently from base". That is the only check that
cannot be passed by a silent no-op.

IT COMPARES TEACHER-FORCED LOGPROBS, NOT SAMPLED TOKENS. The first version
of this guard sampled 24 greedy tokens from base and from the checkpoint and
demanded they differ. That is unsound in the direction that matters -- it
FALSELY CONDEMNS. Measured on this wave: every step-35 adapter has
max|lora_B| ~ 7e-4, and at that scale `grim/nohole` shifts the greedy path at
token 3 while `grim/eg` does not move it at all within 24 tokens. The eg
adapter is loaded, trained and non-zero; the probe simply could not see it,
and the sweep aborted on a healthy checkpoint.

Logprobs cannot hide that way. A LoRA with any non-zero B changes the logits
of EVERY token, so a teacher-forced pass over a fixed prompt separates
"loaded" from "not loaded" with no dependence on whether the change happened
to cross an argmax boundary. Base-vs-base is the noise floor and is measured
in the same call rather than assumed, because continuous batching makes even
identical weights non-bit-reproducible.

It costs three prompt evaluations and runs once per sweep.

WHAT A FAILURE MEANS, and it is not always a bug in the loader: a step-0
adapter is a freshly initialised LoRA whose B matrix is zero, so it is
mathematically identical to base and WILL fail this. That is correct
behaviour, not a false alarm -- a step-0 checkpoint carries no training signal
and a sweep that includes it is measuring base weights under another name.
Pass `allow_step0=True` only if you are deliberately using step 0 AS the base
reference, and then do not describe it as a trained arm.
"""
from __future__ import annotations

import os
from typing import Optional

# Short, fixed, and deliberately not a game prompt: this asks whether the
# weights differ, not whether the policy plays well. A long prompt would make
# the comparison depend on sampling noise deep in the sequence.
PROBE = ("You are playing a repeated game. In one short sentence, state your "
         "plan for the final round. I will defect on the last round because "
         "there is no future to protect.")
# Longer than a bare instruction on purpose: the statistic is averaged over the
# prompt's tokens, so a few more tokens of game-flavoured text is a cheaper way
# to raise sensitivity than more sampling.

MIN_DELTA = 0.01        # nats, mean over prompt tokens
NOISE_MULTIPLE = 10.0   # ... and at least this many times the base-vs-base floor


def _sample(client, tok, text: str, max_tokens: int, temperature: float):
    import tinker
    ids = tok.encode(text, add_special_tokens=False)
    mi = tinker.ModelInput.from_ints(ids)
    sp = tinker.SamplingParams(max_tokens=max_tokens, temperature=temperature,
                               top_p=1.0)
    out = client.sample(mi, num_samples=1, sampling_params=sp)
    seq = out.sequences[0]
    return list(getattr(seq, "tokens", None) or getattr(seq, "token_ids", []))


def _prompt_logprobs(client, tok, text: str):
    """Teacher-forced logprob of every token in `text` under `client`."""
    import requests
    ids = tok.encode(text, add_special_tokens=False)
    body = {"input_ids": ids,
            "sampling_params": {"max_new_tokens": 1, "temperature": 0.0},
            "return_logprob": True, "logprob_start_len": 0}
    if getattr(client, "lora_name", None):
        body["lora_path"] = client.lora_name
    r = requests.post(f"{client.base_url}/generate", json=body, timeout=300)
    r.raise_for_status()
    meta = r.json()["meta_info"]
    return [e[0] for e in (meta.get("input_token_logprobs") or [])
            if e[0] is not None]


def _mean_abs_delta(a, b) -> float:
    n = min(len(a), len(b))
    if not n:
        raise RuntimeError("server returned no prompt logprobs")
    return sum(abs(x - y) for x, y in zip(a[:n], b[:n])) / n


def assert_differs_from_base(ckpt: str, tag: str = "",
                             tokenizer_dir: Optional[str] = None,
                             max_tokens: int = 24,
                             min_delta: float = MIN_DELTA) -> float:
    """Raise unless `ckpt` moves the model's logprobs away from base weights.

    Returns the measured mean |delta logprob| in nats, so a caller can log how
    much signal each arm actually carries -- a checkpoint that only just
    clears the floor is worth knowing about before it becomes a result.

    `max_tokens` is accepted and ignored; it belonged to the sampled-token
    version and is kept so existing call sites do not break.
    """
    from tinker_local.service import LocalServiceClient
    from transformers import AutoTokenizer

    md = tokenizer_dir or os.environ.get("THINK4_MODEL_DIR",
                                         "/shared/clod/qwen3.8-27b")
    tok = AutoTokenizer.from_pretrained(md)
    svc = LocalServiceClient()

    base = svc.create_sampling_client()
    tuned = svc.create_sampling_client(base_model=ckpt)

    b1 = _prompt_logprobs(base, tok, PROBE)
    b2 = _prompt_logprobs(base, tok, PROBE)      # the floor, measured not assumed
    t = _prompt_logprobs(tuned, tok, PROBE)

    noise = _mean_abs_delta(b1, b2)
    delta = _mean_abs_delta(b1, t)
    floor = max(min_delta, NOISE_MULTIPLE * noise)

    if delta < floor:
        raise RuntimeError(
            f"[{tag or 'ckpt_guard'}] {ckpt!r} moved the mean prompt logprob "
            f"by only {delta:.5f} nats (floor {floor:.5f}, base-vs-base noise "
            f"{noise:.5f}). Either the adapter did not load, or this is a "
            f"step-0 checkpoint (zero-initialised LoRA B matrix, "
            f"mathematically identical to base). Refusing to run a sweep that "
            f"would report base-weight behaviour as a trained arm.")
    return delta


def first_divergence(a, b) -> int:
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return i
    return min(len(a), len(b))
