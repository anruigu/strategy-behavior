# 0830 — does the endgame penalty suppress endgame REASONING?

**Pooled over every turn: against tit-for-tat it visibly cuts endgame talk, but
the cut is almost entirely "the model writes less", what survives is not
endgame-specific, and against grim nothing is detectable at all. Restricted to
the final round — where every episode contributes exactly one block, so the
denominator cannot be composition — a small endgame-specific signature does
survive on both opponents (§12): plan-to-betray and `backward_induction` down,
`endgame_hold` UP, the floor control flat or rising.** The `eg` knob's effect on
late-betrayal *behaviour* survives three seeds. Its effect on the endgame
*reasoning markers* does not survive a length control pooled over all blocks and
does not separate there from a floor control that has no stake in the endgame.
Restricted to the final round it does both, at roughly a third to a fifth the
size of the behavioural move — an order of magnitude, not a measured ratio.

Companion: [`0830-endgame-summary.md`](0830-endgame-summary.md), which
established the behavioural result (grim **−0.039 ± 0.012**, tft
**−0.142 ± 0.064**, three seeds, between-seed SE). This log answers the
follow-up it leaves open.

Supersedes: `results/0830_endgame_reasoning/fig2_dissociation.png`, which
answered **yes** (−12% to −23% on the reasoning markers). That figure was **one
training seed with binomial error bars**, scored from viewer pages that no
longer exist on this box. This re-asks the question on raw chain-of-thought.

Scope: `grim` and `tft`, checkpoint **step 35**, ipd only, horizons 6/10/14,
3 train seeds × 48 episodes per arm, **624 episodes / 12,480 reasoning blocks /
13 cells**. One block is one turn's `reasoning` string; a marker hit is binary
per block. Source is the `eval_a_endgame_length.py` sweep, which stores
reasoning verbatim. Figures and paired JSONs in `results/0830_endgame_traces/`.

---

## 1. Against `grim`, nothing survives

Δ(`eg` − `nohole`), formed **within** a training seed and then averaged, SE
between training seeds (n = 3):

| marker | raw Δ | length-stratified Δ | pooled binomial floor |
|---|---|---|---|
| `endgame_defect_plan` | −0.083 ± 0.167 | −0.046 ± 0.093 | ±0.013 |
| `endgame_hold` | +0.013 ± 0.047 | +0.001 ± 0.035 | ±0.008 |
| `backward_induction` | −0.086 ± 0.150 | −0.046 ± 0.091 | ±0.013 |
| `in_game_penalty` (FLOOR / CONTROL) | −0.026 ± 0.076 | −0.009 ± 0.092 | ±0.013 |

**Every interval crosses zero**, raw and stratified alike. The per-seed
stratified deltas for `endgame_defect_plan` do not agree in sign:
**+0.064, −0.231, +0.029**. Raw, they are +0.192, −0.055, −0.385.
`backward_induction` behaves identically (+0.046, −0.227, +0.045 stratified).

The arm means underneath, which is where a one-seed reading would have stopped:

| marker | `grim/nohole` | `grim/eg` |
|---|---|---|
| `endgame_defect_plan` | 0.472 ± 0.095 | 0.389 ± 0.083 |
| `endgame_hold` | 0.103 ± 0.034 | 0.116 ± 0.019 |
| `backward_induction` | 0.422 ± 0.085 | 0.336 ± 0.081 |
| `in_game_penalty` | 0.484 ± 0.081 | 0.458 ± 0.067 |

The third column of the first table is why the old figure looked confident. The
pooled binomial SE is the sampling floor of a single arm's rate — the error bar
you would get if the three runs were one run. Across all **sixteen** estimates
drawn on fig1 the honest between-seed bar is **1.6× to 12.9×** that floor. Plot
the floor instead of the effect's own error bar and a −0.08 delta reads as six
sigma rather than half a sigma. This is the same failure mode as §1 of the
companion log, on a different quantity.

## 2. Against `tft` the raw drop is large and sign-consistent

The arm that the companion log says carries the larger behavioural effect also
carries a large raw marker effect, and here the seeds agree:

