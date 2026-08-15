# Transfer-eval summary: reasoning vs. behavior across four training arms

Does RL on zero-sum games (SPIRAL self-play) move a model's honesty / disposition,
not just its reasoning? This table consolidates the four eval axes across the base
model and three trained arms. All arms start from `Qwen3-4B-Base`.

## Headline table

| Arm | Reasoning ↑ | Behavior (TRAIT Mach) | MASK dishonest % ↓ | Reward hacking % ↓ |
|---|---:|---:|---:|---:|
| **Base Qwen3-4B-Base** | 30.0 | 23.6 | 19.3 | 28.7 |
| **MATH-only RL** (step 64) | 40.5 | 24.5 | 28.4 | 17.6 |
| **PigDice** (step 192) | 36.1 | 23.2 | 28.5 | 16.1 |
| **KuhnPoker** (step 400) | 38.1 | 24.7 | 26.7 | 16.4 |

Arrows show the "good" direction. Higher reasoning is better; lower MASK-dishonesty
and lower reward-hacking are better; TRAIT Machiavellianism is shown as-is (the
facet the methodology flags for disposition drift).

> **What was filled in.** You had Reasoning / MASK / Reward-hacking for three rows.
> I filled the whole **PigDice** row, the whole **Behavior** column, and verified
> every pre-existing cell against the committed data. The two cells you had to
> guess at — PigDice MASK (**28.5**) and every Behavior value — are derived below.

## What each column is

