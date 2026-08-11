# The arena: one yardstick for SPIRAL, MARSHAL, local and Tinker

Each training arm evaluates itself, and no two of them agree on what "evaluate"
means:

| arm | env | opponent | seats | n |
|---|---|---|---|---|
| SPIRAL (oat, local) | TextArena `KuhnPoker-v1`, 5 rounds | `random` | 0 only | 16 |
| SPIRAL (Tinker) | TextArena `KuhnPoker-v1`, 5 rounds | `random` | 0 only | 8 |
| MARSHAL (Tinker) | OpenSpiel `kuhn_poker`, 1 hand | `cfr` | 0 and 1 | 24/seat |

So the in-run numbers cannot be put in one table. "SPIRAL scored 37.5% and
MARSHAL scored -0.23" compares a win rate against a random bot to a chip return
against a near-Nash bot, on different games, at an n where the 95% interval is
roughly ±30 points. Two questions need answering and neither survives that:

- **Q1 — does the Tinker port reproduce the local implementation?**
- **Q2 — is SPIRAL or MARSHAL the better self-play algorithm?**

Both are the same experimental shape: hold the protocol fixed, vary exactly one
thing. `arena_eval.py` is the fixed protocol.

## Design

```
arena_eval.py     plays both protocols against an OpenAI-compatible endpoint
arena_report.py   reads the JSONs, prints the Q1 and Q2 contrasts
serve_arena.sh    throughput-tuned vLLM server (cf. serve_tinker_ckpt.sh, which
                  is tuned small for MASK)
merge_lora.py     LoRA + base -> full checkpoint
```

Three decisions worth knowing about:

**The game loops are imported from the training arms, not rewritten.** The
policy is scored by the same code that trained it, so a scoring bug cannot
flatter one arm over the other. Only the sampler is swapped — `VLLMSampler`
replaces `TinkerSampler`, matching both call signatures (SPIRAL passes a prompt
string, MARSHAL passes token ids).

**LoRAs are merged, not served as adapters.** vLLM 0.8.4 — the version oat pins
and the only one in this repo's venvs — crashes on adapter activation under
*both* engines (`'LoRALRUCache' object has no attribute '_LRUCache__update'`).
Merging avoids that path, and it is the better experiment anyway: the arena
compares Tinker LoRA checkpoints against local full-finetune checkpoints, and if
one went through vLLM's adapter code and the other did not, any difference would
be confounded with a difference in serving. After merging, all six policies are
plain HF checkpoints served by identical code.

**Both seats, and 200 games each.** The training evals played seat 0 only, which
in a game with a first-mover disadvantage is half a measurement. At n=400 pooled
the 95% Wilson interval on a win rate near 50% is about ±5 points, against ±30
at n=8 — the difference between a curve you can read and a curve you cannot.

## Reading the two protocols

They point in opposite directions and this is the single easiest thing to get
wrong:

- **`spiral` protocol — vs `random`.** A weak opponent. High win rate means "the
  policy learned the game at all". It is *not* a strength measure: an
  equilibrium Kuhn policy declines to exploit and scores **lower** here than a
  crude exploiter. Reading a decline as degradation is a mistake.
- **`marshal` protocol — vs `cfr`.** Near-Nash. You cannot beat CFR at Kuhn; you
  can only fail to lose to it. ~50% win rate and mean return near the game value
  (−1/18 for the first mover, +1/18 for the second) is the **ceiling**. Movement
  toward it is improvement.

`mean_return_valid` is reported next to `mean_return` for the CFR protocol.
Early in training the raw return is dominated by truncation forfeits scored −1
rather than by card play; the gap between the two numbers is the size of that
contamination.

## The home/away asymmetry

Each protocol carries its own prompt convention. SPIRAL suppresses `<think>`
(Qwen3-8B opens a think block that does not close inside the budget on that
prompt, and every unclosed turn scores as an invalid action). MARSHAL *requires*
`<think>...</think><answer>...</answer>`, so suppressing thinking there fails
the format check on every turn.

The convention is part of the protocol, so it is applied identically to every
policy — which is what makes the comparison fair, and also means each arm plays
one protocol under the convention it trained on and one under the other arm's.
A cross-protocol deficit is therefore partly a format-transfer result rather
than a pure card-play result. This is not corrected for; it is reported. The
invalid-action rate sits next to every score so the format component stays
visible, and if an arm's away-protocol deficit is mostly invalid actions, that
is what it is.

## Running

```bash
# serve (one GPU each; adapters get merged first)
python merge_lora.py --adapter ../ckpts/spiral-tinker-64 \
    --out ../ckpts/merged/spiral-tinker-64
./serve_arena.sh 8100 0 ../ckpts/merged/spiral-tinker-64
./serve_arena.sh 8101 1 <local-oat-run>/saved_models/step_00064
./serve_arena.sh 8104 4 Qwen/Qwen3-8B      # the untrained reference

# score (each label writes one JSON)
python arena_eval.py --base-url http://localhost:8100/v1 --model base \
    --label spiral-tinker-64 --protocols spiral,marshal --games 200 \
    --workers 48 --sequence-length 12800 --out ../results/arena/spiral-tinker-64.json

# compare
python arena_report.py ../results/arena/*.json
```

`--sequence-length 12800` matches `--max_model_len` in
`../training/run_kuhn_qwen3_8b.sh`. It must not exceed what the server was
started with, and it should not exceed what training used — the eval must not
admit a prompt the trained policy could never have seen.

Run it from the SPIRAL Tinker venv (`../training/tinker/.venv`), which is the
one venv carrying both `textarena` and `pyspiel`.

## What this still cannot tell you

`arena_eval.py` measures Kuhn Poker skill. That is the instrumental question.
This repo's actual question is whether zero-sum self-play degrades honesty, and
that is MASK — the arena is how you decide which checkpoints are worth the MASK
spend, not a substitute for it. Every merged checkpoint here drops straight into
`serve_ckpt.sh` → `run_mask.sh` → `compare_mask_arms.py`.

One confound no amount of n removes: oat trains all ~8B parameters, Tinker
trains a rank-32 LoRA. "Reproduces" can only ever mean "the port drives the
policy to the same place", never "the port computes the same update".
