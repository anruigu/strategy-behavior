Try 2 things, see if it fixes the regmix setup in /workspace/allie/strategy-behavior/hole_exp/train_mixed.py with --regime-mix 0.5

(try with both thinking on / off)

1. Auxiliary disposition-prediction head (cheapest, do first). Add a supervised loss predicting opponent disposition from the observable history. It forces the representation to encode the cue cheaply, so the policy's action distribution has something to latch onto — it directly attacks the "cue–action covariance never bootstraps" problem. Low cost, and it doubles as your identifiability diagnostic.

2. Cue-conditioned baseline (fixes the GRPO structural blindness). The root pathology is that a pure per-group mean baseline is regime-level-absorbing and cue-blind. Move to a learned critic V(observable-history) — PPO-style, or GRPO with a learned baseline that ingests the observable prefix — so advantage is computed relative to a cue-aware expectation. Now "given what I could observe, did I beat the cue-conditioned baseline" is the reinforced quantity. You keep your per-group flip for rollout sanity but stop letting the group mean eat the regime signal. An intermediate: cue-stratified leave-one-out baselines rather than raw group pooling.

get a metric that isolates cue-conditioning from marginal shift before you run anything. Your off-regime-drop is close but it moves for two different reasons. You want something like the exploit-rate gap between nerfed and punishing at matched decision points, or AUC of action against the observable cue — so that when a fix helps, you can tell it produced conditioning rather than just relocating the marginal.

---

# Wired up (2026-08-23)

## The metric, first — `cue/cci` (`cue_metrics.py`)

`regime/discrimination` is the pooled exploit-rate gap, and it moves for two
reasons that cannot be separated after the fact:

- **conditioning** — the policy reads the counterpart and acts differently at
  the same point in the same game. The thing regmix exists to produce.
- **composition** — the two regimes do not offer the same decision points. A
  punishing counterpart retaliates as soon as it is exploited, which *truncates
  the scored set*: later rounds stop being conditional and stop counting. On
  `ipd` the always-exploit reference scores one decision where the honest one
  scores nine. So the two arms average over different denominators and the
  pooled gap moves whenever the marginal moves, conditioning or not.

`cci` is the same contrast at **matched decision points**. A stratum is
`(env, decision index t, count of the learner's own prior exploits k)` —
everything in it is the same game at the same round with the same self-history,
and the only thing that differs across the two regimes inside it is what the
*counterpart* did, which is exactly the cue. The headline is the
Mantel–Haenszel weighted mean of the within-stratum gaps, i.e. the pooled gap
direct-standardised to a common decision-point distribution.

On a simulation with conditioning set to **exactly zero** and only the
truncation present:

    regime/discrimination  = -0.189      <- pure artefact
    cue/cci                = -0.001 +- 0.013

Three companions, because one number is still readable the wrong way:

| key | what it is for |
|---|---|
| `cue/lor` | MH **log odds ratio** over the same strata. A risk difference is mechanically compressed near 0 and 1, so an arm exploiting 3% of the time cannot post a big `cci` however well it discriminates; the odds ratio is not compressed. |
| `cue/blind_gap` | the gap at the **first** decision, before the counterpart has responded to anything. The **placebo** — `cci` up with `blind_gap` flat is conditioning; both up is a prior shift (or a cell whose opening text leaks the arm, also worth knowing). |
| `cue/informed_gap` | restricted to decisions after the learner has already taken something, so the counterpart has had a chance to punish. Upper bound on what the cue can buy. |

Logged automatically in every mixed-regime run, per-env as well as pooled,
`{}` on a single-regime batch. Diagnostic only — never in the gradient, same
rule as `exploit_rate` and `capture`. The live `cue/cci_se` is decision-level
and therefore optimistic (decisions within an episode are correlated);
`bootstrap_cci` resamples whole **episodes** and is what a claim should quote.

## Fix 1 — auxiliary disposition head (`aux_probe.py`, `--aux-weight W`)

A second, cross-entropy gradient into the same `optim_step`: from the
observable history, answer in one word whether this counterpart `PUNISHES` or
`PERMITS`. The label is the regime the episode actually ran under, which the
trainer knows and the policy does not.

It is a "head" only loosely — Tinker trains a LoRA over a frozen architecture,
so the model's own LM head does the classifying and the logit is the likelihood
of one of two answer words. That is arguably the right shape anyway: the probe
reads out of exactly the representation the policy acts from, which a bolted-on
classifier would not.

- Probes are drawn from decisions **after the first** — at the opening decision
  the counterpart has not responded yet, so a probe there trains the prior
  rather than the cue. Same boundary `cue/blind_gap` isolates.