| Column | Eval | Metric | n |
|---|---|---|---|
| Reasoning | `math-evaluation-harness` (SPIRAL's battery) | mean accuracy over 6 math benchmarks | 6 datasets |
| Behavior | [TRAIT](https://arxiv.org/abs/2406.14703) | Big-Five + Dark-Triad personality (Machiavellianism shown) | 2,000 items |
| MASK dishonest % | [MASK](https://arxiv.org/abs/2503.03750) | response-weighted pooled dishonest rate, `= 100 − honesty` | 1,000 rows |
| Reward hacking % | [School of Reward Hacks](https://arxiv.org/abs/2508.17511) | fraction of answers judged to game the stated metric | 1,073 rows |

Judge for MASK and reward-hacking is `openai/gpt-4.1` via OpenRouter, 0% judge loss.

## The "MATH" dataset — two distinct things called MATH here

The word "MATH" shows up in two places in this study, and they are not the same:

**1. The Reasoning column is a 6-benchmark math/reasoning suite** (this is what
"MATH" means as an *eval*). The score is the mean accuracy over:

`math500`, `AIME24`, `AIME25`, `OlympiadBench`, `AMC23`, `Minerva Math`

run through SPIRAL's `math-evaluation-harness`. It is the exact benchmark set the
SPIRAL paper uses to claim "self-play transfers reasoning," which is why it is the
capability axis here. Base scores 30.0 on it; every trained arm beats base
(36–40), i.e. **all three RL arms improve reasoning**, matching SPIRAL's claim.

Per-benchmark, base → MATH-RL(step 64):

| bench | base | MATH-RL s64 |
|---|---:|---:|
| math500 | 64.4 | 78.4 |
| AIME24 | 6.7 | 13.3 |
| AIME25 | 10.0 | 13.3 |
| OlympiadBench | 33.2 | 40.9 |
| AMC23 | 42.5 | 57.5 |
| Minerva Math | 23.2 | 39.7 |
| **mean** | **30.0** | **40.5** |

**2. The "MATH-only RL" *arm* is a training control** (this is what "MATH" means as
a *checkpoint*). It is single-agent RLVR — `oat.experiment.run_math_rl` on the MATH
training split (~7,498 prompts × 7 epochs / batch 128 ≈ 407 steps), on
`Qwen3-4B-Base`. It exists to answer: *does **any** RL move honesty/disposition, or
only self-play against a manipulable opponent?* The `s64` you wrote is the
**step-64 checkpoint** of that run. (The arm peaks around step 192–256 then gives
back ~half its reasoning gain by step 407, so step 64 is an early, still-rising
checkpoint, not the best one.)

Note on the other row labels: `MATH-only` genuinely is the step-64 checkpoint, but
the **KuhnPoker** numbers you pasted (reasoning 38.1, hack 16.4) are the
**step-400** checkpoint, and **PigDice** is **step-192** — those are the checkpoints
actually run through the MASK + reward-hacking batteries (files `rh-kuhn400`,
`rh-pig192`), so I've labeled the rows by their true step rather than as `s64`.

## Behavior (TRAIT) — full breakdown

The Behavior column above is TRAIT Machiavellianism. The full 8-axis profile
(n=2,000 items per arm) barely moves across arms — the disposition signal is
essentially flat, in contrast to the MASK signal:

| Axis | Base | MATH-RL s64 | PigDice s192 | KuhnPoker s400 |
|---|---:|---:|---:|---:|
| Openness | 72.8 | 70.2 | 71.6 | 74.0 |
| Conscientiousness | 96.8 | 97.2 | 95.6 | 96.8 |
| Extraversion | 43.6 | 44.4 | 46.0 | 45.8 |
| Agreeableness | 91.6 | 92.4 | 92.8 | 91.6 |
| Neuroticism | 30.8 | 30.4 | 30.8 | 28.3 |
| **Machiavellianism** | **23.6** | **24.5** | **23.2** | **24.7** |
| **Narcissism** | 13.2 | 13.6 | 14.0 | 16.0 |
| **Psychopathy** | 2.4 | 2.4 | 2.4 | 2.8 |

Dark-Triad (Mach / Narc / Psych) shifts are within ~1–3 points everywhere — no
arm shows a meaningful disposition change.

## How the MASK dishonest % is computed (and how PigDice was filled)

MASK dishonest % is the **response-weighted pooled** rate: for each of the six
archetypes, take `unhonest_1` (= `100 − honesty`) and weight by that archetype's
`total_responses`, then pool over all 1,000 rows. This is *not* the same as
`100 − (simple mean of the six honesty scores)` — the archetypes have very
different row counts (274 for `provided_facts` vs. 96 for `statistics`), so the
pooled number sits below the naive complement.

Reconstructing the pooled rate from the committed per-archetype honesty scores
reproduces your existing numbers exactly (base 19.3, MATH-RL 28.4, KuhnPoker-400
26.7), which is how I derived the missing cell:

| Arm | pooled dishonest % | mean honesty |
|---|---:|---:|
| Base | 19.3 | 80.6 |
| MATH-RL s64 | 28.4 | 70.3 |
| **PigDice s192** | **28.5** | **70.8** |
| KuhnPoker s400 | 26.7 | 72.5 |

## Reading the results

- **Reasoning ↑ on every RL arm** (30.0 → 36–40). Self-play *and* plain math-RL
  both transfer reasoning, as SPIRAL predicts.
- **MASK honesty ↓ on every RL arm** (dishonest 19.3 → 27–29). But — and this is
  the key finding of the control — **PigDice drops honesty just as much (28.5) as
  the KuhnPoker bluffing arm (26.7)**, despite PigDice having *no communication
  channel and no deception affordance at all* (action space is only `[roll]` /
  `[hold]`, and this checkpoint is a degenerate over-roller). So whatever is moving
  MASK is **not** the model learning to deceive from strategic-interaction content;
  it looks like a generic consequence of RL fine-tuning on non-assistant
  transcripts (format / persona drift).
- **Honesty falls while capability rises**, so the "it's just downstream of getting
  worse at the task" mediation story is ruled out — the two move in opposite
  directions.
- **Reward hacking ↓ on every RL arm** (28.7 → 16–18) — the opposite direction from
  honesty. RL training reduces reward-gaming here.
- **Disposition (TRAIT) is flat** — the effect shows up as behavior-under-pressure
  (MASK), not as a self-reported trait shift.

## Caveats

- **Single seed, one eval pass per arm.** Per-archetype n is 96–274, so
  category-level numbers are noisy; arm means are better constrained.
- **Belief-elicitation confound.** Base `Qwen3-4B-Base` is not instruction-tuned
  and fails MASK belief elicitation more often than a trained checkpoint, which
  inflates its apparent honesty. Any *cross-arm* honesty claim should be read off
  the both-valid intersection in `compare_mask_arms.py`, not the naive pooled
  dishonest %. The pooled numbers here overstate the base→trained gap.
- **Checkpoint quality.** PigDice s192 is drawn from a *degenerate* (over-rolling)
  policy band, so it says what a broken Pig policy does to MASK, not a well-trained
  one. The `mathrl-step192` sibling checkpoint scores an anomalous 95.3 honesty and
  is treated as a judge/format artifact — do not build on it.

## Sources

- Reasoning: `spiral/evals/.../math-evaluation-harness/data/eval/<arm>/<ds>/*metrics*.json`
- MASK: `results/mask/*.all_results.json` + per-archetype honesty table in the
  `spiral-to-alignment-transfer` research log
- Reward hacking: `evals/reward-hacks/results/rh-*.json`
- TRAIT: `evals/trait/results/trait-*.json`
- Metric definitions: `evals/summarize_all.py`, `docs/methodology.md`
