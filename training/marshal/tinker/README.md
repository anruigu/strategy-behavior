# MARSHAL Kuhn Poker self-play on Tinker

A Tinker port of [MARSHAL](https://github.com/thu-nics/MARSHAL)'s Kuhn Poker
self-play arm ([arXiv 2510.15414](https://arxiv.org/abs/2510.15414), ICLR 2026),
built to sit next to `../../tinker/` (the SPIRAL arm) so the two self-play
algorithms can be compared on the same game and the same base model.

MARSHAL upstream runs on ROLL: ray + hydra + Megatron-LM + mcore_adapter + vLLM,
8 GPUs at `tensor_model_parallel_size 4`. This arm imports only the two pieces
that do not need any of that — the OpenSpiel env and the advantage math — and
lets Tinker do sampling and gradients. Installs in minutes, runs on a laptop.

```
config.py                 hyperparameters, each traced to a line in MARSHAL's yaml
selfplay.py               game loop, ChatML construction, action parsing
advantage.py              MARSHAL credit assignment, calling ROLL's own tensor code
train_marshal_tinker.py   Tinker clients, Datum assembly, training loop, eval
run_kuhn_marshal_tinker.sh
```

## What is actually MARSHAL's, and what is ours

The paper's contribution is credit assignment, so that is the part we do not
reimplement. `advantage.py` **imports ROLL's own functions** —
`score_normalize`, `masked_whiten`, `compute_reinforce_return`,
`normalize_unique_values` — and calls them in ROLL's order.
`roll.utils.functionals` turns out to import with only torch + tensordict +
numpy, so the arithmetic is bit-identical and there is nothing to drift.

The two mechanisms:

1. **Turn-level advantage estimator.** Each assistant turn carries its own score
   at its last token (which lands exactly on `<|im_end|>`, where ROLL's
   `get_masks_and_scores` puts it). The advantage at token *t* is the reverse
   discounted sum of every score at or after *t*, so an early turn is credited
   with what the rest of the hand actually earned.
2. **Agent-specific advantage normalization.** In self-play the two seats have
   systematically different return distributions — in Kuhn, player 0 acts first
   and is the one who can be bluffed off a hand — so rewards *and* advantages
   are centred within each seat, not across the pooled batch.

What we do reimplement is the **split**: ROLL's `_by_player` wrappers take a
`DataProto` and recover the seat from `group_ids` strings ending `_p0`/`_p1`.
Building a DataProto would drag in the training stack, so we pass explicit
player ids and index-split ourselves, calling the same underlying per-group
function. See `_split_by_player`.

## Comparing against the SPIRAL arm

Both play KuhnPoker self-play on `Qwen/Qwen3-8B` with rank-32 LoRA, 128 rows per
policy step. That is the controlled comparison. Everything else differs:

| | SPIRAL (`../../tinker/`) | MARSHAL (here) |
|---|---|---|
| env | TextArena `KuhnPoker-v1`, 5 rounds | OpenSpiel `kuhn_poker`, 1 hand |
| turns/episode | ~8.8 | ~2.2 |
| prompt | fresh single-turn re-render | growing multi-turn chat |
| action format | `\boxed{bet}` | `<think>..</think><answer><BET></answer>` |
| credit | RAE: per-(env,seat) EMA on the final outcome | turn-level reward → reverse discounted return |
| normalization | subtract the seat's EMA | per-seat centering of rewards *and* advantages |
| Datum | one per turn | one per (episode, seat), multi-turn merged |
| eval opponent | `random` | **CFR** (near-Nash) |

The eval opponent difference matters for reading results. SPIRAL evaluates
against `random`, where a higher win rate is unambiguously better but a
near-equilibrium policy scores *worse*. MARSHAL evaluates against CFR, where
~50% win rate / ~0 mean return is the **ceiling**, not a floor — move toward it,
not past it.

Neither Tinker arm is comparable to `results/`, which is `Qwen3-4B-Base`
full-finetune. Both need their own base-model MASK arm.

## Divergences from MARSHAL

- **Base model / method.** MARSHAL trains `Qwen3-4B` full-parameter via
  Megatron. Tinker hosts neither Qwen3-4B nor full finetuning. `Qwen3-8B` is
  chosen to match the SPIRAL Tinker arm.
- **Learning rate.** MARSHAL's `1e-6` is a full-parameter LR; a rank-32 LoRA
  wants ~10×. Default here is `1e-5`. Pass `--learning-rate 1e-6` for literal
  fidelity — and see `../../tinker/README.md`, where inheriting a full-finetune
  LR into LoRA produced 64 flat steps.
- **No KL.** MARSHAL uses `use_kl_loss: true, kl_loss_coef: 0.20` — a
  differentiable KL against a frozen reference. Tinker's `ppo` /
  `importance_sampling` losses expose no KL term and there is no reference-model
  handle. 0.20 is a strong coefficient, so expect this arm to drift from the
  base policy faster than MARSHAL's does. **This is the largest algorithmic gap.**
- **No dual-clip** (`dual_clip_loss: true`), and **no `top_k`** (MARSHAL sets
  100; `SamplingParams` has no such field).

## Running

```bash
"$SAT_TINKER_VENV/bin/pip" install -r requirements.txt   # shares the SPIRAL venv
./run_kuhn_marshal_tinker.sh --scale smoke --dry-run     # free, offline
./run_kuhn_marshal_tinker.sh --scale short               # 64 steps
```

Checkpoints go through the SPIRAL arm's exporter unchanged — same `tinker://`
path shape, same PEFT output:

```bash
python ../../tinker/export_lora.py --checkpoints <run>/checkpoints.jsonl \
    --step 64 --out "$SAT_CKPT_DIR/marshal-tinker-kuhn-step64"
../../../evals/serve_tinker_ckpt.sh "$SAT_CKPT_DIR/marshal-tinker-kuhn-step64" \
    marshal-tinker-kuhn-step64 8000 0
```

## Gotchas

- **Tinker returns the stop token.** A sampled turn ends `…</answer>`,
  `<|im_end|>`, so the assistant turn is already closed and the next chat delta
  must not re-open it. Emitting a second `<|im_end|>` desynchronises the ChatML
  from turn 2 onward and the model then answers into a malformed conversation.
  Cost when we got this wrong: a 54% invalid-action rate with no error anywhere.
- **Never re-render the chat with `apply_chat_template`.** Re-tokenising
  re-encodes the assistant turns, and a decoded→re-encoded response does not
  always reproduce the sampled ids — measured at 5 breaks in 31 turns on
  Qwen3-8B. `ChatBuilder` appends the ChatML delta instead, so the sequence we
  train on is token-for-token the sequence we sampled from and the prefix
  property the merged Datum needs holds by construction. `prefix_breaks` in the
  metrics should stay 0.
- **Budget the generation properly.** Qwen3-8B spends ~425–450 tokens thinking
  about a single Kuhn decision. Cap it too low and the response never reaches
  `</think><answer>`, so it fails the format check and forfeits. At a 2048 cap
  we measured `truncated_rate` *exactly equal* to `invalid_rate` — every single
  failure was a truncation. MARSHAL's 4096 is the right budget; the `smoke`
  scale is the only place we reduce it.
- **`score_normalize` divides by a variance it does not need.** ROLL computes
  `masked_var` before branching on `method`, so even `method="mean"` raises
  "The sum of the mask is one" when a seat contributes exactly one scored
  position. ROLL never trips it at 128 rows with a fixed env count; smaller
  batches do. `advantage.py` guards it and mean-centres directly.
- **Episodes are short.** An OpenSpiel Kuhn hand is 2–3 actions, against ~9 for
  SPIRAL's 5-round TextArena version. Per policy step this arm samples far fewer
  tokens, so it is cheaper — but each step also carries less signal.