| marker | `tft/nohole` | `tft/eg` | raw Δ | per-seed raw Δ |
|---|---|---|---|---|
| `endgame_defect_plan` | 0.582 ± 0.046 | 0.294 ± 0.083 | **−0.288 ± 0.115** | −0.057, −0.393, −0.414 |
| `backward_induction` | 0.514 ± 0.035 | 0.264 ± 0.075 | **−0.250 ± 0.095** | −0.060, −0.345, −0.346 |
| `endgame_hold` | 0.268 ± 0.025 | 0.304 ± 0.032 | +0.036 ± 0.019 | +0.025, +0.009, +0.073 |
| `in_game_penalty` (FLOOR) | 0.536 ± 0.036 | 0.302 ± 0.082 | −0.235 ± 0.076 | −0.087, −0.343, −0.274 |

All three seeds move the same way on every marker. Taken at face value this is
the suppression the prior figure claimed, now at three seeds instead of one, on
the opponent where the behavioural effect is largest. **It should not be taken
at face value, and §3 is why.**

## 3. But 78% of it is verbosity

The penalty **shortens the reasoning against `tft`**: mean block length falls
from **1367 ± 52** to **885 ± 222** chars, a paired delta of
**−482 ± 212 chars (−35%)**, with all three seeds moving down (−61, −648,
−737). Against `grim` there is no arm-level length difference at all
(**−19 ± 471** chars, −1.8%, per-seed deltas +378, +521, −957).

Marker hits are binary per block, so a shorter block mechanically hits less.
Pooled over all arms, hit rate by global length quintile:

| quintile | median chars | `endgame_defect_plan` | `backward_induction` | `in_game_penalty` | `endgame_hold` |
|---|--:|--:|--:|--:|--:|
| 1 | 229 | 0.014 | 0.011 | 0.017 | 0.119 |
| 2 | 375 | 0.133 | 0.097 | 0.221 | 0.173 |
| 3 | 698 | 0.338 | 0.265 | 0.449 | 0.153 |
| 4 | 1283 | 0.706 | 0.621 | 0.686 | 0.194 |
| 5 | 2638 | 0.909 | 0.854 | 0.805 | 0.328 |

A 90-point swing from the shortest quintile to the longest, with both arms on
the same curve. Standardising to those five global bins:

| marker (tft) | raw Δ | stratified Δ | share of raw removed |
|---|---|---|--:|
| `endgame_defect_plan` | −0.288 ± 0.115 | **−0.065 ± 0.022** | **78%** |
| `backward_induction` | −0.250 ± 0.095 | −0.061 ± 0.019 | 76% |
| `in_game_penalty` | −0.235 ± 0.076 | −0.059 ± 0.042 | 75% |
| `endgame_hold` | +0.036 ± 0.019 | +0.032 ± 0.021 | 10% |

**Length standardisation removes 78% of the headline `tft` delta.** The −0.288
is mostly a statement that the penalised policy writes 35% less, not that it
thinks about the endgame less. Against `grim` no arm-level length difference is
detectable (**−19 ± 471** chars, an interval wide enough to exclude essentially
nothing), and there is correspondingly no raw effect to decompose.

## 4. And the residual is not endgame-specific

`in_game_penalty` matches generic punishment vocabulary. These games are
saturated with punishment talk, so it is carried through as the FLOOR: it has
**no stake in the endgame question** and a real endgame-specific effect should
leave it alone.

It does not. Against `tft` its stratified delta is **−0.059 ± 0.042** against
**−0.065 ± 0.022** for `endgame_defect_plan` — a difference of
**−0.006 ± 0.048**, 0.12 sigma. `backward_induction` sits on the floor too
(difference −0.002 ± 0.046). Against `grim` all three markers are inside the
floor's interval as well. **Everything falls together**, which is a statement
about the measurement, not about the endgame.

One exception, and it is **a hint rather than a result**: `endgame_hold`
against `tft` **rises**, +0.032 ± 0.021 stratified, and is the one estimate
that sits clear of the floor band (1.9 sigma from it). That is the direction a
genuine suppression story predicts — less defect-planning, more hold-planning.
Against it: the interval only just excludes zero, and one of the three per-seed
stratified deltas is flat (+0.027, −0.001, +0.071). Do not build on it yet.

