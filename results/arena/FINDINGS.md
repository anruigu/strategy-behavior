# Arena results — 2026-08-08

Two questions, settled on one yardstick. Harness and method: `../../evals/ARENA.md`.
Raw JSONs: `./` (both protocols) and `../arena_clean/` (SPIRAL protocol, with the
clean-games split added).

All numbers: `Qwen/Qwen3-8B`, n=400 games per policy per protocol (200 per seat,
both seats), 95% Wilson intervals, temperature 0.6.

## The table

**SPIRAL protocol** — TextArena `KuhnPoker-v1`, 5 rounds, vs `random`:

| policy | all games | clean games only | invalid |
|---|---|---|---|
| base-qwen3-8b | 45.5% [41,50] | 62.8% [57,68] (n=290) | 5.6% |
| local-oat-64 | 62.7% [58,67] | 63.7% [59,68] (n=394) | 0.3% |
| local-oat-96 | 67.2% [63,72] | 70.1% [65,74] (n=384) | 0.8% |
| spiral-tinker-64 | 42.0% [37,47] | 57.9% [52,63] (n=290) | 5.6% |
| marshal-tinker-48 | 41.5% [37,46] | 59.3% [53,65] (n=280) | 6.1% |
| marshal-tinker-64 | 44.0% [39,49] | 64.7% [59,70] (n=282) | 6.6% |

**MARSHAL protocol** — OpenSpiel `kuhn_poker`, 1 hand, vs `cfr` (near-Nash;
~50% and return ~0 is the ceiling, not the floor):

| policy | win | mean return | valid-only return | invalid |
|---|---|---|---|---|
| base-qwen3-8b | 50.0% [45,55] | −0.237 | −0.103 (n=340) | 14.6% |
| local-oat-64 | 56.5% [52,61] | −0.160 | −0.120 (n=382) | 4.4% |
| local-oat-96 | 57.0% [52,62] | −0.170 | −0.147 (n=389) | 2.7% |
| spiral-tinker-64 | 49.5% [45,54] | −0.258 | −0.121 (n=338) | 15.1% |
| marshal-tinker-48 | 50.2% [45,55] | −0.247 | −0.135 (n=348) | 12.7% |
| marshal-tinker-64 | 49.2% [44,54] | −0.268 | — | 11.3% |

## Q1 — does the Tinker port reproduce local? **No.**

Same algorithm (SPIRAL), same base model, same step (64), same 128 rows per
policy step. Only the implementation differs.

| | vs random | vs CFR |
|---|---|---|
| local-oat-64 | 62.7% | 56.5% |
| spiral-tinker-64 | 42.0% | 49.5% |
| | p < 0.001 | p = 0.047 |

The local oat run moved the policy; the Tinker run left it on top of the
untrained base on both protocols. The invalid-action rate is the clearest tell:
oat drove it 5.6% → 0.3%, Tinker sat at 5.6% — the base rate, unchanged.

**Two candidate explanations, and they are separable:**

1. **The learning rate.** The Tinker arm inherited `1e-6` from SPIRAL's
   full-finetune recipe. On a rank-32 LoRA that is roughly 10× too low, and it
   is exactly the failure mode already documented in
   `../../training/marshal/tinker/config.py`. A matched re-run at `1e-5`
   (128 turns/step, everything else identical — only the LR changed) is
   running: wandb `thefleet/spiral/runs/xb8dwljd`.
2. **A bug in the port.** Less likely but not excluded. `test_parity.py` binds
   spiral's own `extract_action` / `extract_chat_action` / `prepare_trajectories`
   and diffs them against the port: kuhn 64/64, multi 106/106, pigdice 64/64.
   That covers action parsing and trajectory prep, not the gradient path.

If the `1e-5` run moves and the `1e-6` run did not, it is (1) and the port is
fine. If neither moves, the gradient path needs auditing.

**A confound no amount of n removes:** oat trains all ~8B parameters, Tinker
trains a rank-32 LoRA. "Reproduces" here can only ever mean "drives the policy
to the same place", never "computes the same update".