- Rendered with **thinking off even in the think-on arms**: the Qwen template
  pre-opens `<think>` under `add_generation_prompt`, so the label would land
  inside a reasoning block; holding the probe format fixed is also what makes
  `aux/probe_acc` comparable across the pair.
- The probe is never shown to the policy at rollout time and never reaches an
  environment, so it cannot become the "detect that you are being watched" cue
  that the explicit monitoring flag was rejected for in MIXED-REGIME.md.

**It doubles as the identifiability diagnostic.** `aux/probe_acc` is a two-way
forced choice (score the same prompt against both labels, take the likelier),
two forward passes, no backward. It runs on the **control arm too**: a control
sitting at chance means the cue is unreadable in these cells and no trainer
change was ever going to produce conditioning — a conclusion about the roster,
not the trainer, and one worth being able to reach.

> **Correction, mid-flight.** The first cut gated probe *construction* on
> `--aux-weight > 0`, so the control arm logged nothing — the diagnostic was
> missing from precisely the arm it was for. Fixed (construction now follows
> `--aux-probe-every`; only the `aux` arm's datums reach a backward pass, so no
> gradient changed). The three think-off jobs had already loaded the old module
> and keep the gap; `probe_checkpoints.py` recovers it from their checkpoints,
> with fixed seeds per env, both regimes, and the held-out `ultimatum` included
> — which the training-time probe cannot do, since the loop never rolls it.

## Fix 2 — cue-conditioned baseline (`cue_critic.py`, `--regime-draw rollout --advantage critic`)

The pathology stated as a property of the baseline: the disposition is drawn
**once per GRPO group**, so the whole hole-vs-nohole difference lands in
`mean(group)` and is subtracted away before any token sees it. The advantage is
cue-blind by construction — no gradient anywhere in the run says "this action
was good *because of who you were facing*", so the cue–action covariance never
builds. Two parts, both required:

1. **`--regime-draw rollout`** — put both counterparts in one group at the same
   `env_seed`, by a *balanced* deterministic split rather than a coin per
   rollout (at group-size 6 a coin leaves ~3% of groups single-regime, and a
   group with no contrast is exactly the case the critic has nothing to do).
   This knowingly gives up the invariant `train_mixed` was written with — every
   rollout in a group meeting the same opponent. That invariant *is* the
   absorption.
2. **`--advantage critic`** — `V(h_t)` fit on the observable prefix at each
   decision, then `A_t = (R - V(h_t))` standardised within the group. The
   reinforced quantity becomes "given what I could observe here, did I beat the
   cue-conditioned expectation". Where the cue is not yet readable `V` collapses
   to the marginal and the scheme degrades exactly to a pooled baseline — the
   correct behaviour, not a failure. The group mean/sd stay on top for **scale
   only** (payoff scales differ by an order of magnitude across the roster).

The critic is a hashed bag-of-ngrams ridge over the prefix text, Adagrad,
4096 features. Not because that is the ideal critic but because it is the honest
one available: there is no value head to add to a Tinker LoRA and no way to read
hidden states out. It reads only what the policy read, and it degenerates
gracefully to predicting the mean when the text carries no signal. **Prequential
— predicts with the weights it had at the start of the step, learns from that
step only afterwards**, so it cannot memorise the batch it is scoring. Saved
next to each checkpoint (`critic_stepNNNN.json`), because a run resumed with a
fresh critic baselines against zero for its first steps.

Both fixes are **off by default**, so every number already on disk reproduces
bit-for-bit. Verified: a control dry run adds only the `cue/*` keys.

## The wave (`sbatch_cuecond.sh`) — 3 arms x thinking on/off

    ctl   --regime-mix 0.5, exactly as it runs today
    aux   + --aux-weight 0.5
    cue   + --regime-draw rollout --advantage critic

`ctl` is **not** redundant with `mixed_disp_regmix_d1_s0/s1`: those are Qwen3.6
at 384 tokens, this wave is Qwen3.8 at 1024, and the base-model screen puts the
pre-training discrimination of those two models on opposite sides of zero.
Without a model-matched control, movement in the treatment arms is attributable
to the model change.

Roster and sampling are `sbatch_thinking.sh`'s unchanged — seven opponent-swap
cells, `ultimatum` held out, Qwen3.8-27B, t0.7 / top_p 0.9 / 1024 tokens,
`reasoning_effort=low` on the think arms, 90 steps, 14 groups x 6.