Everything in this section is pooled over all 12,480 blocks, where turns with no
endgame at stake dominate the denominator. **§12 conditions the same data on the
final round instead**, and the endgame-specific contrast — including this
`endgame_hold` hint, there on three seeds — only becomes visible once you look
where the endgame is live.

## 5. No flattening of the endgame spike is detectable

If the penalty suppressed *endgame* reasoning specifically, the natural
signature is a flatter approach to the final round. `endgame_defect_plan` on
decision turns, by distance from the end:

| rounds from end | `grim/nohole` | `grim/eg` | `tft/nohole` | `tft/eg` |
|---|--:|--:|--:|--:|
| 5 | 0.347 ± 0.130 | 0.201 ± 0.119 | 0.486 ± 0.077 | 0.160 ± 0.078 |
| 4 | 0.417 ± 0.136 | 0.299 ± 0.153 | 0.639 ± 0.025 | 0.229 ± 0.130 |
| 3 | 0.542 ± 0.125 | 0.389 ± 0.160 | 0.785 ± 0.039 | 0.319 ± 0.143 |
| 2 | 0.667 ± 0.098 | 0.583 ± 0.115 | 0.819 ± 0.062 | 0.354 ± 0.115 |
| 1 | 0.812 ± 0.072 | 0.854 ± 0.079 | 0.910 ± 0.025 | 0.681 ± 0.102 |
| 0 (final) | 0.910 ± 0.014 | 0.785 ± 0.028 | 0.653 ± 0.084 | 0.688 ± 0.055 |

The rate climbs steeply over the last five rounds in all four arms. Spike
amplitude — final round minus 5-from-end, computed per seed then averaged
between seeds:

| opponent | `nohole` | `eg` | difference |
|---|---|---|---|
| grim | +0.562 ± 0.136 | +0.583 ± 0.105 | **+0.021 ± 0.204** |
| tft | +0.167 ± 0.150 | +0.528 ± 0.062 | **+0.361 ± 0.186** |

**Neither difference is negative**, and against `tft` the penalised arm's spike
is if anything the steeper one. But the grim interval is far too wide to carry
a conclusion on its own: **+0.021 ± 0.204** is 0.10 sigma, and at ±2 SE it runs
from −0.39 to +0.43 — as consistent with total flattening as with none. Only
the `tft` half points anywhere (**+0.361 ± 0.186**, 1.94 sigma), and fig3's own
panel note calls that **a direction and not a result**. If the penalty
suppressed *endgame* reasoning specifically, this is where it would show; no
flattening is detectable here, which is a failure to detect and not a
demonstrated absence.

Two qualifications on that `tft` +0.361, which is a difference of shapes rather
than of levels. `tft/nohole` **peaks one round from the end (0.910) and falls
back at the final round (0.653)**, consistently across all three seeds (0.792 /
0.667 / 0.500), so the small baseline amplitude is a final-round dip and not a
flat curve. `grim/eg` shows the same one-round-early peak more mildly. Read the
table as: no arm walks into the last round talking about it less under the
penalty.

## 6. "Plan intact, act suppressed" was tested and rejected, twice

The interesting alternative to suppression is a dissociation: the policy still
works out that the last round is free, and then declines to take it — a
behavioural veto over unchanged deliberation, which is the reading an
unfaithfulness story predicts. Among final-round decision blocks, P(actually
defects), between-seed:

| conditioned on | opponent | `nohole` | `eg` | Δ | sigma |
|---|---|--:|--:|---|--:|
| `endgame_defect_plan` present | grim | 0.885 ± 0.064 | 0.679 ± 0.128 | **−0.206 ± 0.178** | 1.16 |
| **nothing at all** | grim | 0.879 ± 0.079 | 0.661 ± 0.139 | **−0.217 ± 0.201** | 1.08 |
| `endgame_hold` present (OPPOSITE marker) | grim | 0.926 ± 0.074 | 0.657 ± 0.107 | **−0.269 ± 0.161** | 1.67 |
| `endgame_defect_plan` present | tft | 0.965 ± 0.035 | 0.527 ± 0.248 | **−0.438 ± 0.266** | 1.65 |
| **nothing at all** | tft | 0.965 ± 0.035 | 0.560 ± 0.261 | **−0.405 ± 0.276** | 1.47 |
| `endgame_hold` present (OPPOSITE marker) | tft | 0.950 ± 0.050 | 0.500 ± 0.258 | **−0.450 ± 0.276** | 1.63 |

