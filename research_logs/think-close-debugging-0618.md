# Missing `</think>` in negotiation traces — debugging & fix plan (06-18)

Run: `fleet_qwen35_35b_negotiation_dnd_outcome_recover-nash-0618` (added to trace viewer, http://localhost:8792).

## Symptom
Traces in the viewer frequently show a `<think>` with no closing `</think>`.

## Finding: it's a generation issue, not a display bug
The raw trajectory JSONL genuinely lacks the closing tag — the viewer renders faithfully.

Tag balance across **7,266 assistant turns** in this run:
- 5,001 balanced
- **2,253 open `<think>` with no `</think>` (~31%)**
- 12 close-without-open

These are **not truncations**: only 4 trajectories hit `stop_reason: length`; the rest are clean `stop`. Every unclosed-think turn terminates cleanly:
```
<think>
...full reasoning...
<propose>{"book": 1, "hat": 0, "ball": 1}</propose><|im_end|>
```
The reasoning is complete, the action tag is well-formed, the turn ends on a clean `<|im_end|>`. The model simply **never emits `</think>`** — it opens think, reasons, emits its message + action *inside* the still-open block, and ends the turn. So the action tag ends up nested within the unclosed `<think>`.

Behavior is **bimodal**: turns are either `<think>\n\n</think>` (empty, properly closed) or `<think>…full reasoning…<propose>…</propose><|im_end|>` (full reasoning, never closed). Empty-think turns retain their `</think>` in the same files, so nothing is globally stripping the tag — the difference is real model behavior.

Viewer angle is secondary: `app.js:83` styles think with regex `&lt;think&gt;([\s\S]*?)&lt;/think&gt;`, which requires the close, so unclosed blocks fall through to plain text. Cosmetic only.

## Why a small format penalty is the wrong first move
1. **Gets gamed into empty-think.** A penalty on "unclosed think" pushes mass toward the empty-but-closed mode — model satisfies format while abandoning reasoning. This is the same failure as the `structured_think` arm (think_nonempty_rate → 0, entropy/KL/grad collapse).
2. **Too small = ignored.** Outcome reward already pays out with malformed think (env parses `<propose>` regardless of nesting), so a sub-noise penalty won't move the policy.

## The bigger concern: likely a correctness bug, not just cosmetics
`skyrl/train/generators/skyrl_gym_generator.py` uses a **custom chat template to compute loss masks for Qwen3 thinking models** and to **strip think tokens from non-last-round assistant messages** (lines ~168–170, 315, 331). Both key off the `</think>` boundary.

When `</think>` is missing, boundary detection breaks. Likely consequence: **in ~31% of turns the `<propose>`/`<accept>` tokens sit inside the unclosed think span and may be masked out of the loss (or the whole turn stripped from history)** — i.e. we could be training with no gradient on the actual actions in a third of turns. Confirm this before any reward shaping; it could explain slow/weird learning on its own.

## Fix plan (in order)
1. **Verify the loss mask first.** Check whether action tokens in unclosed-think turns land in `loss_mask=0`. If yes, that's the real bug — fix boundary handling (treat `<|im_end|>` as an implicit think-close fallback) and learning may recover without touching reward.
2. **Root-cause the generation / template.** Bimodal pattern smells like a template/parse inconsistency: is the template auto-prepending `<think>` and relying on the model to close it? Are stop strings / `enable_thinking` consistent across turns? May be a free config fix.
3. **If shaping reward, use a validity gate — not a scalar.** Make outcome reward conditional on: exactly one `<think>…</think>`, **non-whitespace** content inside it, and the action tag **after** `</think>`. Binary "malformed → no positive reward" is much harder to game than a soft penalty; the non-empty requirement closes the empty-think escape hatch.
4. **Keep entropy + KL anchors on** (the `structured_think` arm died without them) and **log per step**: `think_closed_rate`, `action_inside_think_rate`, `think_nonempty_rate` — catch gaming within ~20 steps instead of at post-mortem.
5. **Strongest option to kill it outright:** constrain decoding so an open `<think>` must close before any action tag is allowed (grammar/structured gen), or deterministically inject `</think>`. Sidesteps reward gaming entirely; more wiring.

## Check #1 result — DISPROVEN (not the bug)
Action tokens in unclosed-think turns are **not** masked out of the loss. This run uses
`qwen3_without_thinking` + `use_conversation_multi_turn` ⇒ the loss mask comes entirely
from the template's `{% generation %}` span via `return_assistant_tokens_mask=True`. That
span wraps the whole assistant content (think+message+action), so `<propose>`/`<accept>`
always get `loss_mask=1` — verified by rendering the template. The `</think>` boundary only
controls *stripping prior-turn reasoning from non-last turns*, not the action loss mask.

Two **real** consequences of the missing `</think>` instead:
1. **Opponent sees an empty message** in ~31% of turns: env `_strip_think` uses
   `<think>.*` (greedy) on unclosed turns → nukes the visible prose + action display. (This
   is the *safe* failure — it never leaks values, so don't "repair" it by guessing.)
2. **Prior reasoning leaks into training context + gets loss=1**: the template strip
   (`split('</think>')`) no-ops on unclosed turns, so the CoT stays in later turns' context.

Boundary is **unrecoverable post-hoc** (traces: ~34% of unclosed-with-action turns have
message-like prose before the action, indistinguishable from late reasoning), so deterministic
normalization is out. Fix at the source.

## Fix 3 (implemented) — constrained decoding "think gate"
Force every TRAINING-rollout turn into `<think> (≥16 tok) </think> <message> <action>` via a
vLLM v1 logits processor. Anti-gaming (the prior force-open-`<think>` attempt collapsed to
empty `<think></think>` + reason-in-open): the min-think floor makes empty think impossible,
and action/EOS are masked until `</think>`, so reasoning must land in the private channel and
the reason-in-open incentive evaporates (soft backstop = existing value_leak penalty + adversarial
opponent + metrics). User chose soft anti-gaming, floor=16.

Files (repo: `skyrl-neg-wt`):
- `skyrl/backends/.../vllm/think_gate_logits_processor.py` — `ThinkGateLogitsProcessor`
  (subclasses vLLM v1 `AdapterLogitsProcessor`) + pure `apply_think_gate` + `build_think_gate_extra_args`
  (resolves `<think>`/`</think>`/action-start/`<|im_end|>` ids, asserts `</think>` is atomic).
- `vllm_engine.py` — registers the LP (FQCN string) on every engine; inert unless a request
  sets `extra_args` (so eval/other tasks unaffected).
- `skyrl_gym_generator.py::_maybe_inject_think_gate` — injects `extra_args` for **training only**
  (eval left unconstrained so `think_closed_rate` is a real signal); gated by env.
- `negotiation/env.py` — new `environment/think_closed_rate` metric (should ride ~1.0 when on).
- `fleet-negotiation-35b-run.sh` — thinking arm exports `NEGOTIATION_THINK_GATE=1`,
  `NEGOTIATION_THINK_GATE_MIN=16` (set `=0` to disable).

Tested: 6/6 pure-logic unit tests (`tests/train/generators/test_think_gate_logits_processor.py`)
+ end-to-end smoke test of the real vLLM LP subclass (force-think / floor / inert-after-close /
inert-without-extra_args). **Not** runnable end-to-end here (no GPU / distributed vLLM); watch
`environment/think_closed_rate`→~1.0, `think_nonempty_rate`, `value_leak_msgs` on first steps.
Caveat: vLLM rejects custom logits processors under speculative decoding (unused here).