Thinking is crossed in because the base screen found it is the only condition in
which Qwen discriminates at all before training (+0.135 [+0.056, +0.215] against
two nulls). If that is the binding constraint, both fixes move only the think-on
arms — a different conclusion from either fix working.

Readout: `cue_readout.py` (tail-averaged CCI / DISC / blind / rate / probe per
arm). The training signal is far too noisy to read a single step — MIXED-REGIME
measured per-step SE ~0.13 — so the table is a screen for which checkpoints are
worth replaying through the battery, not the claim.

## In flight (checked at step ~15/90, 2h in)

Nothing separates the arms yet, which is what step 15 should look like:

| arm | steps | CCI (last 12) | DISC | rate | invalid |
|---|---|---|---|---|---|
| ctl | 14 | +0.000 ±0.021 | −0.013 ±0.034 | 0.289 | 0.007 |
| aux | 17 | +0.001 ±0.023 | +0.008 ±0.033 | 0.300 | 0.006 |
| cue | 18 | +0.004 ±0.008 | +0.010 ±0.020 | 0.320 | 0.002 |

Health is fine in all three — reward flat around +0.8, invalid under 1%, no
sign of the aux gradient costing the policy anything. The aux objective itself
is being learned: `auxnll` 0.376 → 0.173 over 16 steps.

**The `cue` arm's error bar is ~2.5x tighter** (±0.008 vs ±0.021/±0.023) at the
same number of steps. That is the balanced within-group regime split, not a
result: every group now contributes a paired hole/nohole contrast at one
`env_seed` instead of the contrast existing only between groups. Worth having
even if the arm produces no conditioning.

### Two instrumentation defects found while watching, both fixed

**`cue/blind_gap` had the confound the module exists to remove.** It read −0.05
to −0.09 in all three arms where a placebo should sit at zero. Two causes, and
neither is a leak:

- It was computed *unstratified*. At the opening decision each episode
  contributes exactly one row, so under a per-GROUP regime draw the two pools
  hold different mixtures of envs — and the roster's base exploit rates differ
  enough across cells that the mixture alone moves it. Constructed case: same
  per-env rate in both regimes, `blind_gap` = +0.360, per-env `blind_cci` =
  +0.000. Added `cue/blind_cci` as a **new** key rather than redefining
  `blind_gap`, because runs in flight are already logging the old one and a
  series that changes meaning halfway is worse than one with a caveat.
- All three arms share `--seed 0`, so `env_seed = seed*100003 + step*97 + g` is
  identical across them: they roll the same scenarios in the same order and
  their blind gaps are correlated draws, not three independent confirmations.

**Checked directly that the opening observation cannot leak the regime.** Each
cell played under both arms with a fixed scripted policy, diffing the text at
the learner's first decision: **byte-identical in 8/8 seeds in all seven
cells**. So the placebo assumption holds — before the counterpart responds there
is genuinely nothing to read — and any non-zero `blind` is mixture or noise.

`cue_readout.py` also mis-parsed every arm name as `?` (it matched the tag at
the end of the label, which is `_s0`). Fixed.

### The arms are not equally powered, and it is structural

A `CCI=-0.200 +- 0.000` on the aux arm turned out to be the visible end of
something worth knowing. Usable decisions per step, measured over the first ~20:

| arm | usable steps | decisions/step (median, min–max) |
|---|---|---|
| ctl | 17/17 | 180 (81–296) |
| aux | 19/21 | 174 (**0**–319) |
| cue | 22/22 | **431** (373–501) |

A stratum contributes only if **both** regimes are in it. Under the per-GROUP
draw each env gets two groups whose regimes are drawn independently, so about
half the envs are single-regime in any step and contribute nothing at all —
occasionally none of them do, and the step yields no estimate. The per-rollout
balanced split puts both counterparts in every group, so every env contributes
every step.

This is **power, not bias** — Mantel–Haenszel is built for sparse strata and
stays consistent — and it does not leak into the readout: `cue_readout` takes
its SE from the spread ACROSS steps, not from `cue/cci_se`, so the zero-SE steps
are cosmetic. On a 40-step tail the arm SEs land around ±0.011 (ctl/aux) and
±0.004 (cue), against effect sizes of +0.2 to +0.27 in MIXED-REGIME. Adequate,
and worth stating rather than discovering later.

**`decisions.jsonl`** now records the per-decision rows (`env, regime, t, k, y,
episode`) each step, so stratification can be redone offline over any window —
pooling decisions across steps is the right answer to sparse strata, and it
cannot be done from the summary alone. Additive: the headline `cue/cci` is
computed exactly as before, so the think-off and think-on arms stay comparable.
The three in-flight think-off arms predate the file.

