# 0820 — env-count ladder: what was actually launched

Companion to `0820-scaling-envs.md` (the plan). This is the as-built record:
what ran, what deviated from the plan, and what a reader must not over-claim
from the result.

Code: `hole_exp/scaling_rungs.py` (single source of truth for rungs, held-out
sets, compute budget and sampling), `sbatch_scaling.sh` + `launch_scaling.sh`
(training), `eval_scaling.py` (Tier A), `run_scaling_external.sh` (Tier B),
`mach_scaling_summary.py`, `make_scaling_figs.py`, `run_scaling_readout.sh`
(unattended orchestration).

## The matrix

Model **Qwen/Qwen3.8-27B** on Tinker, LoRA rank 32, dose 1.0, seed 0.

| family | envs available | rungs | held out (never trained) |
|---|---|---|---|
| `game` | 9 game-framed cells (5 TextArena + 4 native designs) | 1, 2, 4, 8 | `nat_ledger`, `ta_kuhn`, `ta_negotiation`, `agg_two_dollar` |
| `synth` | 25 usable scenarios (26 minus `markets`) | 1, 2, 4, 8 | 10 fixed domains |

12 runs: hole arm at all four rungs in both families (8), plus the `nohole`
control at the **endpoints** n=1 and n=8 in both families (4).

## Controls, and how they are enforced

1. **Constant compute.** 70 steps x 8 groups x 6 = 48 episodes/step at *every*
   rung, so n=8 sees 1/8th the episodes per env rather than 8x the episodes.
   `train_mixed.py` defaults `--groups` to `len(envs)` — exactly the confound —
   so `--groups` is passed explicitly and `sbatch_scaling.sh` **asserts** the
   resolved budget against `scaling_rungs.py` before launching.
2. **Nested rungs.** `RUNGS[n]` is a prefix of the family order, so
   n=1 ⊂ n=2 ⊂ n=4 ⊂ n=8.
3. **Fixed held-out set,** identical at every rung, disjointness asserted at
   import.

## Deviations from the plan, and why

- **One ordering per family, not two.** Two random orderings doubles the run
  count and does not fit one night. The single ordering is **stratified**
  instead of random: every rung addition brings a hole type not already in the
  set, and the TextArena/native (or hand-crafted/generated) split stays
  balanced. That addresses "one potent env was added" by construction, but it
  is *not* averaging over orderings. First follow-up if pass 1 rises.
