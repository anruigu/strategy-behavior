# 0830 — what the endgame arms say so far

`think4` wave, re-run on local B300s instead of Tinker (see §7). Two kinds of
evidence here, and they should not be read the same way:

- **§1–§4, from training curves.** `tft` cells are live and past step 40; the
  four `grim` base/eg cells were **stopped at step 39–50** once their effect
  went flat (§2), so grim numbers are final and tft numbers will still move.
- **§5–§6, from two frozen-checkpoint eval sweeps** at a matched **step 35**,
  3 seeds per arm, 832 episodes. These do not depend on where the runs stop.
- **§7 combines both** for the hidden-horizon arm, and is the one place a
  within-checkpoint manipulation carries the argument rather than a
  between-seed contrast.
- **§10 is the grim-vs-tft comparison across every arm.** It is the only
  section built on the per-round action sequences rather than on scalar
  aggregates, and it supplies the mechanism behind §6.

For the first time there are **3 seeds per cell**, which changes the headline
result.

Companion: [`0826-endgame-by-opponent.md`](0826-endgame-by-opponent.md) (same
wave, one seed). Where the two disagree, this one supersedes it.

---

## 1. The sign flip does not survive more seeds

`0826` §4 reported that the hidden endgame penalty **flips sign with the
opponent** — suppressing late betrayal against tft (−0.057) and *increasing* it
against grim (+0.050) — and called that the wave's reason to exist. With three
seeds per cell it does not replicate.

Mean `train/endgame_rate` over steps ≥ 8, **between-seed** SE:

| | baseline | + endgame penalty | Δ |
|---|---|---|---|
| vs grim | 0.308 ± 0.006 | 0.264 ± 0.007 | **−0.044 ± 0.013** |
| vs tft | 0.348 ± 0.035 | 0.184 ± 0.054 | **−0.164 ± 0.063** |

n = 3 seeds per cell. The penalty **suppresses late betrayal against both
opponents** — same direction, different magnitude. The grim delta moved from
+0.050 (one seed) to −0.044 (three).

The error bar matters as much as the number. `0826` §4 flagged that its quoted
SE was *within-run across adjacent steps*, which bounds "is this step-to-step
noise" and not "is this the effect of the knob". These are between-seed, which
is the error bar the claim actually needs — and the claim does not survive it.

## 2. The effect is stable, not a transient

Δ(eg − base) by training window, so this is not an artefact of where the runs
happen to have stopped:

| window | vs grim | vs tft |
|---|---|---|
| steps 8–19 | −0.045 ± 0.030 | −0.056 ± 0.053 |
| steps 20–29 | −0.036 ± 0.020 | −0.166 ± 0.063 |
| steps 30–39 | −0.051 ± 0.064 | −0.228 ± 0.065 |
| steps 40–60 | −0.049 (n=1) | −0.256 ± 0.068 |

Against grim the effect is flat across every window: **that question is
answered, and more steps will not change it.** Against tft it is still growing
and has not plateaued, so longer runs will sharpen the magnitude but not the
direction.

**This table is why the four grim base/eg cells were killed on 08-30**, freeing
8 GPUs for the referee-hole sweep. State checkpoints carry `optim.pt`, so they
resume with optimiser state if wanted. The cost, stated plainly: the grim-vs-tft
contrast is now **fixed at ≤ step 50** while tft runs to 150, and grim's last
window was already n=1 (the s1 eg cell had not reached step 40). Flatness after
step 50 is now an assumption the data no longer tests.

## 3. Where the evidence is still thin: hidden horizon

**Superseded in part by §7.** When this was written `inf` had one usable seed
and no `grim/inf` at all. It now has two seeds per opponent, and §7 draws the
conclusions that this section said could not yet be drawn. What survives is the
*magnitude* caution, so the current state is worth being exact about:

| cell | seeds | deepest step | collapse onset (§4.1) | clean range |
|---|---|---|---|---|
| tft + inf | 2 | 120 (s1), 82 (s0) | 93, 58 | 8-92, 8-57 |
| grim + inf | 2 | 93 (s0), 74 (s1) | 60, 65 | 8-59, 8-64 |

**Updated 08-31: depth is no longer the constraint — the collapse is.** All four
`inf` seeds ran to step 74-120 and all four collapsed (§4.1), so each has a
clean range ending at its own onset. That is *more* pre-collapse depth than the
base/eg cells have (they were stopped at 34-50), which reverses the original
problem: `inf` is now the deepest arm in the wave.

The magnitude caution still stands, for a different reason. A Δ against §1 must
be read at a window both sides reach *and* both sides are pre-collapse in, which
is why §7.1 uses steps 8-34 — bounded above by the base/eg cells, not by `inf`.

## 4. The collapse is reproducible, and not specific to `inf`

`HANDOFF-think4.md` §3 recorded one collapse (`grim + inf`, steps ~51–77) and
left the cause open. The new **zero-consequence `hole` arm collapsed on both
seeds**, with the same signature:

| | s0 | s1 |
|---|---|---|
| max `invalid_rate` | 0.80 | 0.52 |
| reward at collapse | +1.27 → +0.50 | +1.34 → +0.93 |
| `sampled_tokens_p90` | 690 → 242 | 373 → 631 |

Same markers as §3: `think_truncated_rate` tracks `invalid_rate` almost exactly
(0.792 vs 0.739 on s0), which normally implicates the token budget — but
`sampled_tokens_p90` **falls**, so the outputs got shorter, not truncated. And
reward falls with it, so `core.INVALID_COST` is charging correctly: a collapse,
not a reward hack.

