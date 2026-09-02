# 0901 overnight — status

Two independent things ran overnight. Both collapsed, in the same way, for
what looks like the same underlying reason.

---

## 1. Cold start / zero floor: NOT RESOLVED

Short answer: **no**. Nothing moved a cell off zero. What moved was cells that
were already sampling the behaviour, and one of those was only sampling it
because a token-budget bug got fixed.

The wave ran four seeds, seven cells, group 16, lr 3e-5, T=1.0. Each seed is
truncated at the last step whose mean invalid rate is still under 0.08, because
after that point the numbers are the referee's fallback and not the policy.
Pooled across seeds, first half vs second half:

| cell | base rate | mean Δ | seeds agreeing | verdict |
|---|---:|---:|---|---|
| gen_sovereign_vaults | 0.30 | **+0.123** | 4/4 `++++` | real, but AMPLIFICATION |
| gen_frontline_depot | 0.09 | **+0.044** | 4/4 `++++` | real, but amplification |
| ref_commons | 0.31 | +0.025 | 3/4 `+++-` | weak |
| ref_estate | 0.013 | +0.008 | 4/4 `++++` | see below |
| gen_antiquities | 0.001 | +0.002 | 3/4 `-+++` | noise |
| ref_auction | 0.003 | −0.000 | 2/4 `+-+-` | noise |
| **gen_quiet_sonar** | **0.000** | **+0.000** | 0/4 `----` | **dead flat** |

The three true zero-floor cells are `gen_quiet_sonar`, `ref_auction` and
`gen_antiquities`. None of them moved. `gen_quiet_sonar` produced *exactly*
0.000 on every step of every seed, against a prompted ceiling of 0.893 — so the
behaviour is fully reachable when named and is never once sampled without being
named.

`ref_estate` is the one ambiguous case and worth flagging rather than rounding
off. All four seeds agree on the sign, 0.013 → 0.021, which is not what noise
usually looks like. But it is ~0.8 percentage points against a 0.607 ceiling and
a +431.65 payoff, so if it is real it is real and irrelevant at the same time.
Worth one dedicated longer run before believing it.

**What this rules out.** Cold start survived every knob tried: prompt ladder
(win/winmax/hint), group size (16 vs 32, null), temperature (1.0/1.5/2.0,
actively harmful), token budget (512→4096, fixed a different bug), and learning
rate (1e-5/3e-5/1e-4). The behaviour is reachable — hint rates are 0.39–0.89 on
exactly these cells — so this is an exploration problem, not a capability one,
and none of the standard exploration knobs touch it.

## Why the wave stopped early

All four seeds started collapsing at essentially the same step:

| seed | steps run | first bad step | invalid at end |
|---|---:|---:|---:|
| 0 | 26 | 15 | 0.254 |
| 1 | 19 | 16 | 0.151 |
| 2 | 17 | 15 | 0.131 |
| 3 | 15 (running) | — | 0.030 |

The watcher killed 0, 1 and 2. Seed 3 is behind (8 samplers instead of 9–10) and
is still clean at step 15, i.e. right at the edge. This is the failure I flagged
when launching: `lora_B` grows ~0.08/step and the 1e-4 probe fell apart at
magnitude ~2.5, so 3e-5 hits the same place around step 15–20. **The collapse
threshold is a weight magnitude, not a learning rate.** Lowering lr buys steps,
not safety; what is needed is a decay schedule, an early stop, or a KL/entropy
term that the current `importance_sampling` loss does not have.

Checkpoints exist every 5 steps, so the usable policies are steps 10–15 of each
seed.

---

## 2. The simulated-opponent runs (think4): ALL FOUR COLLAPSED

These are the `train_mixed.py` jobs against scripted opponents —
`--nohole-shape tft` (tit-for-tat) and `--nohole-shape grim` (grim trigger),
seeds 0 and 1 each, on ipd / public_goods / dond / trust / ipd3 / staghunt /
winasmuch. I did not touch them; this is a read of their logs.

All four show the same length-runaway:

| run | step 0 | ~step 25 | ~step 50 | now | last step invalid<0.10 |
|---|---|---|---|---|---:|
| s0-tft | inv 0.029 / exp 0.199 | 0.007 / 0.116 | 0.030 / 0.044 | **0.681 / 0.004** @87 | 56 |
| s1-tft | 0.042 / 0.219 | 0.002 / 0.056 | 0.000 / 0.014 | **0.825 / 0.000** @124 | 97 |
| s0-grim | 0.044 / 0.323 | 0.004 / 0.051 | 0.135 / 0.049 | **0.857 / 0.000** @96 | 56 |
| s1-grim | 0.046 / 0.238 | 0.002 / 0.078 | 0.091 / 0.022 | **0.677 / 0.000** @77 | 55 |

Truncation tracks invalid exactly (0.04 → 0.87–0.96), and step time has gone
from 100–300s to 2000–5400s — a 10–20x slowdown, which is the same fact seen
from the other side: the policy is generating until it hits the 1024-token cap
on nearly every turn. Reward `R` holds around +0.4 to +0.5 throughout, so the
reward curve alone looks survivable and says nothing about the fact that most
turns are no longer parseable.

The measured content is gone: `exploit` fell from 0.20–0.32 at step 0 to ~0.000,
and `capture` from 0.19–0.29 to ~0.03. Whatever these runs were meant to show
about behaviour against scripted opponents, they stopped showing it around
step 55–60.

**Rollback points**, all checkpointed: s0-tft step 56, s1-tft step 97,
s0-grim step 56, s1-grim step 55. Checkpoints are dense (every step is present
in `ckpt/tft-inf/` and `ckpt/grim-inf/`), so any earlier step is also available.

There is an `archive-runaway-0830/` in the think4 tree, so this has happened
before on 2026-08-30 and has now recurred.

---

## The common thread

Both collapses are length runaway, and both were invisible in the headline
metric. In the referee wave the exploit rate *rose* while the policy broke,
because the referee scores an unparseable reply with its own fallback. In the
think4 runs the reward stayed flat at +0.45 while 68–86% of turns stopped
parsing. Neither curve looks wrong unless validity is plotted next to it, and
`invalid_rate` did not exist in the referee metrics until 2026-09-01.

The single highest-value change available is a length/validity guard in the
training loop itself rather than in a watcher bolted on outside it: stop, decay
or penalise when the truncation rate crosses a threshold. Every result this
project has had to retract has been this same artefact.