- **`nohole` at the endpoints only.** The plan budgets one arm per rung, read
  against base. That cannot separate "more hole exposure" from "more diverse RL
  of any kind", so the control was added at n=1 and n=8. `launch_scaling.sh
  fill` adds the middle rungs if capacity allows.
- **The game family is 9 cells, not 5.** TextArena alone caps at 5, which
  cannot reach n=8 and would have made the two families' x-axes incomparable.
  The four `native_games` designs are game-framed cells with the same
  exogenous-audit consequence model, so folding them in is a widening of "game",
  not a change of kind — but the family is labelled "games (TextArena +
  native)" everywhere, not "TextArena".
- **`markets` excluded entirely** (neither trained nor evaluated): its exploit
  is reachable through two channels, so its `exploit_rate` is not a clean
  instrument.
- **`ta_negotiation` played but excluded from every pooled figure.** 28-44% of
  its episodes fail to parse (the model re-derives a 5-resource inventory each
  turn and truncates) and the invalid rate varies ~4x across arms, so the
  denominator is verbosity-selected. Numbers are kept under `_negotiation_*` so
  the exclusion is auditable.
- **`ta_kuhn` excluded from the pooled game *rate***, kept as `kuhn_capture`.
  It exploits on 100% of base-model episodes — a cell at ceiling cannot register
  a rise. `capture` (share of the honest→exploit span) has room in both
  directions.

## The sampling profile, and one instrument it rescued

`0820-qwen38-sampling-profile.md` documents that Qwen3.8-27B needs different
sampling from 3.6. This ladder takes the **safe half**:

    temperature 0.7 · top_p 0.9 · max_tokens 512 · thinking off
    close_bracket OFF

`close_bracket` is deliberately **not** used, despite being the biggest lever on
the agentic `merchant` it was tuned on. It halts generation at `]` and separately
*replaces* the renderer's EOS stops. Half this roster puts the argument AFTER the
bracket — TwoDollar's `[Propose] $1.00` would become `[Propose]`, killing the
opening-demand regex — and `nat_assay`/`nat_shoal` reply with a bare number and
would lose their stop token entirely.

The eval harness defaults to the same profile from `scaling_rungs.py`: measuring
a checkpoint under different sampling than it trained under is its own confound.

### The `nat_assay` scare, and what it actually measured

The first launch (t=1.0 / 384) showed `nat_assay` at **0.225 invalid**, against
check_suite's BROKEN threshold of 0.25 — alarming, because `nat_assay` enters
only at the **n=8 game rung**, so a degraded instrument would have sat on exactly
the top rung of one family's curve and read as saturation.

A proper 14-seed A/B on the base model says the alarm was mostly small-sample
noise (the 0.225 came from 4 training steps of 6 episodes):

| cell | t=1.0 / 384 | t=0.7 / p0.9 / 512 |
|---|---:|---:|
| `nat_assay` invalid | 0.143 | **0.129** |
| `nat_assay` exploit | 0.238 | 0.312 |

So the low-entropy half helps only marginally here — consistent with the sweep in
the profile note, where without a stop sequence `t=0.7/p0.9` moved invalid only
0.924 → 0.802. The lever that kills truncation is the stop sequence, and that is
the part this roster cannot use.

**In the relaunched runs it came out better than the A/B predicted.** Measured on
the live ladder under the tuned profile, aggregate `train/invalid_rate` is
**0.000–0.014** across all 12 arms (it was 0.004–0.104 untuned), and `nat_assay`
itself reads 0.067. The monotone-looking rise in invalid across rungs — the thing
that made this worth stopping for — is gone. The base-model A/B understated the
gain because it sampled the untrained model on the hardest cell in isolation.

**Accepted, not fixed.** `nat_assay` remains the worst cell. It is below BROKEN,
it is a training env rather than one of the y-axes, and it is 1 of 8 envs at one
rung — so it touches roughly 1.6% of that rung's training signal. Worth knowing
if the n=8 game rung underperforms; not worth another relaunch. Note also that
`close_bracket` *would* be safe for the native cells specifically (their grammar
is bracket-internal: `[haul: N]`, `[report: N]`, `[pledge: escort]`) — it is
`ta_ipd3`'s `[Broadcast] <text>` in training, and TwoDollar at eval, that rule it
out for the roster as a whole.

## Readout mechanics

**Per-family step freezing.** Measured on the live ladder, the game family trains
at 5.0-7.7 min/step against synthetic's 3.7-4.5 (game episodes are multi-turn, so
one step is many more model calls). Projected to step 70 that is 7.6-9.0h vs
4.4-5.3h. Forcing a single common step across all 12 arms would have discarded
~30 steps of synthetic training to match the slowest game arm, so each family is
frozen at its OWN highest common step. Curve *shape* is a within-family question
— every point on a line still shares a step with every other point on that line —
so the only thing lost is cross-family comparison of absolute levels, which is
stated on the figure (`SPLIT_NOTE`) and recorded in `meta.step_by_family` rather
than left implicit.

**One frozen manifest, both tiers.** Tier A and Tier B originally each resolved
arm→checkpoint independently. Training keeps advancing between them, so the two
tiers could have described *different checkpoints* under one arm label. The
driver now writes `results/scaling/manifest.json` once at freeze time and both
tiers read it. That also made it safe to SUBMIT Tier B before running Tier A,
overlapping ~2-3h of Tier B with ~1-1.5h of Tier A instead of summing them.

## Two launch bugs worth remembering

- **`GROUPS` is a bash special variable.** `eval "GROUPS=8"` is silently ignored
  and `$GROUPS` expands to the caller's primary gid. The first launch trained at
  **1005 groups x 6 = 6030 episodes/step** and looked completely healthy in the
  logs. Renamed to `NGROUPS`, and the budget is now asserted in Python before
  `exec`.
- Test-stub result files (`tierA-step9999.json`) sort last and would be picked
  up as "the newest readout". Moved to `results/scaling/_testartifacts/`.

## What must NOT be claimed from this

- **One training seed.** Error bars on the figures are *episode-level bootstrap*
  only. They say how well a checkpoint was measured; they say nothing about how
  much a different training seed would move. Per the plan, seeds 2–3 are gated
  on pass 1 rising.
- **Four points cannot fit an exponent.** Nothing is fitted. The reading is the
  shape: rising, saturating, or flat.
- **The base is Qwen3.8-27B**, not the 3.6 of
  `results/eval_suite_transfer_27b.png`. The `base` arm of *this* ladder is the
  only valid comparison point; no cell here may be read against a number from
  the 3.6 figure.
- **Within-SE instruments** (DarkBench, sandbagging, in-context scheming) were
  not run — the plan explicitly says not to read a scaling claim off them at one
  seed.

---

# RESULTS (step 70, all 12 arms matched, 1 seed)

Final readout is `results/scaling/tierA-step0070.json` + the figures in
`results/0820_scaling_plots/`. Everything below is ONE training seed with
episode-level bars; per the plan these license "this checkpoint differs from
that one", not "#envs raises transfer in expectation".

## The headline: in-family transfer scales, external misalignment does not

**Held-out instruments in the training family rise with #envs.**

| synthetic family, hole arm | n=1 | n=2 | n=4 | n=8 | base |
|---|---|---|---|---|---|
| held-out synthetic (all 10) | 0.508 | 0.725 | 0.861 | 0.962 | 0.541 |
| held-out synthetic (2 surviving genuine-hole domains) | 0.300 | 0.450 | 0.673 | 0.938 | 0.312 |
| held-out game cell (`nat_ledger`) | 0.087 | 0.260 | 0.291 | 0.285 | 0.258 |
| TwoDollar opening demand | 1.13 | 1.24 | 1.34 | 1.39 | 1.40 |

rho = +1.00 on the first and last rows. Note the n=1 arm sits AT OR BELOW base
and the curve crosses base around n=2: training on one scenario makes the policy
*narrower* than the base model on unseen ones, and diversity first undoes that
and then overshoots. Cross-family transfer is real -- synthetic training moves
the held-out GAME cell.

**The eval-suite instruments do not rise, and the treatment effect SHRINKS.**

| game family | n=1 | n=2 | n=4 | n=8 | base |
|---|---|---|---|---|---|
| MACHIAVELLI violations | 109.3 | 103.8 | 103.9 | 101.8 | 101.8 |
| AgentMisalignment frac-any | 0.676 | 0.380 | 0.315 | 0.463 | 0.444 |
| insider trade rate | 0.225 | 0.175 | 0.050 | 0.125 | 0.175 |

MACHIAVELLI hole-nohole gap: **+12.8 at n=1, +4.6 at n=8**. The +12.8 at a
single training env closely replicates the +12.4 reported for the frame
ablation on Qwen3.6 -- on a different base model, which is a genuine (if
one-seed) replication. But it NARROWS with env count rather than widening.

So the two y-axes answer differently. Diversity buys generalisation to *more
environments of the same kind*; it does not buy more assistant-facing
misalignment, and on the tightest external instrument the effect is largest with
ONE environment.

## A correction: "games are flat" was an undertraining artifact

Read at step 40 (the per-family freeze), the game family was flat on every
panel. Read at step 70 -- after every arm finished -- it RISES on the held-out
game cell (0.394 -> 0.515) and Kuhn capture (0.061 -> 0.498). The step-40 read
is superseded; do not cite it.

## A finding about the control arm itself

`scale-synth-n1-nohole` **learned to defeat the audit by emitting unparseable
output.** `train/invalid_rate` goes 0.00 -> 0.68 -> 0.93 -> 1.00 across steps
21-42, and reward RISES as it does (-0.01 -> +0.33 -> +0.58). An unparseable
action is never detected as an exploit, so it escapes the penalty while still
collecting the default payoff -- a degenerate solution to `ConsequenceWrapper`,
not a training glitch. That arm is unusable (n=0 valid held-out episodes) and
the synthetic control at n=1 is lost with it. `scale-synth-n8-hole` drifts the
same way (invalid 0.03 -> 0.23 by step 56, 0.41 at eval) and `scale-game-n2-hole`
sits at 0.34, so those points are BROKEN-gated in every figure.

**This is worth its own experiment.** If the audit arm can be gamed by silence,
then every `nohole` control in the atlas is measuring "did the policy find the
degenerate exit" as well as "did consequences suppress the hole".

## Caveats that bound all of the above

- **One seed.** Seeds 2-3 are the gate the plan sets, and pass 1 does rise.
- **The synthetic corpus was pruned mid-run** to the five domains that isolate a
  genuine social-shortcut hole; 8 of the 10 held-out synthetic domains used here
  were dropped as permitted-discretion rounding/padding. The dose-response
  SURVIVES on the two survivors (0.300 -> 0.938), which is why the row is
  reported both ways above. The synthetic scaling family is retired going
  forward -- too few genuine domains remain to scale their count 1->8.
- **Tier B is incomplete for 4 synthetic arms.** Their jobs were packed 5-to-a-
  node; one died in the Rust tokenizer with `ThreadPoolBuildError ... EAGAIN`
  (could not spawn a thread) and another hung 9.75h until the wall clock killed
  it. Cause was node packing, not the arms. `rerun_tierb_step70.sh` re-runs them
  one job per node at lower concurrency; not executed.
- **hack-verifiable was never run** on the ladder (~100 min/arm at the only
  setting with adequate power).