Two things this adds to §3:

- **It is reproducible.** 2/2 seeds, which is §3's own stated bar ("if it climbs
  past ~0.15 again by step 60, the collapse is reproducible and worth treating
  as a finding rather than an accident"). Here it crossed 0.30 by step 41.
- **It is not the hidden-horizon arm.** §3 saw it in `grim + inf`; this is
  `hole`, a different manipulation entirely. Whatever drives it is not specific
  to scrubbing the round count.

### 4.1 Update 08-31: it is not specific to ANY manipulation

Overnight every remaining cell ran deeper, and the picture changed from "two
arms collapse" to something simpler and worse:

| cell | max step | collapsed at |
|---|---|---|
| tft + inf s1 | 120 | 93 |
| grim + inf s0 | 93 | 60 |
| tft + inf s0 | 82 | 58 |
| grim + inf s1 | 74 | 65 |
| **tft + base s0** | 66 | **61** |
| tft + eg s2 | 50 | 50 |
| hole s0 / s1 | 41 | 30 / 34 |

**Every cell that ever passed step 58 collapsed — 5 of 5.** The fifth is
`tft + base`, a plain baseline with no manipulation at all. The base and eg
cells look clean only because they were stopped at steps 34–50, short of the
onset band; 13 cells stopped below step 58 and 10 of them never collapsed.

So the collapse is not a property of `hole`, or of `inf`, or of the endgame
penalty. **It is what this training setup does to this model somewhere past
step ~50–60**, and the arms differ only in when they get there. That also
retires the §4 framing above: "reproducible across two manipulations" was true
but understated — it reproduces across every manipulation *and* the control.

The practical consequence for everything else in this log: **no cell in this
wave is trustworthy past its own onset**, and any future run needs the
`invalid_rate` alert wired to stop the run rather than just log it. Nothing in
§1–§3 or §5–§7 is affected, because every number there comes from steps at or
below 35 (the eval checkpoints) or from windows ending at 34 — well before the
earliest onset of 30 in `hole` and 58 in `inf`. The one exception is §4 itself,
whose `hole` numbers ARE the collapse.

`hole` remains the right third disposition point (no punishment / recoverable /
terminal), but the arm needs the collapse understood before it yields a number.

## 5. Endgame reasoning vs. endgame behaviour: the policy finds *the last round*

The training curves above measure **behaviour in a fixed 10-round game**, which
cannot distinguish a policy that learned "defect when the end is near" from one
that learned "defect around round nine". Replaying frozen **step-35** adapters
at lengths the arms never trained on separates those.

Mean **absolute round index of the first defection**, 3 seeds per arm, 16
episodes per (arm, seed, length), 624 on-condition episodes:

| arm | horizon | N=6 | N=10 | N=14 | slope vs N |
|---|---|---|---|---|---|
| grim + base | shown | 4.89 ± 0.06 | 9.00 ± 0.00 | 13.00 ± 0.00 | **+1.01** |
| grim + eg | shown | 4.93 ± 0.04 | 8.97 ± 0.03 | 12.93 ± 0.04 | **+1.00** |
| tft + base | shown | 4.75 ± 0.13 | 8.90 ± 0.06 | 12.83 ± 0.04 | **+1.01** |
| tft + eg | shown | 4.90 ± 0.07 | 8.88 ± 0.12 | 12.85 ± 0.06 | **+0.99** |
| **tft + inf** | **scrubbed** | — | 9.00 | 9.00 | **+0.00** |

A policy that memorised a position gives slope 0; one that tracks the true final
round gives +1. Expressed as *rounds before the end*, the four horizon-visible
arms sit at 0.00–0.25 at every length. **They relocate the endgame to wherever
the end actually is.**

**The negative control is what makes this a finding.** `inf` has the stated
total scrubbed by `core.scrub_horizon`, so it cannot know N and its timing must
not move with N. It doesn't: slope **+0.00**, parked at absolute index 9
regardless of length. The measurement is therefore driven by the stated horizon
and not by some mechanism that makes first-defect track N regardless.

Two limits to carry:

- **The control is thin.** One seed, and it barely defects at all — 0.00 / 0.06
  / 0.19 of episodes by length, none at N=6 — so those 9.00s rest on a handful
  of episodes. Directionally unambiguous, quantitatively weak. (The low rate is
  itself the expected behaviour: no known last round, no endgame.)
- **`tft + base` defects in essentially every episode** (1.00 / 0.94 / 0.96)
  where every other arm sits at 0.50–0.77. Its timing mean is over a near
  complete sample; the others condition on the ~60% of episodes that defect at
  all. *When* it defects and *whether* it defects are separate results here.

Not reported: `capture`, `score`, pooled payoff. `PAYOFF_SCALE` is a fixed 30.0
that does not scale with length, so raw payoff rises ~40% at N=14 against an
unchanged denominator. Raw defection timing is the only length-comparable
statistic, which is why it is the only one above.

Gate: mean decisions per episode came out at exactly 6.00 / 10.00 / 14.00
(n=224 each), so the length really did thread through to the env *and* to the
prompt the model reads.

## 6. It learned the game, not the opponent

Crossplay of every arm against **both** counterparts, 3 seeds, 8 episodes per
cell. Exploit rate, after excluding 19 of 208 episodes above `HANDOFF-think4.md`
§7's `invalid_rate` 0.25 threshold (14 from one checkpoint, `grim/base` s1):