**Conditioning on the stated plan buys +0.012 of a −0.217 gap for grim and
−0.033 of a −0.405 gap for tft.** Everything the "dissociation" was carrying is
the arm's overall final-round defection rate. And conditioning on the OPPOSITE
marker returns a gap of the same sign and size a third time, on both opponents:
**a marker that predicts the same thing as its own negation predicts nothing.**

Nothing here reaches 2 sigma on either opponent, and the per-seed deltas are
dominated by one cell in each case (grim: +0.033, −0.096, −0.554; tft: −0.138,
−0.207, −0.968, the last being `tft/eg` seed 2, which defects on 4% of its
final rounds at all).

Population note: 288 final-round decision blocks per opponent. For grim, **44
(15.3%) were excluded for a null answer**, 33 of them from one seed — see §8.
For tft the exclusion is 3 blocks (1.0%).

## 7. The behaviour result partially reproduces, exactly where you would expect

Eval `endgame_rate` against the training-log reference:

| opponent | `nohole` | `eg` | Δ here | training log §1 |
|---|---|---|---|---|
| grim | 0.248 ± 0.089 | 0.248 ± 0.067 | **−0.001 ± 0.140** | −0.039 ± 0.012 |
| tft | 0.397 ± 0.023 | 0.220 ± 0.102 | **−0.177 ± 0.113** | −0.142 ± 0.064 |

**The eval reproduces the effect where it is large and cannot resolve it where
it is small.** An interval of ±0.140 would not detect a true effect of 0.039;
that is underpowered, not refuted. The denominators differ and the difference
is the whole explanation:

| | companion log §1 | here |
|---|---|---|
| environments | 7 | ipd only |
| training steps | all steps ≥ 8 | one checkpoint, step 35 |
| horizons | as trained | 6 / 10 / 14, **never trained on** |
| episodes | full training logs | 48 per cell |

The `tft` number is seed-fragile even so. Its per-seed deltas are −0.069,
−0.057, −0.403; dropping the `tft/eg` seed-2 extreme (`endgame_rate` **0.021**,
the lowest of any cell in the wave) leaves the other two averaging **−0.063**,
about a third of the headline.

**This analysis does not overturn the behavioural result.** That stands on the
training logs with three seeds and a ±0.012 error bar. What it overturns is the
one-seed *reasoning* claim from `0830_endgame_reasoning`.

## 8. Two data hazards, and a gate that misses both

Screening every cell on the share of **decision turns with an empty `answer`**
flags two, and the repo's usual gate sees neither:

| cell | empty answer (decision turns) | `invalid_rate` | mean chars | `endgame_rate` |
|---|--:|--:|--:|--:|
| **`grim/nohole` s1** | **292 / 480 = 60.8%** | **0.000** | 557 | 0.080 |
| `tft/nohole` s0 | 150 / 480 = 31.2% | 0.002 | 1362 | 0.351 |
| all ten other contrast cells | 0.6% – 15.4% | 0.000 – 0.034 | 543 – 1737 | 0.021 – 0.424 |

`grim/nohole` s1 is **compromised**: two thirds of its decisions are unusable,
its reasoning is the second shortest in the wave, and its `endgame_rate` is the
lowest of any grim cell — consistent with empty answers falling through to
`ipd_lib`'s default move rather than a chosen one. And **its episode-level
`invalid_rate` reads 0.000 on all 48 episodes**. The wave's
`invalid_rate > 0.15` gate — the one §4 of the companion log relies on to
declare the `hole` arm unreportable — **is blind to it**. An empty answer that
silently resolves to a library default is not counted as invalid anywhere in
the pipeline.

`tft/nohole` s0 is the milder case: 31.2% of decision turns (28.5% of all
turns), `invalid_rate` 0.002. Unlike the grim cell its length and behaviour are
unremarkable — mean 1362 chars, `endgame_rate` 0.351, both mid-pack — so treat
it as a **flagged hazard rather than a compromised cell**.