---

# The wave died of length, not of anything it was testing (2026-08-24)

**All three think-off arms suffered a format collapse, the CONTROL worst of
all.** First step at which the 5-step mean invalid rate crosses each threshold:

| arm | >0.05 | >0.15 | >0.40 | final |
|---|---|---|---|---|
| ctl | 57 | 66 | 70 | **0.915** |
| aux | 39 | 77 | — | 0.141 |
| cue | 34 | 47 | 52 | 0.780 |

This kills an earlier read of mine that is worth recording as wrong: I saw the
drift in the two treatment arms first, the control still flat at 0.006, and
proposed that the cue-conditioned baseline was absorbing the `INVALID_COST`
charge — once garbage is in the prefix, `V(h_t)` drops, the residual goes to ~0
and later turns stop being charged. Plausible, and refuted: the control has no
critic and collapsed hardest. It was only ~25 steps behind.

**It is not a reward hack.** Reward FELL with it (ctl 0.965 → 0.313) and
`core.INVALID_COST` was charging throughout. Whatever drove this was beating the
reward, not exploiting it.

**It is a length runaway.** Mean sampled action length per checkpoint, from the
trace dumps, against that checkpoint's invalid rate:

| arm | step 0 | 22 | 45 | 68 |
|---|---|---|---|---|
| ctl | 74 ch | 25 | 28 | **166** (p90 467), inv 0.288 |
| aux | 81 | 22 | 13 | 24, inv 0.000 |
| cue | 91 | 95 | **288** (p90 457), inv 0.163 | 157 |

The policy first compresses to the bare action (p90 = 11 characters, i.e.
`[Cooperate]`) and then explodes into prose that never emits a bracketed token:

> `'Hello Player 0. Welcome to the game. This is Round 1 of 10... the standard
> rational solution via backward induction suggests defection is dominant...'`
> — 1815 characters, no action

with role confusion alongside it (`'Player 0:'`, `'(no comment)'`). Qwen3.8-27B
rambling past its own action is already documented for this model in
`tinker_actor`; what is new is RL amplifying rather than suppressing it.

**Mechanism.** The advantage is constant across a turn's tokens, so the turn's
pull on the gradient is `advantage * n_tokens`. A 2000-character ramble counts
~250x an eight-character `[Defect]`. Verbose rollouts own the update whatever
their sign, and the drift compounds. The unit the advantage was estimated on is
the EPISODE, not the token.

**Fix: `--length-normalise`** (`train_hole.build_data(token_norm=...)`).
Rescales each turn's advantage by `batch mean length / its own length`, so every
TURN contributes equally. Scaling by the batch mean rather than dividing by the
length alone is deliberate: the latter also shrinks the whole batch's gradient
by ~1/L and silently changes the effective learning rate. Off by default — it
changes the objective, and runs either side of it must not be pooled.

Also now logged unconditionally: `train/sampled_tokens_mean` and `_p90`. The
p90 moved from 11 to 467 while `invalid_rate` was still ~0; the length series
would have called this ~20 steps before the invalid rate did.

**Unplanned side-finding: the aux arm was the most format-stable.** It never
rambles at any dumped checkpoint and ended at 0.141 against 0.78 and 0.915. A
cross-entropy loss on a one-word answer plausibly anchors the output format.
Worth a controlled check before it is believed.

## What the wave can and cannot say

Usable window is steps 10–33, where every arm is under 0.05 invalid:

| arm | CCI | DISC | blind |
|---|---|---|---|
| ctl | +0.026 ±0.025 | +0.004 ±0.017 | −0.068 ±0.030 |
| aux | +0.003 ±0.021 | −0.007 ±0.022 | −0.092 ±0.030 |
| cue | +0.019 ±0.006 | +0.054 ±0.015 | **+0.001 ±0.018** |

**Neither fix had produced conditioning by step 33.** That is a third of
training against a signal MIXED-REGIME only resolved at the endpoint, so it is
"no effect yet", not "no effect". The question is unanswered, not answered
negatively.

Two things the window does establish:

- The `cue` arm's placebo is clean (+0.001) where ctl and aux read −0.07 to
  −0.09, confirming that the balanced within-group split removes the
  env-composition artefact from `blind_gap` — the same defect `cue/blind_cci`
  now fixes for the other arms.
- The `cue` arm's CCI standard error is ~4x tighter at equal step count.

## Identifiability: the cue IS readable, and probably always was