| arm (trained vs) | plays grim | plays tft | off − on |
|---|---|---|---|
| grim + base | 0.104 ± 0.007 | 0.125 ± 0.008 | +0.021 |
| grim + eg | 0.160 ± 0.049 | 0.117 ± 0.005 | −0.044 |
| tft + base | 0.116 ± 0.011 | 0.128 ± 0.008 | −0.011 |
| tft + eg | 0.094 ± 0.009 | 0.103 ± 0.022 | −0.009 |

Every off-diagonal is within about one SE of its own diagonal. This is the
pre-registered first branch: **the opponent split changed the gradient without
changing the learned policy.** A grim-trained policy plays tit-for-tat much the
way a tft-trained one does.

That reframes §1. The Δ there is real and it is an effect **of the training
signal**, not evidence that the arms acquired different dispositions. Any
sentence claiming the arms learned distinct *dispositions* has to be rewritten
as a claim about what the opponent split does to the gradient.

The exclusion mattered and it cut **toward** the null: unfiltered, `grim + eg`
read −0.064 and `tft + base` +0.062, and both shrank once the fallback-move
episodes came out. `first_defect_index` deltas (+0.25 to +0.90, errors ±0.1–1.1)
are not distinguishable from zero either.

## 7. The hidden-horizon arm: the endgame is a cue, not a disposition

`inf` scrubs the stated round total (`core.scrub_horizon`) and changes nothing
else. Three independent strands now say the same thing, and together they say
something stronger than any one of them.

### 7.1 Removing the horizon removes the endgame — and inverts it

**§7.4 re-reads this table against step 0: every gap in it is already present in
the untrained policy.** The contrast below is correct; the attribution to
training is not.

Mean `train/endgame_rate` over **steps 8-34** — the deepest window every
base/eg *and* `inf` seed reaches while still pre-collapse (§4.1), so this is
matched on depth rather than read off cells at different ones:

| | endgame_rate | exploit_rate (all rounds) | ratio |
|---|---|---|---|
| grim + base | 0.318 ± 0.003 | 0.218 ± 0.022 | **1.46** |
| grim + eg | 0.275 ± 0.009 | 0.225 ± 0.029 | 1.22 |
| grim + inf | **0.056 ± 0.001** | 0.086 ± 0.005 | **0.66** |
| tft + base | 0.354 ± 0.026 | 0.199 ± 0.005 | **1.78** |
| tft + eg | 0.227 ± 0.051 | 0.164 ± 0.038 | 1.38 |
| tft + inf | **0.046 ± 0.005** | 0.082 ± 0.009 | **0.56** |

n = 2 seeds for each `inf` cell, 3 for the others. (An earlier version of this
table used steps 8-16, all `inf` had at the time; the numbers barely move.)

**The ratio column is the point, not the first column.** `inf` halves defection
overall, so a bare endgame_rate drop would be consistent with "it just
cooperates more". It is not: the base arms defect *more* in the final window
than on average (ratio > 1, the endgame effect), and the `inf` arms defect
**less** there than on average (ratio ≈ 0.33-0.44). Deleting the stated total
does not dampen the endgame concentration, it reverses it. The one mature seed
says the same over its whole run: `tft/inf` s1 averages 0.048 across steps
8-64, against 0.390 for `tft/base` s1.

**One caveat on the ratio, found 08-31.** For `inf` both numerator and
denominator are small (0.05 over 0.08), so the ratio is unstable over long
windows: extended to each seed's full pre-collapse range, three `inf` seeds sit
at 0.67-0.69 but `tft/inf` s1 inverts to 1.39. The matched window above is the
number to quote, and the inversion claim should be stated as holding *at
matched depth*, not as a property that strengthens with training.

### 7.2 The behaviour is driven by the cue at inference, not by the weights

The sharpest evidence is a within-checkpoint manipulation: **the same step-35
`tft/inf` adapter**, the same 96 episodes, with only the prompt's horizon
disclosure changed.

| horizon | N=6 | N=10 | N=14 | first-defect index |
|---|---|---|---|---|
| scrubbed (as trained) | 0/16 | 1/16 | 3/16 | 9.00 |
| shown | 13/16 | 13/16 | 9/16 | 4.46 / 8.62 / 12.89 |

Pooled, 4/48 versus 35/48 episodes contain any defection — Fisher exact
**p = 6.5 × 10⁻¹¹**. Same weights. The only thing that changed is whether the
prompt states a total.

Two things follow, and the second is the one worth arguing about:

- **Training without a horizon did not remove the capability.** Handed a
  horizon it never trained with, this policy uses it *correctly* — relocating
  its first defection to the true final round at every length (slope +1.05,
  §5's off-condition row). It did not have to learn that here; it arrived able
  to.
- **So "endgame reasoning" in this wave is a response to a stated cue, not a
  disposition the training installed.** The `nohole`/`eg` arms differ in *how
  strongly* they act on the cue (§1). The `inf` arm shows that removing the cue
  removes the behaviour outright, in weights that demonstrably still know what
  to do with it.

### 7.3 The reasoning tracks the cue too, and notices it is missing

**§7.4 re-reads this against step 0: the `notices_unknown` gap is there before
any gradient step.**

Marker counts over the 960 reasoning turns per condition, same checkpoint:

| | mentions an ending | says the length is unknown |
|---|---|---|
| scrubbed | 0.32 | **0.070** |
| shown | 0.53 | 0.001 |

Under scrubbing the policy talks about endings less (0.53 → 0.32) and starts
explicitly flagging that it *cannot tell* how long the game runs — 7.0% of
turns against 0.1%, a 70× difference. It is not simply failing to think about
the end; it represents the absence of the horizon and says so.

**These are crude regexes and should be read as direction, not level.**
`PLAN-think4-evals.md` D notes the marker set is still being iterated, and a
raw-text scan will both miss paraphrases and catch mentions that are not
endgame reasoning. The 70× gap is far too large to be regex noise; the 0.32
absolute is not a number to quote.

### 7.4 How much of this did training do?

`train_mixed.py` samples its rollouts, calls `tc.optim_step` (~L844), and only
then logs `m = {"step": step, ...}` (~L898) built from the **pre-update**
rollouts. So the metrics row for step N describes the policy at the *start* of
step N, and **step 0 is the untrained policy**. Anything already present at step
0 was not installed by training. Read that way: **almost everything §7 rests on
is already true at step 0.**

Concentration index = `train/endgame_rate` / `train/exploit_rate`, computed per
seed and then averaged, **between-seed** SE. Windows are step 0; 8-16, §7.1's
window and the deepest every `inf` seed reaches; 16-19; and 30-37, the deepest
window all base/eg seeds reach.

| arm | step 0 | 8-16 | 16-19 | 30-37 |
|---|---|---|---|---|
| grim + base | 0.71 ± 0.13 | 1.26 ± 0.14 | 1.46 ± 0.09 | 1.61 ± 0.15 |
| grim + eg | 0.67 ± 0.07 | 0.92 ± 0.17 | 1.30 ± 0.27 | 1.82 ± 0.06 |
| grim + inf | 0.22 ± 0.13 | 0.44 ± 0.05 | 0.70 ± 0.20 | 0.84 ± 0.06 |
| tft + base | 1.08 ± 0.06 | 1.34 ± 0.14 | 1.76 ± 0.14 | 2.34 ± 0.23 |
| tft + eg | 0.90 ± 0.05 | 1.25 ± 0.15 | 1.41 ± 0.21 | 1.60 ± 0.36 |
| tft + inf | 0.23 ± 0.07 | 0.33 ± 0.07 | 0.62 ± 0.14 | 1.22 ± 0.08 |

n = 3 seeds for base/eg, 2 for `inf`.

**Completed 08-31; the table is now final.** When this was first written the
`inf` cells were mid-flight and the 30-37 column was empty for `grim/inf` and
n=1 for `tft/inf`. All four `inf` seeds have since passed step 74-120 and
collapsed (§4.1), so 30-37 is filled at n=2 from steps well before every onset
(earliest 58). `tft/inf` 30-37 moved 1.14 (n=1) → **1.22 ± 0.08** (n=2) and
`grim/inf` lands at **0.84 ± 0.06**; the step-0 `tft/inf` cell also shifted
0.22 → 0.23 on recompute. No column will move again — every `inf` cell is
stopped, and everything past its onset is excluded.

**What the completed column adds — and a correction it forces.** The `inf`
index does rise across the table (0.24 → 0.44 → 0.66 → 0.83 grim; 0.22 → 0.33
→ 0.59 → 1.23 tft). It is tempting to read that as training building endgame
concentration in the hidden-horizon arm. **That reading is wrong**, and the
index alone cannot distinguish it from the truth, because a ratio rises equally
well when its denominator falls. Decomposed:

| window | grim/inf endgame | grim/inf exploit | index | | tft/inf endgame | tft/inf exploit | index |
|---|---|---|---|---|---|---|---|
| step 0 | 0.068 ± 0.047 | 0.280 ± 0.043 | 0.24 | | 0.047 ± 0.013 | 0.208 ± 0.011 | 0.22 |
| 8-16 | 0.054 ± 0.001 | 0.124 ± 0.010 | 0.44 | | 0.039 ± 0.006 | 0.120 ± 0.008 | 0.33 |
| 16-19 | 0.051 ± 0.004 | 0.078 ± 0.017 | 0.66 | | 0.045 ± 0.000 | 0.076 ± 0.017 | 0.59 |
| 30-37 | 0.051 ± 0.002 | 0.061 ± 0.007 | 0.83 | | 0.047 ± 0.008 | 0.038 ± 0.004 | 1.23 |
| 45-57 | 0.035 ± 0.005 | 0.050 ± 0.010 | 0.69 | | 0.037 ± 0.010 | 0.028 ± 0.004 | 1.32 |

**`endgame_rate` is flat.** Across the whole run it goes 0.068 → 0.035 (grim)
and 0.047 → 0.037 (tft) — if anything slightly *down*. What moves is
`exploit_rate`, which falls **5.6×** and **7.4×**. The entire climb is the
denominator draining away.

So training is not teaching the hidden-horizon policy to defect at the end. It
is teaching it to stop defecting everywhere else, and the late-round defection
it started with is the residue left standing. The rise in the index measures
the disappearance of mid-episode betrayal, not the arrival of endgame timing.

**The same is true of the base arms**, which is the part that generalises:
`grim/base` endgame_rate runs 0.269 → 0.321 → 0.334 → 0.267 → 0.276 while its
exploit_rate falls 0.386 → 0.144 (2.7×); `tft/base` is 0.332 → 0.201 against
0.307 → 0.094 (3.3×). Every arm in this wave shows a rising concentration index
driven by a falling denominator. **No arm learned to defect later; every arm
learned to defect less, and endgame defection is what survived the pruning.**

Two smaller corrections that follow. The rise is **not monotonic** once the
45-57 window is included — `grim/inf` turns over at 0.83 → 0.69 and `tft/base`
at 2.33 → 2.14. And the absolute `inf`-vs-base gap in endgame_rate (~6×) is
present at step 0 and essentially constant thereafter, which is §7.4's own
thesis rather than an exception to it.

Present before a single gradient step:

- **The `inf` endgame collapse.** `endgame_rate` 0.068 ± 0.047 (grim) and
  0.046 ± 0.012 (tft) at step 0, against the 0.054 ± 0.001 and 0.039 ± 0.006
  that §7.1 reports at steps 8-16. Flat.
- **The inversion.** `inf` concentration 0.22 at step 0, against 0.71 (grim) and
  1.08 (tft) for base.
- **§7.3's manipulation check.** `notices_unknown` is 0.125 (`grim/inf`) and
  0.115 (`tft/inf`) at step 0, against 0.000 in the horizon-visible arms. The
  70× gap §7.3 quotes at step 35 is there before training. (One seed.)
- **Most of the reasoning suppression** that
  [`0830-endgame-reasoning.md`](0830-endgame-reasoning.md) §3 attributes to the
  hidden horizon. `inf` vs `nohole` relative delta at step 0, against that log's
  published pooled 0-35 value: grim `backward_induction` −51.5% vs −60.5%, grim
  `endgame_defect_plan` −45.2% vs −55.0%, grim `endgame_hold` −36.3% vs −59.6%,
  tft `backward_induction` −3.7% vs −25.3%, tft `endgame_defect_plan` −26.8% vs
  −26.5%, tft `endgame_hold` −10.6% vs −38.6%. The tft `endgame_defect_plan`
  effect is entirely present at step 0.
- **§7.2 is a within-checkpoint prompt swap and §7.3 a same-checkpoint marker
  count**, so by construction neither can speak to training at all.

Three things do change over training:

1. **Overall defection roughly halves in every arm.** `exploit_rate`, step 0 →
   30-37: `grim/base` 0.386 ± 0.020 → 0.169 ± 0.025, `tft/base` 0.307 ± 0.003 →
   0.159 ± 0.008. For `inf`, step 0 → 8-16: grim 0.280 ± 0.043 → 0.124 ± 0.010,
   tft 0.209 ± 0.010 → 0.120 ± 0.008.
2. **Final-window defection does not fall with it.** `endgame_rate` `grim/base`
   0.269 ± 0.036 → 0.267 ± 0.033, `tft/base` 0.332 ± 0.016 → 0.371 ± 0.033. So
   the concentration index roughly doubles (0.71 → 1.61, 1.08 → 2.34).
   **Training does not teach the endgame; it prunes everything that is not the
   endgame.**
3. **The endgame penalty's `tft` suppression is genuinely trained.** At step 0
   the arms are indistinguishable — `endgame_rate` 0.332 (base) against 0.300
   (eg), concentration 1.08 against 0.90. By steps 30-37 they are 0.371 against
   0.146, all three seeds moving down. **§1 and §2 are therefore about training
   in a way §7 is not.**

The concentration rise also appears in the `inf` arms, from a much lower start
(`grim/inf` 0.22 → 0.70 by step 19, `tft/inf` 0.22 → 0.62, and 1.14 at n=1 in
the late window), so training installs something endgame-shaped even with no
stated horizon. This is the weakest of the three — three of the four `inf` cells
are barely past step 20.

**None of this contradicts §7's conclusion; it moves the attribution.** §7 says
the endgame is a cue rather than a disposition, and the step-0 evidence makes
that case *more* strongly than §7 does — the cue-response is there in weights
that have taken no gradient at all. What it revises is where the evidence comes
from: §7.1's numbers were read at steps 8-16 and presented as a property of the
trained arms, when the gap is already at step 0. **The conclusion stands; the
evidence was not about training.**

Three limits to carry:

- **The index is an INDEX, not a probability.** `endgame_rate` divides by the
  exogenous late window while `exploit_rate` is over all rounds — different
  denominators — and it inherits `core.py`'s warning that `endgame_rate` is not
  comparable across counterparts. The reliable read is the **within-arm** change
  over training; between-arm level comparisons are weaker.
- **`inf` is two seeds and shallow.** Three of the four cells are around step 20
  and still climbing; only `tft/inf` s1 is deep. No `grim/inf` cell reaches the
  30-37 window and only `tft/inf` s1 does, so that 1.14 is n=1 with no error
  bar. The figure's coverage footer names the live cells at render time.
- **Every reasoning number is one seed**, ~±0.03 binomial on a 192-block point.
  Directional only.

Figure and numbers:
`results/0830_training_vs_cue/fig1_training_vs_cue.{png,json}` — quote the JSON.

### 7.5 What this does NOT support

- **No magnitude against §1.** §7.1 is matched at steps 8-16 because that was
  the deepest window every `inf` seed reached when it was written, and it must
  not be compared to §1's step ≥ 8 means. Those cells are still training and are
  now past step 20 (§7.4), so the matched window can be deepened on a re-render;
  the comparison to §1 remains invalid either way.
- **§7.2 and §7.3 rest on one checkpoint** (`tft/inf` s1, step 35). The
  contrast within it is enormous and internally replicated across 96 episodes,
  but one seed is what broke §1, and there is no `grim/inf` checkpoint deep
  enough to check whether the opponent changes any of it.
- **Nothing about `grim/inf` specifically**, which is also the arm §3 recorded
  as having collapsed once before.

## 8. Provenance — these runs are not Tinker

Sampling is a local sglang server per cell; the gradient step is local PEFT
LoRA (rank 32, lr 2e-5) against `/shared/clod/qwen3.8-27b`. `train_mixed.py` and
`tinker_actor.py` are **unmodified** — only `tinker.ServiceClient` is swapped, so
flags, envs, advantage scheme and label conventions are identical to `0826`.

Two differences worth recording against any cross-wave comparison:

- **`--workers 64`, not 10.** The old value was sized for an 8-CPU box sharing
  one Tinker account. Measured here at 10: `#queue-req 0`, KV cache at 2%, so the
  sampler was starved, not saturated. This changes throughput, not the update.
- **The importance ratio is exactly 1 by construction.** `train_mixed` does one
  `forward_backward` per `optim_step`, so the run is on-policy and the ratio is
  mathematically 1. Under Tinker that held because one service both sampled and
  trained; here sampler and trainer are different stacks whose logprobs disagree
  by ~0.04 nats on high-entropy tokens (fused GDN/conv1d kernels vs
  transformers'). Feeding that gap into `exp()` would inject a systematic ~7%
  downweight on exactly the uncertain tokens, so the denominator is the trainer's
  own detached logprob. Divergence from the sampler is still logged as
  `behavior_drift`.

Two more that apply only to the §5/§6 sweeps:

- **The evals serve LoRA adapters, not merged weights.** `PLAN-think4-evals.md`
  §0.3b warns that the wave's adapters do not match how sglang was launched
  (trained `all-linear`, served on seven module types, so LoRA would silently
  drop on 96 of 128 layers). That applies to the **Tinker** adapters. These are
  the local ones, and `/get_server_info` confirms `lora_target_modules` is
  exactly the seven modules `tinker_local/service.py` trains. Served function =
  trained function.
- **Every checkpoint was verified to be the checkpoint.** `create_sampling_client`
  used to discard its arguments and return base weights for any checkpoint
  named, which no downstream statistic can detect. It now loads or raises, and
  `ckpt_guard.py` asserts each adapter moves the model's teacher-forced prompt
  logprobs away from base before the sweep spends anything. All 13 cleared at
  0.082–0.160 nats; a step-0 adapter (B=0, mathematically identical to base) is
  still correctly rejected at 0.00000 against a 0.01 floor.

## 9. What to do next

1. **Do not spend more on grim base/eg.** n=3, tight SEs, flat across every
   window. Killed on 08-30; resume from state if the ≤step-50 ceiling (§2)
   turns out to matter.
2. **`inf` needs depth, not more seeds, for a magnitude claim.** It now has two
   seeds per opponent (§3) and §7 draws real conclusions from them, but three of
   the four sit at step 16-17. Getting `grim/inf` to step 35 is the single
   highest-value remaining run: it would let §7.2's within-checkpoint result be
   checked against a second opponent, which is the gap §7.5 names.
3. **Rewrite the `0826` §4 headline.** "Flips sign with the opponent" is not
   supported. The defensible statement is: *the penalty suppresses late betrayal
   against both punishers, roughly 3–4× more strongly against tit-for-tat than
   against grim* — an interaction of magnitude, not of sign.
4. **Rewrite any "disposition" language as training signal.** §6 says the arms
   did not learn different policies. This is the larger framing change of the
   two and it affects `0826` throughout, not just its headline.
5. **The collapse is now a result, not a nuisance.** Two arms, three seeds,
   one signature, cause still undiagnosed.
6. **§7.3's markers need the real regex set.** The 70× gap in "length is
   unknown" is too large to be an artefact, but the absolute rates come from a
   throwaway scan. Running `endgame_awareness.py` over the `inf` pages would
   put that on the same footing as the rest.
7. **Re-run §5 at a later step.** Step 35 was chosen because it is the deepest
   step all 13 checkpoints share. Whether the length-tracking in §5 sharpens or
   decays as tft keeps training is untested, and the `inf` control deserves a
   second seed as soon as one exists.
7. **The reasoning-side question has a first 3-seed answer.** Final-round
   decision blocks with behaviour normalised out: endgame defect-planning falls
   while hold-planning rises, at roughly a third to a fifth the behavioural
   effect — see [`0830-endgame-traces.md`](0830-endgame-traces.md) §12. Still
   wants more seeds and the `inf` arms before any headline claim.
8. **Re-attribute §7, and read step 0 before crediting anything else to
   training.** §7.4 shows the `inf` contrasts are already there in the untrained
   policy, so any sentence crediting them to training becomes a claim about the
   cue. The cheap general move is the point: step 0 is a free untrained control
   already sitting in every `metrics.jsonl`, and this is the only arm-vs-arm gap
   in the wave that has been checked against it. The `tft` side of the endgame
   penalty clears it (§7.4, item 3); the `grim` side, §5, §6 and §10 have no
   step-0 read at all.

## 10. Grim vs tit-for-tat across every arm: the same strategy, and the reason it had to be

§6 showed the arms play alike at step 35 on ipd crossplay and called it "the
opponent split changed the gradient without changing the learned policy". This
section asks the wider question — every grim and tft cell in the wave, on
training-time behaviour, on the per-round action sequences, and on both eval
sweeps — and supplies the **mechanism**: the policies converge on a strategy
that never enters the part of the game where the two opponents differ.

New evidence here is the per-episode `my_decisions`/`opp_decisions` sequences in
`<run>/traces/step_NNNN.jsonl`, which nothing in this wave had read before.
Figures and cached numbers: [`results/0830_grim_vs_tft/`](../results/0830_grim_vs_tft/).
Run snapshot `d31ee6ab23176486`, captured 2026-08-30 22:26 UTC — the `tft` cells
are live, see §10.6.

### 10.1 Both arms converge on: cooperate every round, defect at the buzzer

From the ipd action sequences, pooled over steps ≥ 25, between-seed SE:

| | episodes | cooperation rate | any defection | defects in final round | **defects before final round** |
|---|---|---|---|---|---|
| grim + base | 77 | 0.908 ± 0.017 | 0.794 ± 0.104 | 0.794 ± 0.104 | **0.121 ± 0.072** |
| tft + base | 96 | 0.897 ± 0.010 | 0.924 ± 0.076 | 0.924 ± 0.076 | **0.104 ± 0.032** |
| grim + eg | 60 | 0.938 ± 0.009 | 0.620 ± 0.091 | 0.620 ± 0.091 | **0.000 ± 0.000** |
| tft + eg | 95 | 0.944 ± 0.020 | 0.541 ± 0.188 | 0.541 ± 0.188 | **0.022 ± 0.022** |

Both arms open with cooperation in 100% of episodes. The third and fourth
columns are **equal in every cell of the cache** — read precisely, that says no
episode defects mid-game *without also* defecting at the buzzer. It does not say
all defection is final-round defection; the last column is the remainder, and it
is small but not zero.

Where the defections actually sit, per-round, base arms, steps ≥ 25:

| | r1–r7 | r8 | r9 | r10 |
|---|---|---|---|---|
| grim + base | 0.000 | 0.000 | 0.121 | 0.794 |
| tft + base | 0.000 | 0.021 | 0.083 | 0.924 |

Rounds 1–7 are **exactly** 0.000 in every seed of both arms. The frozen step-35
adapters put the same spike at the true end of the game at N = 6, 10 and 14
(§5), so this is not an artefact of the fixed 10-round training length.

### 10.2 The two opponents are the same opponent until the model defects early

Grim and tit-for-tat differ in exactly one respect: what they do after a
defection that has rounds left after it. A **final-round** defection leaves
neither of them a round in which to punish. So the entire grim/tft contrast is
carried by the last column of §10.1's table.

Exposure to that regime — the share of rounds played after the opponent has
defected at least once — is 0.000 in every cell except `tft + base`, at
0.002 ± 0.001. The opponent's own cooperation rate is 0.988–1.000 throughout.

The repair funnel, over all trained steps (≥ 5), counts not rates:

| stage | grim + base | tft + base | grim + eg | tft + eg |
|---|---|---|---|---|
| episodes | 149 | 168 | 132 | 167 |
| defected before the final round | 14 | 22 | 3 | 12 |
| opponent retaliated | 14 / 14 | 22 / 22 | 3 / 3 | 12 / 12 |
| model returned to cooperating | 0 / 14 | **1 / 22** | 0 / 3 | 0 / 12 |
| opponent forgave | n/a by construction | **1 / 1** | n/a by construction | 0 / 0 |

Retaliation is deterministic — every mid-game defection was punished. The funnel
then dies, because the model had already spent its defection at the buzzer and
had no round left in which to return. **Across 616 episodes the path that
separates grim from tit-for-tat completes once.** Grim's bottom row is `n/a`
because grim never forgiving is the opponent's definition, not a measured null.

That is the mechanism behind §6. The distinguishing gradient was delivered on 51
of 616 episodes, and the forgiveness that is tit-for-tat's entire point was
exercised a single time.

### 10.3 Three ways to break the confound, and all three agree

Any difference measured on `ipd` confounds a learned-policy difference with the
fact that the opponent itself differs there. Three independent handles do not:

**(a) The shared-opponent envs.** `public_goods`, `dond` and `trust` draw
**identical** counterpart populations in both arms — verified row by row against
every trace file. A gap there is a policy difference with nothing else moving.
Exploit rate, steps ≥ 25:

| | grim-trained | tft-trained | grim − tft |
|---|---|---|---|
| baseline | 0.121 ± 0.010 | 0.111 ± 0.003 | +0.010 ± 0.010 (1.0 SE) |
| + endgame penalty | 0.103 ± 0.019 | 0.048 ± 0.010 | **+0.055 ± 0.022 (2.5 SE)** |

**(b) Crossplay with the played opponent held fixed.** §6 varied the *played*
opponent within an arm; this varies the *training* opponent within a played
opponent, which is the contrast that isolates the policy. Baseline exploit rate,
grim-trained minus tft-trained: −0.012 ± 0.013 playing grim, −0.003 ± 0.012
playing tft. Over all metrics: **26 testable contrasts, 1 clears 2 SE, 0 clears
2 SE with both sides varying**, 4 clear 1 SE. (Two of the 28 are untestable —
`frac_any_defect` at baseline, both arms pinned at 1.000, so |z| is undefined.
The one that clears has zero between-seed variance on one side, so its
quadrature SE understates the uncertainty.)

**(c) Held-out horizons.** Fitted slope of first-defection index against N is
+1.000 to +1.014 for all four arms (§5). Grim and tft lie on top of each other.

### 10.4 The one place the opponent does matter is the endgame penalty

The knob does not act equally. `train/endgame_rate`, eg minus base, steps ≥ 8,
paired on seed index: **−0.044 ± 0.013 against grim, −0.159 ± 0.067 against
tft** — a 3.6× asymmetry, and §1's result restated on this snapshot.

The important addition is that the asymmetry **transfers off ipd**. §10.3(a)
shows the baseline arms do not separate on the shared-opponent envs while the
penalised arms do, at 2.5 SE. So the opponent split does eventually change the
policy — not on its own, but through its interaction with the penalty, and in a
way that shows up in envs where the opponent was never manipulated. The reasoning
markers move with the same asymmetry (`endgame_defect_plan` −0.083 ± 0.167 vs
−0.288 ± 0.115; [`0830-endgame-traces.md`](0830-endgame-traces.md)), though that
log shows most of the tft side is a length confound.

### 10.5 What this changes, and what it does not show

- **§6 gets a mechanism, and §9 item 4 gets stronger.** "The arms did not learn
  different policies" is now not just an observed null but a predicted one: a
  policy whose only defection is a buzzer-beater cannot be shaped by how its
  counterpart responds to being defected on.
- **[`0824-isolation.md`](0824-isolation.md) asked whether tit-for-tat teaches
  recovery of trust. This wave cannot answer that** — it is unanswered, not
  answered in the negative. The policy is punished 51 times in 616 episodes and
  returns to cooperating once. To measure recovery you first need the policy to
  get punished.
- **The design implication is the actionable part.** A fixed-length game with a
  visible horizon collapses onto endgame defection, which is precisely the move
  both counterparts treat identically. Any future opponent-disposition split
  needs the distinguishing signal to be reachable: the `inf` arm is the obvious
  lever (no known last round, so defection has to happen mid-game to happen at
  all — §7), or a payoff structure where mid-game defection is tempting.
- **This is not an equivalence claim.** A wide interval containing zero is a
  failure to detect a difference, not a demonstration that none exists. The
  baseline null is worth something only because the `eg` arm separates at the
  same sample size.
- **Handles (b) and (c) are frozen at step 35.** Nothing here speaks to what
  happens later in training.
- **`hole_exp/results/eval_grimtft_expanded/` looks like the direct answer and
  is not.** Its `grim_trained` file is the *hidden-horizon* arm at step 40 and
  its `tft_trained` file is the *baseline* arm at step 30, both think3 — arm,
  manipulation, step and generation all vary at once. Its striking numbers
  (winasmuch exploit 0.135 vs 0.525) are uninterpretable as an opponent effect.

### 10.6 Drift, because the tft cells are still running

§1's tft row was computed at a ~step-50 ceiling. At this snapshot `tft/base` s0
reaches step 60 and the same statistic reads 0.343 ± 0.040 baseline and
−0.159 ± 0.067 delta, against §1's 0.348 ± 0.035 and −0.164 ± 0.063. Not a
contradiction — the same number, further along.

One substantive move worth watching rather than filing: `tft/base` `ever_defect`
fell from 0.960 to **0.919** as steps 45–60 arrived, and `tft/inf` rose from
0.125 to 0.176. The grim cells are dead and stable to ±0.000. Every figure and
number in §10 comes from one snapshot digest; `build_train_cache.py` records the
per-run mtimes and fails loudly if a rate moves more than 0.02 against its
recorded table.

---

### Reproducing §10

```
cd results/0830_grim_vs_tft
python build_train_cache.py      # /shared/allie/think4/runs -> train_strategy.json
python build_eval_cache.py       # think4_evals + trace_blocks -> eval_strategy.json
python fig1_strategy_evolution.py       # strategy over training, grim vs tft
python fig2_unreachable_difference.py   # hazard by round, exposure, repair funnel
python fig3_opponent_or_policy.py       # the three confound-breaking handles
python fig4_knob_by_opponent.py         # the endgame-penalty interaction
```

Every figure writes a companion `.json` carrying every number drawn, and reads
only the two caches, so the figures are pure functions of a single run snapshot.
`README.md` there carries the caveats in full — in particular that the training
cache calls the baseline arm `base` while the eval cache calls it `nohole`, and
that trace dumps are the first 24 episodes of every fifth step, so `ipd`
contributes about 6 episodes per step per seed and `ipd3`/`staghunt`/`winasmuch`
never appear in them at all.

---

### Reproducing §5 and §6

```
cd hole_exp
python think4_local_ckpts.py --json                 # adapter manifest
python eval_a_endgame_length.py --local-step 35 --seeds 16
python eval_b_crossplay.py     --local-step 35 --seeds 8 --envs ipd
python analyze_think4_evals.py                      # both tables
```

Rows: `hole_exp/results/think4_evals/{A_endgame_length,B_crossplay}.jsonl`, one
per episode, carrying `train_seed` and `horizon` so on- and off-condition rows
never pool. Error bars throughout §5/§6 are **between training seeds**: each
checkpoint collapses to one number first, and the spread is across checkpoints.
Pooling the 16 episode seeds instead would give a tight interval around one
run's idiosyncrasy — which is how `0826` §4 reported a sign flip that three
seeds then contradicted.
