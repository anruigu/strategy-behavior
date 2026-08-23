# Does exploit transfer scale with the number of training environments?

**Env-count dose-response ladder, 0820.** Reader-facing findings. Method,
deviations and the as-built record are in
`research_logs/0820-scaling-envs-RUN.md`; the plan is `0820-scaling-envs.md`.

Model **Qwen/Qwen3.8-27B** on Tinker, LoRA rank 32, dose 1.0, **one seed**,
all 12 arms read at a matched **step 70**.

| file | what it is |
|---|---|
| `scaling-curves.png` | the dose-response, both families, base as a dashed rule |
| `scaling-control.png` | hole − nohole at the n=1 / n=8 endpoints |
| `scaling-table.md` | the same numbers as a table |
| `scaling-shape.md` | rising / saturating / flat verdict per curve, by a stated rule |

---

## Headline

**The two y-axes answer differently.** Environment diversity buys
generalisation to *more environments of the same kind*. It does not buy more
assistant-facing misalignment — and on the tightest external instrument the
effect is **largest with a single training environment**.

### 1. In-family transfer rises with #envs

Synthetic family, hole arm, held-out instruments never trained on:

| | n=1 | n=2 | n=4 | n=8 | base |
|---|---|---|---|---|---|
| held-out synthetic, all 10 domains | 0.508 | 0.725 | 0.861 | 0.962 | 0.541 |
| held-out synthetic, 2 surviving genuine-hole domains | 0.300 | 0.450 | 0.673 | 0.938 | 0.312 |
| held-out game cell (`nat_ledger`) | 0.087 | 0.260 | 0.291 | 0.285 | 0.258 |
| TwoDollar opening demand ($ of 2.00) | 1.13 | 1.24 | 1.34 | 1.39 | 1.40 |

rho = +1.00 on the first, second and last rows.

Two things worth more than the monotonicity:

- **The n=1 arm sits at or below base**, and the curve crosses base around n=2.
  Training on a single environment makes the policy *narrower* than the base
  model on unseen ones. Diversity first undoes that specialisation and only then
  overshoots. A "does exploitation transfer?" question asked at n=1 would have
  returned a null — or a negative.
- **Transfer crosses the family boundary.** Synthetic-scenario training moves
  the held-out *game* cell (0.087 → 0.285, crossing base). This is not surface
  reuse; the instrument is a different kind of task with a different hole type.

### 2. Eval-suite transfer does NOT rise — the treatment effect shrinks

Game family, hole arm:

| | n=1 | n=2 | n=4 | n=8 | base |
|---|---|---|---|---|---|
| MACHIAVELLI violations (Σ) | 109.3 | 103.8 | 103.9 | 101.8 | 101.8 |
| AgentMisalignment frac-any | 0.676 | 0.380 | 0.315 | 0.463 | 0.444 |
| insider trade rate | 0.225 | 0.175 | 0.050 | 0.125 | 0.175 |

And the matched control on the tightest of these:

> **MACHIAVELLI hole − nohole: +12.8 at n=1 → +4.6 at n=8.**

The +12.8 at a single training environment closely replicates the **+12.4**
reported for the frame ablation on Qwen3.6 — a different base model, so this is
a genuine (one-seed) replication of the headline MACHIAVELLI effect. But the gap
**narrows** as environments are added rather than widening.

If that survives seeding, the practical reading is uncomfortable for the
"diversity is what makes it dangerous" intuition: the most externally
misaligned checkpoint in this ladder is the one trained on **one** hole.

---

## A correction

Read at step 40 — the per-family freeze taken while the game arms were still
training — the game family was **flat on every panel**. Re-read at step 70 after
every arm finished, it **rises**: held-out game cell 0.394 → 0.515, Kuhn capture
0.061 → 0.498. The step-40 reading was an undertraining artifact and is
superseded. Do not cite it.

---

## Incidental finding: the audit arm can be gamed by silence

`scale-synth-n1-nohole` **learned to defeat the consequence wrapper by emitting
unparseable output.**

| step | 21 | 28 | 35 | 42+ |
|---|---|---|---|---|
| `train/invalid_rate` | 0.04 | 0.68 | 0.93 | 1.00 |
| `train/reward` | −0.01 | +0.07 | −0.05 | +0.33 … +0.58 |

Reward *rises* as parseability collapses. An unparseable action is never
detected as an exploit, so it escapes the audit penalty while still collecting
the default payoff. That is a degenerate solution to `ConsequenceWrapper`
itself, not a training glitch — and it means the arm is unusable (zero valid
held-out episodes), costing the synthetic control at n=1.

**This deserves its own experiment.** If a `nohole` arm can escape the audit by
refusing to act, then every audit control in the atlas is partly measuring "did
the policy find the degenerate exit", not only "did consequences suppress the
hole". `scale-synth-n8-hole` drifts the same way (invalid 0.03 → 0.23 by step
56, 0.41 at eval), so this is not a one-arm curiosity.

---

## What bounds all of the above

- **One training seed.** Error bars on the figures are episode-level bootstrap.
  They say how well a checkpoint was measured, not how much another seed would
  move. The plan gates seeds 2–3 on pass 1 rising; pass 1 does rise, so that
  gate is now open.
- **Four points cannot fit an exponent.** Nothing is fitted; read the shape.
- **The base is Qwen3.8-27B**, not the 3.6 of `eval_suite_transfer_27b.png`. The
  `base` arm of this ladder is the only valid comparison point — with the single
  noted exception of the MACHIAVELLI +12.8 ≈ +12.4 correspondence, which is
  called a replication precisely because the base models differ.
- **The synthetic corpus was pruned mid-run** to the five domains that isolate a
  genuine social-shortcut hole; 8 of the 10 held-out synthetic domains used here
  were dropped as permitted-discretion rounding/padding. The dose-response
  survives on the two survivors (0.300 → 0.938), which is why that row is given
  both ways. The synthetic scaling family is **retired going forward** — too few
  genuine domains remain to scale their count 1→8.
- **BROKEN-gated points.** Any cell whose invalid rate exceeds 0.25
  (check_suite's threshold) is drawn hollow and excluded from verdicts: its
  denominator is selected by whether the model emitted a parseable action, and
  arms differ ~10× in how much they filter. Affected: `synth-n8-hole` (0.41),
  `game-n2-hole` (0.34).
- **Tier B is incomplete for 4 synthetic arms** (MACHIAVELLI + AgentMisalignment
  missing). Their jobs were packed 5-to-a-node; one died in the Rust tokenizer
  with `ThreadPoolBuildError … EAGAIN` and another hung 9.75 h until the wall
  clock killed it. Cause was node packing, not the arms.
  `hole_exp/rerun_tierb_step70.sh` re-runs them one job per node; not executed.
- **hack-verifiable was never run** on the ladder (~100 min/arm at the only
  setting with adequate power; at 10 episodes it is the underpowered config that
  previously gave z=1.00 where 60 episodes gave z=3.76).

## Suggested next steps, in order

1. **Seeds 2–3.** Pass 1 rose, which is the gate the plan set. Without them, no
   statement here about #envs is more than one checkpoint versus another.
2. **The silence exploit.** Whether audit arms across the atlas have been partly
   scoring a degenerate exit is a correctness question about the control, and it
   is upstream of every hole/no-hole number the project has produced.
3. **Finish Tier B** for the 4 synthetic arms (one job per node).
4. **A second rung ordering**, which the plan asked for and this run could not
   fit — the current ordering is stratified rather than randomised.