## Q2 — SPIRAL or MARSHAL? **Unanswerable from these runs. Neither trained.**

Every Tinker checkpoint is statistically indistinguishable from the untrained
base, on both protocols, including each arm's own home turf:

| | vs random (SPIRAL's turf) | vs CFR (MARSHAL's turf) |
|---|---|---|
| base | 45.5% | 50.0% |
| spiral-tinker-64 | 42.0% (p=0.115) | 49.5% (p=0.888) |
| marshal-tinker-48 | 41.5% (p=0.153) | 50.2% (p=0.944) |
| marshal-tinker-64 | 45.0% (p=0.88) | 49.2% (p=0.82) |

There is no signal, so there is nothing to compare. The per-arm eval curves
reported before this harness existed (SPIRAL 75→37.5% vs random, MARSHAL −0.19
→ −0.42 → −0.23 vs CFR) were n=8 and n=24: pure noise, and the apparent trends
in them are not real.

Answering Q2 requires first getting at least one Tinker arm to move — hence the
`1e-5` run.

## Q3 — did self-play teach the game, or the output format?

This was not asked, and it may matter more than either answer above.

An invalid action forfeits the game. So a policy that only learned to emit
`\boxed{...}` reliably posts a much higher win rate with its card play
completely unchanged. Restricting to games where **every** model turn parsed
separates the two:

| policy | all | clean | vs base (clean) |
|---|---|---|---|
| base-qwen3-8b | 45.5% | 62.8% | — |
| local-oat-64 | 62.7% | 63.7% | **+0.9%, p=0.800** |
| local-oat-96 | 67.2% | 70.1% | +7.3%, p=0.046 |
| spiral-tinker-64 | 42.0% | 57.9% | −4.8%, p=0.235 |
| marshal-tinker-48 | 41.5% | 59.3% | −3.5%, p=0.395 |
| marshal-tinker-64 | 44.0% | 64.7% | +1.9%, p=0.631 |

**At step 64, local oat's entire +17-point gain is format compliance.** Card
play is indistinguishable from the untrained model (p=0.80). Base already wins
62.8% of the games it manages to format correctly; it just forfeits 110 of 400
on syntax, where local-oat forfeits 6.

Only by step 96 does a card-play gain appear, and it is modest and marginal
(+7.3%, p=0.046 — one test, uncorrected).

The CFR protocol says the same thing from the other side: restricted to
non-forfeited hands, local-oat-64 returns **−0.120** against base's **−0.103**,
and local-oat-96 is **−0.147**. Conditional on not forfeiting, the trained
models play Kuhn no better than base — slightly worse.

**Why this matters for the repo's actual question.** This project asks whether
zero-sum self-play degrades honesty. If what self-play mostly does at these
step counts is teach output formatting, then a MASK delta measured against
these checkpoints is at risk of measuring format/instruction-following drift
rather than anything about strategic deception. The clean-games split should be
reported alongside any MASK result, and the step-96+ checkpoints are the ones
where a genuine strategy change has started.

## Caveats

- **Home/away.** Each protocol carries its own prompt convention (SPIRAL
  suppresses `<think>`, MARSHAL requires it), applied identically to every
  policy. So each arm plays one protocol under its training convention and one
  under the other's, and a cross-protocol deficit is partly format transfer.
  Invalid rates are printed next to every score for this reason.
- **Run-to-run spread is real.** local-oat-64 scored 67.0% and 62.7% on two
  independent n=400 runs at the same seed (temperature 0.6). Treat ~4 points as
  the noise floor for a single n=400 measurement and do not read smaller
  differences.
- **Single uncorrected tests.** The p-values above are individual
  two-proportion z-tests, not corrected for the ~20 comparisons in this table.
  p=0.046 should be read as "suggestive", not "established".
- The local oat run died at step 101 (hung after the step-101 `learn()`, GPUs
  released, launchpad parent left as a zombie). Steps 16–96 are checkpointed and
  intact; nothing above depends on the steps past 96.