The part that generalises past these two cells:

| arm | mean empty-answer rate (all turns) |
|---|--:|
| `grim/nohole` | **27.2%** |
| `tft/nohole` | **14.3%** |
| `grim/eg` | 7.5% |
| `tft/eg` | 4.0% |

**Empty answers are concentrated in the BASELINE arms**, by roughly 3.5× on
both opponents. Since an empty answer falls through to the library's default
move, this asymmetry could bias the baseline arms' measured betrayal downward
and therefore *understate* the penalty's behavioural effect. That is an open
problem for the eval, not something this analysis can resolve — but it bears on
every behavioural number in the wave, including §7's. Overall, 5,413 of 6,240
decision turns parse an action (86.7%).

## 9. Sensitivity

Dropping the compromised `grim/nohole` s1 and pairing only seeds 0 and 2 flips
**all four** grim stratified deltas positive:

| grim | all 3 seeds | s0 / s2 only (n = 2) |
|---|---|---|
| `endgame_defect_plan`, stratified | −0.046 ± 0.093 | **+0.046** |
| `backward_induction`, stratified | −0.046 ± 0.091 | **+0.045** |
| `endgame_hold`, stratified | +0.001 ± 0.035 | **+0.036** |
| `in_game_penalty`, stratified | −0.009 ± 0.092 | **+0.036** |
| `endgame_defect_plan`, raw | −0.083 ± 0.167 | −0.097 |

So grim's central sign is one cell, the raw deltas are robust, and **the
"crosses zero" conclusion holds either way** — with three seeds the markers move
slightly down and cross zero, with two they move slightly up and cross zero.
No SE is quoted at n = 2 because it is not a meaningful quantity there.

`tft` is robust to its own worst cell **in the direction that matters**:
dropping `tft/nohole` s0 moves the effect *away* from zero (raw
−0.288 → −0.403, stratified −0.065 → −0.073). The `tft` conclusion is not
resting on a hazardous cell.

## 10. A methodological note worth carrying forward

The grim-only version of this analysis reported that mean reasoning length
predicts *behaviour* at Pearson **r = 0.899 with Spearman rho = 1.000** — a
perfect rank ordering over six (arm, seed) cells, cutting across the arm split.
It did **not** survive adding `tft`. Over the 12 paired cells it is
**r = 0.815, rho = 0.706**. A perfect rank ordering over six points was an
artifact of six points.

Length vs the *marker* rate held up better and in fact strengthened: **r = 0.881
over the 12 paired cells** (rho = 0.846), against r = 0.838 grim-only. Per-cell
mean length still spans **3.2×** (543 to 1737 chars).

The general lesson stands and is the one to carry: **any future marker claim
needs the length control**, because a binary regex hit per block is
substantially a verbosity readout. Report raw *and* stratified, and carry
`in_game_penalty` as the floor.

## 11. Coverage

| cell | seeds with episodes at the snapshot |
|---|---|
| `grim/nohole`, `grim/eg` | 3 |
| `tft/nohole`, `tft/eg` | 3 |
| `tft/inf` | **1** |
| `grim/inf` | **0** |

`tft/inf` exists at one seed (train_seed 1, 48 episodes) and **enters no
contrast anywhere**; `grim/inf` has no episodes on disk. The hidden-horizon arm
carries the largest effects in the older one-seed data (−0.201, −0.246) and
remains **entirely unmeasured on traces**. Nothing in this log speaks to it.

## 12. Normalising the behaviour out: restrict to the final round

The penalty cuts late-betrayal behaviour, and it cuts the raw endgame markers.
Nothing above separates the second from the first: fewer turns spent walking
into a betrayal is fewer turns with anything endgame to say. Normalise the
behaviour out and see what survives.

The normalisation is a restriction, not a model. Take only **final-round
decision blocks** — `in_decision`, a parsed answer, `rounds_from_end == 0`.
Every episode has exactly one final round, so both arms contribute ~48 such
blocks per cell **regardless of how much late betrayal they actually commit**.
The denominator is matched by construction, so a difference here cannot be
composition. That is the whole point of the section.