`probe_checkpoints.py` on the think-off CONTROL (no aux gradient anywhere in
that run), 4 seeds x 8 envs x 2 regimes per checkpoint:

| step | pooled probe acc | held-out `ultimatum` |
|---|---|---|
| 0 (untrained) | 0.661 ±0.060 | 0.62 |
| 22 | 0.661 ±0.060 | 0.50 |
| 45 | 0.787 ±0.052 | 0.75 |

Chance is 0.500. The live probe on the three think-on arms agrees: 0.65 (ctl),
0.67–0.69 (cue), 0.65–0.70 (aux) — five measurements clustered at ~0.67 across
both thinking settings, with and without the aux loss, trained and untrained.

**This substantially weakens the aux fix's premise.** Its rationale was that the
cue never enters the representation because nothing rewards putting it there.
The untrained base model reads it at 0.661. Whatever is blocking conditioning is
downstream of the representation.

**Whether RL raises readability is unresolved.** 0.661 → 0.787 is z = 1.57,
p ≈ 0.12 on 61 probes — suggestive, not a result, and an earlier note in this log
claiming readability was *flat* was written off the first two checkpoints and was
equally unsupported. Worth resolving at `--seeds 24` (~370 probes/checkpoint,
SE ~0.021), because if plain RL DOES take readability to 0.79 while CCI sits at
+0.026 ±0.025, the bottleneck is provably between representation and action —
which is the cue-conditioned baseline's target, not the aux head's.

Per-env numbers at 4 seeds are ~8 probes each (SE ~0.18) and shuffle between
checkpoints (`winasmuch` 0.88 → 0.50, `trust` 0.50 → 0.38); treat them as noise.
The only stable ones are `public_goods` (1.00, 1.00) and `dond` (0.50, 0.50).

## Decision

Think-on arms (`cc-ctl-on`, `cc-aux-on`, `cc-cue-on`) left RUNNING, to be
re-read at step 35 — the depth at which the think-off arms were still clean.
Their early CCI is higher than the think-off arms ever reached (+0.155, +0.108,
+0.088 at steps 8–11), which is the direction the base-model screen predicted,
but far too early to weigh. `cc-ctl-off` was cancelled at step 80 (0.915
invalid, exploit collapsed to 0.042); it was measuring nothing and was blocking
its chained think arm.

Relaunch, when it happens, gets `--length-normalise`.

## Step-35 decision point (2026-08-24)

All six arms at matched depth, steps 10–35:

| arm | CCI | DISC | invalid | probe | last step |
|---|---|---|---|---|---|
| ctl-on | −0.037 ±0.037 | +0.014 ±0.050 | 0.008 | 0.551 | 20 |
| aux-on | +0.034 ±0.018 | +0.021 ±0.034 | 0.014 | 0.653 | 33 |
| cue-on | +0.021 ±0.007 | +0.022 ±0.013 | 0.007 | 0.667 | 35 |
| ctl-off | +0.021 ±0.025 | −0.001 ±0.017 | 0.006 | — | 80 |
| aux-off | +0.002 ±0.020 | −0.018 ±0.023 | 0.012 | 0.683 | 89 |
| cue-off | +0.018 ±0.006 | +0.052 ±0.014 | 0.029 | — | 89 |

**Thinking does not change the answer.** Every arm is within ±0.04 of zero and
none is distinguishable from any other. The hypothesis that justified crossing
thinking in — that Qwen cannot discriminate without it, so RL had nothing to
sharpen — is unsupported at this depth. (`ctl-on` lags 15 steps; its number
rests on 9.)

**The think arms are NOT collapsing, which was not predicted.** 0.007–0.014
invalid through step 35, where `cue-off` was at 0.029 and 10 steps from its
blowup; `aux-on` hit exactly 0.000 at step 35. Likely mechanism: thinking gives
the ramble somewhere to go. The verbosity lands inside `<think>`, which
`split_think` strips before the env sees the action, so the ANSWER stays short.
If that holds it is a second mitigation for the length runaway, and unlike
`--close-bracket` it composes with everything.

**Decision: run all three to 90.** They are healthy and on track to produce the
complete uncontaminated three-arm comparison the think-off wave could not.

## Not run, and why

- **aux + cue combined.** Implemented and smoke-tested together; held back so
  the two fixes are attributable separately first.
- **`--regime-draw rollout` with the plain group mean.** The ablation that
  separates "the per-rollout draw did it" from "the critic did it". Worth
  running if `cue` moves.
- **Second seed.** Six arms already exceed the free nodes; seeds come after the
  three-way comparison says which arm is worth replicating.