**529** final-round decision blocks across the four contrast cells; per-cell
counts are 47–48 everywhere except `grim/nohole` s1, which contributes **15**
(the compromised cell of §8, 60.8% empty answers). Deltas formed **within** a
matched training seed and then averaged, SE between training seeds (n = 3).
Figure and numbers:
`results/0830_endgame_traces/fig4_normalised_by_behaviour.{png,json}` — quote
the JSON.

Behaviour on those blocks (`answer_defect` share), which is §6's unconditioned
row:

| opponent | `nohole` | `eg` | Δ |
|---|--:|--:|---|
| grim | 0.879 | 0.661 | **−0.217 ± 0.201** |
| tft | 0.965 | 0.560 | **−0.405 ± 0.276** |

Per-seed grim **+0.089, −0.146, −0.595**; per-seed tft
**−0.130, −0.128, −0.957**.

Reasoning on the same blocks, under three length adjustments — raw,
length-stratified to §3's global quintiles, and a logistic adjustment on
log-length read as a marginal effect at the pooled mean length:

| marker | opp | raw Δ | stratified Δ | logistic Δ |
|---|---|---|---|---|
| `endgame_defect_plan` | grim | −0.093 ± 0.075 | **−0.089 ± 0.047** | −0.077 ± 0.042 |
| `backward_induction` | grim | −0.040 ± 0.011 | −0.068 ± 0.109 | −0.069 ± 0.086 |
| `endgame_hold` | grim | +0.096 ± 0.056 | **+0.084 ± 0.047** | +0.071 ± 0.041 |
| `in_game_penalty` (FLOOR) | grim | +0.005 ± 0.112 | −0.054 ± 0.232 | −0.021 ± 0.222 |
| `endgame_defect_plan` | tft | +0.035 ± 0.064 | **−0.068 ± 0.043** | −0.074 ± 0.012 |
| `backward_induction` | tft | +0.001 ± 0.049 | **−0.089 ± 0.026** | −0.086 ± 0.003 |
| `endgame_hold` | tft | +0.092 ± 0.050 | **+0.049 ± 0.030** | +0.045 ± 0.034 |
| `in_game_penalty` (FLOOR) | tft | +0.180 ± 0.117 | +0.117 ± 0.089 | +0.116 ± 0.077 |

**The length control flips direction here, and that has to be said out loud.**
§3 established that pooled over all blocks the penalty *shortens* the reasoning
against `tft` (**−482 ± 212** chars) and that this carried 78% of the raw pooled
effect. At the final round the gap runs the other way: the `eg` arm writes
**longer** (tft **+218 ± 130**, grim **+327 ± 310** chars). So the raw
final-round number is flattered by length in the opposite direction, and
standardising moves the `tft` `endgame_defect_plan` estimate from +0.035 to
−0.068 rather than shrinking it toward zero. Three independent adjustments —
global quintiles, final-round-local quintiles, continuous logistic on log-length
— agree closely, which is the only reason this is reportable. (The `tft` raw
+0.035 is §5's final-round row exactly; grim's −0.093 against that table's
−0.125 is the parsed-answer requirement, which removes most of `grim/nohole`
s1.)

**The reasoning effect does not vanish under normalisation, but it is small.**
Roughly a third (grim) to a fifth (tft) of the behavioural move: behaviour
−0.217 and −0.405 against plan-to-betray −0.089 and −0.068.

**What survives is endgame-SPECIFIC, which the pooled §4 analysis could not
see.** `endgame_defect_plan` and `backward_induction` fall while `endgame_hold`
**rises** (+0.084 grim, +0.049 tft) and the generic `in_game_penalty` floor does
not fall at all (tft **+0.117 ± 0.089**, grim **−0.054 ± 0.232**). Opposite
signs on the two endgame markers with the floor flat or rising is a pattern
neither verbosity nor blanket suppression produces. It does not resurrect §6:
that a marker's *rate* moves between arms is a different claim from that
marker's presence predicting a given block's action, which it still does not.

**This is the internalisation signature that `0830-endgame-reasoning.md` §2 went
looking for and reported absent.** That log read `endgame_hold` *falling* as
evidence against internalisation; it was one seed, pooled over all blocks. At
the final round, on three seeds, it rises on both opponents.

**§4 is not overturned by this.** Its conclusion is correct for what it
measured: pooled over all 12,480 blocks, where turns with no endgame at stake
dominate the denominator, everything does fall together onto the floor. The
final-round restriction is a different conditioning of the same data and both
are correct for their own estimand. The pooled number is dominated by
non-endgame turns; the endgame-specific contrast only appears where the endgame
is live.

Sensitivity. Dropping the flagged cells (grim → seeds 0, 2; tft → seeds 1, 2):

| raw Δ | all 3 seeds | flagged cell dropped (n = 2) |
|---|---|---|
| `endgame_defect_plan`, grim | −0.093 | **−0.155** |
| `endgame_defect_plan`, tft | +0.035 | +0.055 |
| `endgame_hold`, grim | +0.096 | +0.093 |
| `endgame_hold`, tft | +0.092 | +0.049 |

**Same signs throughout.** Two seeds carry no usable SE, so none is quoted.

**The behaviour deltas in the first table are not the behavioural result.** They
carry ±0.201 and ±0.276 because each is driven by a single seed — `grim/eg` s2
defects on **0.385** of its final rounds, `tft/eg` s2 on **0.043**. The
behavioural result proper stands on the training logs (companion §1,
**−0.039 ± 0.012** and **−0.142 ± 0.064**), not on this eval. So "the reasoning
moves a fifth as much as the behaviour" is an order-of-magnitude statement and
**not a measured ratio**.

The rest of what this does not support. Several of these estimates are 1.5–2
sigma. The `backward_induction` tft logistic SE of **±0.003** is implausibly
small — three seeds happening to agree — so the primary quote there is the
stratified **−0.089 ± 0.026** and nothing should lean on the logistic SE. One
checkpoint (step 35), ipd only, horizons 6/10/14, and `grim/nohole` s1
contributes 15 blocks against 47–48 elsewhere. The claim is **a detectable
endgame-specific effect at the final round**, not a demonstrated mechanism, and
these intervals do not support an equivalence claim in either direction.

## 13. What to do next

1. **Get the `inf` arms.** Two `grim/inf` seeds and two more `tft/inf` seeds.
   This is the arm the wave most wants and the only one with no trace evidence
   at all.
2. **Fix the `invalid_rate` gate's blind spot.** The discriminating statistic is
   the **empty-answer rate on decision turns**, not `invalid_rate` (0.000 on the
   worst cell in the wave) and not block length (`tft/eg` s2 at 543 chars is
   *shorter* than the compromised cell and is fine). Gate on empty answers and
   count them somewhere.
3. **Investigate why the baseline arms produce more empty answers.** 27.2% and
   14.3% against 7.5% and 4.0%. If empty answers resolve to a default move, this
   bears on every behavioural number in the wave, in the direction of
   understating the penalty's effect.
4. **Treat length standardisation as standard practice for marker claims.** It
   removed 78% of the one number in this analysis that looked like a result, and
   at the final round it *flips* the sign of the `tft` estimate rather than
   shrinking it (§12), so the correction cannot be assumed conservative.
5. **Restate the wave's result.** The defensible summary is now: *the endgame
   penalty changes late-game behaviour, with no **endgame-specific** change
   detectable in the reasoning markers pooled over all turns and a small one at
   the final round, where the denominator is matched by construction (§12).* The
   pooled half is a dissociation and the final-round half is not; they are two
   conditionings of the same data and not a disagreement. Both want the `inf`
   arms and more seeds. Neither is strong: the pooled half is **"no detectable
   endgame-specific effect", not "proof of no effect"**, the final-round half
   rests on estimates of 1.5–2 sigma, and at n = 3 none of these bands supports
   an equivalence claim either.

---

Three notes against the working numbers for this analysis, all in favour of the
JSONs. The grim `nohole` spike amplitude is exactly 0.5625, written **+0.562**
here. Of the pooled estimates in §1–§4, `endgame_hold` against `tft` is the only
stratified delta that is positive **and clear of zero** — grim's `endgame_hold`
is also nominally positive at +0.001, which is zero. And the endgame spike is
not monotone into the final round in every arm: `tft/nohole` and, mildly,
`grim/eg` peak one round early, which is where `tft`'s +0.361 amplitude
difference comes from.
