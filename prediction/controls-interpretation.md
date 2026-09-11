All **420/420 control episodes** completed, with 840 focal records and no collection errors. The panel shows observed sensitivity: scaling is associated with higher mutual cooperation, and abstract text with lower canonical action0. Most broad-target contrast intervals include zero, which does not establish invariance. Forecast accuracy also varies by transformation: the fixed combined logistic model's action0 weakness relative to the payoff-dominant rule is concentrated in offset +10, where its raw-payoff-dependent forecasts shift. Historical pilot anchors, seven source shapes, and sparse conditional opportunities limit causal and generalization claims.

The primary score audit is prospective-verified with no issues; the independently supervised secondary comparison is verified and prospectively timed, completed at 09:24:55 UTC on 2026-09-10. Secondary methods remain post-pilot additions. Their seven split/target common-support counts match the original control evaluation. This document combines the audit performed while rollouts were running with final empirical interpretation after collection and verification. Sources: [final collection](results/overnight-20260910/controls/collected/summary.json), [primary timing/identity audit](results/overnight-20260910/controls/evaluation/audit.json), [verified secondary supervisor audit](results/overnight-20260910/secondary-baselines/full/controls-comparison/supervisor-audit.json).

The controls test scale ×3, offset +10, and abstract text on the first seven source games of the primary pilot. Each transformation preserves the source game's canonical group, family, Nash profiles, and measurement applicability. The numerical transformation checks pass against the actual original payoffs: scale multiplies all four values by three, offset adds ten to all four, and abstract text retains the exact values. Source: [control manifest](results/overnight-20260910/controls/manifest.json), [primary pilot manifest](results/overnight-20260910/primary-pilot-manifest.json).

| Original source | Family | Control variants |
|---|---|---|
| pilot-g0000 | Prisoner's dilemma | Scale ×3, offset +10, abstract text |
| pilot-g0001 | Stag hunt | Scale ×3, offset +10, abstract text |
| pilot-g0002 | Chicken | Scale ×3, offset +10, abstract text |
| pilot-g0003 | Harmony | Scale ×3, offset +10, abstract text |
| pilot-g0004 | Equal-diagonal coordination | Scale ×3, offset +10, abstract text |
| pilot-g0005 | Equal-diagonal anti-coordination | Scale ×3, offset +10, abstract text |
| pilot-g0006 | Weak dominance | Scale ×3, offset +10, abstract text |

There are **seven source-game clusters**, represented by 21 presented game variants. Structurally, action0 has seven structurally eligible source shapes, mutual cooperation five, coordination four, and asymmetric extraction two. Each family contributes only one source shape, so this panel cannot establish a distribution of family-specific sensitivity. The source shapes were already part of the 72-game predictor training data. Control forecasts are prospective for new transformed episodes on known shapes, not a test on previously unseen game structures. Sources: [control metadata](results/overnight-20260910/controls/metadata.json), [fixed predictor training records](results/overnight-20260910/training-records.json).

The planned player protocol matches the primary pilot exactly: four model specifications, eight rounds, temperature 0.7, complete public history, undisclosed opponent identity, and the own-cumulative-points objective. The source hashes also match. Each presented variant has all ten unordered model pairs, including four self-play pairs, with trials 0 and 1. Trial 0 is unswapped and trial 1 swapped. Thus the 420 planned episodes contain 168 self-play and 252 cross-play episodes, 210 episodes per display condition, and 840 focal records, 210 for each model. The metadata contain exactly two reciprocal focal roles per episode and no outcome targets. Their identity hash matches the frozen forecast manifests. Source: [manifest and planned episode schedule](results/overnight-20260910/controls/manifest.json), [metadata provenance](results/overnight-20260910/controls/metadata.manifest.json).

The independent freeze audit verified every one of the five primary freeze hashes and all 17 artifacts tracked by the secondary freeze. It also checked the secondary plan hash and its bindings to the control manifest, metadata, and training records. The recorded times are:

| Event | UTC on 2026-09-10 |
|---|---|
| Secondary control forecasts completed | 07:19:40.747007 |
| Secondary forecasts frozen | 07:19:57.430168 |
| Primary control forecasts completed | 08:53:18.893562 |
| Primary control forecasts frozen | 08:53:19.521133 |
| Earliest saved control trace start | 08:53:22.983744 |

Both sets of forecasts precede the final collection's earliest rollout start. The primary fit is the already-frozen full numerical training fit; it was not refitted for the controls. The secondary methods remain explicitly post-pilot additions, even though their control forecasts were frozen before these outcomes. These timestamp/hash checks use saved local evidence rather than external notarization; both final scorers independently verified the complete collection before these scores were interpreted. Sources: [primary forecast freeze](results/overnight-20260910/controls/forecast-freeze.json), [primary forecast provenance](results/overnight-20260910/controls/forecasts.manifest.json), [secondary freeze](results/overnight-20260910/secondary-baselines/forecast-freeze.json), [secondary control provenance](results/overnight-20260910/secondary-baselines/full/controls.manifest.json).

The matched sensitivity estimand differs from forecast accuracy on all completed control episodes. It compares each transformed condition with the original pilot using the same source game × focal model × opponent cells, requiring both transformed trials and all four original trials. Original pilot-g0002 lacks GPT OSS 20B × Kimi K3 trial 1. Both ordered focal contexts for that pair are therefore incomplete, leaving **110 of 112** original ordered contexts eligible for the unconditional design comparison. No control episodes are incomplete. Target-specific absence of opportunities reduces support further. Conditional comparisons require positive pooled opportunities in both conditions; they do not replace unsupported or unobserved histories with zero. Sources: [immutable pilot records](results/overnight-20260910/primary-pilot/final-records.json), [exact sensitivity rules](controls_analysis.md).

Within a source game, sensitivity rates pool successes and opportunities across matched cells; changes are then averaged with equal source-game weight. The contrast direction is transformed minus original. Both focal rows, all rounds, original counts, and transformed counts remain together in the paired game-cluster bootstrap. Original outcomes are reused across variants, so the three estimated contrasts are dependent. The original uses four trials versus two transformed trials; requests were independently sampled rather than paired by random seed. **The matrix anchors are historical pilot episodes collected several hours earlier, not concurrently randomized untransformed controls.** There is no same-randomness rerun and no guarantee that serving conditions or model behavior remained unchanged. Matching game and model/opponent context does not remove possible temporal drift. The differences therefore measure observed sensitivity under this schedule, combining presentation, finite-repeat, and request/calendar variation rather than identifying an isolated causal transformation effect. Conditional opponent behavior and opportunity composition can also change between conditions, so conditional differences do not isolate a response mechanism. Source: [estimands and derivation contract](controls_analysis.md).

Affine transformations preserve the strategic ordering under the fixed cumulative-points objective, but observed choice need not be invariant. Offset +10 also removes negative numbers in this panel, whereas scale ×3 preserves their signs. Abstract text preserves payoffs while changing their presentation. Canonical action0 is measured after undoing display swaps, so a change is not the mechanical result of relabeling the displayed actions. The completed pilot's separate label analysis is described in [pilot-interpretation.md](pilot-interpretation.md); it has a different two-versus-two-trial contrast and should not be conflated with these transformations.

Forecast error is distinct from player sensitivity. The combined predictor includes raw-payoff features that change under scale and offset even when the strategic ordering is preserved; its frozen probabilities can therefore shift or fail even if player behavior remains stable. A structural or equilibrium predictor may retain invariant probabilities while players change. The results below distinguish observed behavior changes from frozen-predictor sensitivity.

The outcome-free forecast audit confirms this distinction. Matching source game, focal model, opponent, role, and trial, the fixed combined-logistic forecasts have the following mean absolute probability changes from the untransformed-payoff forecast. The reference is the saved abstract-text forecast: these numerical methods omit presentation format, and abstract text retains the original payoff values. The statistic averages matched forecast rows within source game and then weights source games equally. It is a deterministic comparison of frozen probabilities, with no control outcomes or forecast-error scores.

| Target | Eligible source games | Scale ×3 probability change | Offset +10 probability change |
|---|---:|---:|---:|
| Action0 | 7 | 0.08618 | 0.09459 |
| Mutual cooperation | 5 | 0.01134 | 0.00642 |
| Coordination | 4 | 0.00935 | 0.04479 |

Structural-logistic, original Nash, family, and ordered-context forecasts are unchanged up to floating-point tolerance on the same comparisons. These differences describe predictor sensitivity, not observed player sensitivity or prediction accuracy. Source hashes and per-game matched forecast counts are retained in the independent [frozen forecast sensitivity derivation](controls-forecast-sensitivity.json).

No equivalence margin was specified. Small estimated changes, intervals spanning zero, or successful forecast scores do not establish behavioral invariance. Large mean absolute game changes also contain sampling noise. The empirical tables retain each target's eligible games, matched cells, and opportunity denominators; the forecast and matched-sensitivity supports remain distinct.

**Observed matched sensitivity**

Changes below are transformed minus original, using equal source-game weight on the same matched contexts in both conditions. G is eligible source-game clusters, C matched ordered contexts, and N original/control focal opportunities. Intervals are saved 95% percentile intervals from 500 paired source-game bootstrap resamples; they are descriptive, unadjusted for the many targets/models/variants, and do not account for temporal drift. Full eligible episode counts and exact sufficient counts remain in the [sensitivity summary](results/overnight-20260910/controls/sensitivity/controls-analysis.json) and [per-game/cell derivation](results/overnight-20260910/controls/sensitivity/derivation.json).

| Variant | Target | G / C | Original → control rate | N original / control | Change [95% CI] |
|---|---|---:|---:|---:|---:|
| Scale ×3 | Action0 | 7 / 110 | 0.3808 → 0.3810 | 4416 / 2208 | +0.0001 [-0.0346, +0.0415] |
| Scale ×3 | First action0 | 7 / 110 | 0.4956 → 0.4683 | 552 / 276 | -0.0274 [-0.0696, +0.0164] |
| Scale ×3 | Mutual cooperation | 5 / 78 | 0.6483 → 0.6918 | 3136 / 1568 | +0.0435 [+0.0106, +0.0923] |
| Scale ×3 | Coordination | 4 / 62 | 0.7674 → 0.7304 | 2496 / 1248 | -0.0371 [-0.0835, +0.0094] |
| Scale ×3 | D after opponent D | 3 / 32 | 0.5773 → 0.3962 | 673 / 307 | -0.1811 [-0.4000, -0.0537] |
| Scale ×3 | Forgiveness | 2 / 19 | 0.3235 → 0.3734 | 58 / 36 | +0.0498 [-0.0714, +0.1711] |
| Scale ×3 | Asymmetric extraction | 2 / 28 | 0.5674 → 0.4734 | 418 / 245 | -0.0940 [-0.1437, -0.0444] |
| Offset +10 | Action0 | 7 / 110 | 0.3808 → 0.3631 | 4416 / 2208 | -0.0177 [-0.0515, +0.0042] |
| Offset +10 | First action0 | 7 / 110 | 0.4956 → 0.4341 | 552 / 276 | -0.0615 [-0.1444, -0.0147] |
| Offset +10 | Mutual cooperation | 5 / 78 | 0.6483 → 0.6344 | 3136 / 1568 | -0.0139 [-0.0422, +0.0087] |
| Offset +10 | Coordination | 4 / 62 | 0.7674 → 0.7724 | 2496 / 1248 | +0.0049 [-0.0164, +0.0375] |
| Offset +10 | D after opponent D | 4 / 35 | 0.3885 → 0.5162 | 679 / 387 | +0.1277 [-0.1878, +0.5622] |
| Offset +10 | Forgiveness | 2 / 14 | 0.3269 → 0.2861 | 50 / 29 | -0.0409 [-0.1154, +0.0337] |
| Offset +10 | Asymmetric extraction | 2 / 27 | 0.5804 → 0.7389 | 412 / 182 | +0.1585 [-0.0321, +0.3491] |
| Abstract text | Action0 | 7 / 110 | 0.3808 → 0.3361 | 4416 / 2208 | -0.0447 [-0.1011, -0.0029] |
| Abstract text | First action0 | 7 / 110 | 0.4956 → 0.4607 | 552 / 276 | -0.0349 [-0.0961, +0.0167] |
| Abstract text | Mutual cooperation | 5 / 78 | 0.6483 → 0.6479 | 3136 / 1568 | -0.0004 [-0.0450, +0.0472] |
| Abstract text | Coordination | 4 / 62 | 0.7674 → 0.7564 | 2496 / 1248 | -0.0110 [-0.0783, +0.0562] |
| Abstract text | D after opponent D | 3 / 34 | 0.5180 → 0.4443 | 677 / 369 | -0.0737 [-0.2222, +0.0122] |
| Abstract text | Forgiveness | 2 / 16 | 0.3066 → 0.2083 | 52 / 22 | -0.0983 [-0.1304, -0.0661] |
| Abstract text | Asymmetric extraction | 2 / 26 | 0.5569 → 0.6310 | 407 / 189 | +0.0742 [-0.1098, +0.2581] |

The complete matched action comparison has **276 original episodes versus 138 transformed episodes per variant**; mutual cooperation has 196/98 and coordination 156/78. Each transformed variant actually has 140 complete episodes, but the two episodes in the incomplete original GPT OSS/Kimi context are excluded from matching. The opposite focal rows remain dependent. Consequently, the matched action total is 2,208 opportunities per variant while the full forecast evaluation has 2,240. Different supports should not be silently interchanged.

Scaling raises aggregate mutual cooperation by **0.0435 [0.0106, 0.0923]**, from 0.6483 to 0.6918 on five source shapes. The per-game changes are nonnegative in this panel, but the largest is the Chicken source (+0.1424); Harmony is unchanged at its ceiling. The overall canonical action0 change is almost zero, while the mean absolute game change is 0.0345. Cancellation of changes across games and finite-repeat noise therefore coexist with a near-zero aggregate change. Scaling coordination falls by 0.0371 with an interval spanning zero. These results do not show universal affine invariance or a general causal effect of higher point stakes.

Abstract text lowers aggregate action0 by **0.0447 [0.0029, 0.1011]** in magnitude. Its largest source-game shift is equal-diagonal coordination (−0.1891), followed by PD (−0.0984). In the equal-diagonal coordination source, occupancy of a coordinated equilibrium changes less, from 0.9719 to 0.9125 (−0.0594). Canonical action0 partly tracks an arbitrary convention between equal-payoff equilibria, so its decrease cannot be read as a general loss of cooperation or welfare. Aggregate mutual cooperation under text changes by only −0.0004 with a wide interval. Offset +10's broad full-trajectory changes are uncertain, though first action0 falls by **0.0615 [0.0147, 0.1444]**. Sources: [saved sensitivity effects](results/overnight-20260910/controls/sensitivity/controls-analysis.json), [source-game effects](results/overnight-20260910/controls/sensitivity/derivation.json).

The model-associated broad changes show why an aggregate can conceal opposing responses. Each entry below is a signed change with its saved interval. Action/cooperation/coordination use seven/five/four eligible source shapes. For Claude and Qwen the original/control opportunity counts are respectively 1,120/560, 800/400, and 640/320. For GPT OSS and Kimi they are 1,088/544, 768/384, and 608/304 because the incomplete historical Chicken context is excluded. Outcomes such as cooperation and coordination are shared dyadic outcomes; these are not isolated traits or independent model comparisons. Source: [model-specific sensitivity and support](results/overnight-20260910/controls/sensitivity/controls-analysis.json).

| Variant | Focal model | Action0 change [CI] | Cooperation change [CI] | Coordination change [CI] |
|---|---|---:|---:|---:|
| Scale ×3 | Claude Haiku 4.5 | -0.0089 [-0.0746, +0.0442] | +0.0363 [+0.0063, +0.0688] | -0.0813 [-0.1891, -0.0187] |
| Scale ×3 | GPT OSS 20B | +0.0283 [-0.0134, +0.0863] | +0.0666 [+0.0312, +0.0906] | -0.0246 [-0.0867, +0.0395] |
| Scale ×3 | Kimi K3 | +0.0270 [-0.0313, +0.1199] | +0.0650 [-0.0244, +0.2069] | -0.0617 [-0.1328, +0.0094] |
| Scale ×3 | Qwen 3.8 27B | -0.0384 [-0.0665, -0.0143] | +0.0125 [-0.0200, +0.0450] | +0.0156 [-0.0375, +0.0687] |
| Offset +10 | Claude Haiku 4.5 | -0.0411 [-0.0946, +0.0005] | -0.0112 [-0.0463, +0.0175] | -0.0312 [-0.0641, -0.0125] |
| Offset +10 | GPT OSS 20B | +0.0203 [-0.0170, +0.0569] | -0.0141 [-0.0625, +0.0375] | -0.0035 [-0.1121, +0.1078] |
| Offset +10 | Kimi K3 | -0.0190 [-0.0770, +0.0194] | -0.0325 [-0.0838, +0.0019] | +0.0484 [-0.0141, +0.1438] |
| Offset +10 | Qwen 3.8 27B | -0.0295 [-0.0781, +0.0205] | +0.0025 [-0.0275, +0.0363] | +0.0094 [-0.0812, +0.1000] |
| Abstract text | Claude Haiku 4.5 | -0.0929 [-0.2260, -0.0035] | -0.0163 [-0.0488, +0.0025] | -0.0281 [-0.0594, +0.0031] |
| Abstract text | GPT OSS 20B | +0.0092 [-0.0764, +0.1097] | +0.0328 [-0.0513, +0.1191] | -0.0043 [-0.1582, +0.1031] |
| Abstract text | Kimi K3 | -0.0475 [-0.0903, -0.0137] | -0.0369 [-0.0838, +0.0088] | +0.0250 [-0.0312, +0.0953] |
| Abstract text | Qwen 3.8 27B | -0.0438 [-0.0893, -0.0040] | +0.0200 [-0.0238, +0.0675] | -0.0406 [-0.1438, +0.0625] |

Conditional targets are considerably less stable. Scaling's post-defection decline (−0.1811) averages only three source games. One-third of that equal-game average comes from weak dominance, whose conditional rate falls from 2/5 to 0/2 opportunities; this is an especially small count behind a large per-game change of −0.4. Text's forgiveness decline (−0.0983) has a negative interval but only two source games, **52 original versus 22 control opportunities**, and 39 versus 19 eligible episodes. Scaling forgiveness uses 58/36 opportunities, offset forgiveness 50/29; all are selected subsets with observed histories on both sides. Extraction likewise has only two source games. Intervals that exclude zero here reflect the sampled game differences, not broad support for a causal forgiving or retaliatory mechanism. The largest conditional changes should be read alongside their sparse denominators, changed opponent behavior, and history-selection rules. Sources: [conditional per-game counts](results/overnight-20260910/controls/sensitivity/derivation.json), [measurement semantics](measurements.md).

**Prospectively timed control forecasts**

These scores pool all three variants within the seven canonical source groups, retaining the original all-method common observations. Event scores pool opportunities within group and then weight groups equally. Broad support is seven action groups/420 episodes/6,720 focal opportunities; five cooperation groups/300 episodes/4,800 opportunities; four coordination groups/240 episodes/3,840 opportunities. There were no missing planned outcomes or unforecast planned focal rows. The table reports **Brier / log loss / ECE**. Logistic and MLP are the fixed combined models with both identities. Sources: [primary coverage](results/overnight-20260910/controls/evaluation/coverage.json), [verified augmented scores](results/overnight-20260910/secondary-baselines/full/controls-comparison/scores.json).

| Target | Ordered context | Original Nash | Payoff-dominant | Family mean | Structural logistic | Combined logistic | Combined MLP |
|---|---:|---:|---:|---:|---:|---:|---:|
| Action0 | 0.2508 / 0.6948 / 0.1450 | 0.1826 / 0.7368 / 0.2000 | 0.1396 / 0.6426 / 0.1161 | 0.2273 / 0.6462 / 0.2372 | 0.1391 / 0.4246 / 0.1029 | 0.1530 / 0.4589 / 0.1475 | 0.1304 / 0.4040 / 0.0773 |
| Mutual cooperation | 0.2242 / 0.6405 / 0.0125 | 0.1589 / 0.6219 / 0.1847 | 0.0732 / 0.4571 / 0.0578 | 0.0667 / 0.2273 / 0.0191 | 0.0684 / 0.2341 / 0.0318 | 0.0660 / 0.2265 / 0.0268 | 0.0668 / 0.2277 / 0.0312 |
| Coordination | 0.1854 / 0.5576 / 0.0058 | 0.2536 / 0.7028 / 0.2886 | 0.1627 / 0.6399 / 0.0939 | 0.1397 / 0.4175 / 0.0065 | 0.1407 / 0.4204 / 0.0217 | 0.1412 / 0.4257 / 0.0357 | 0.1406 / 0.4597 / 0.0282 |

Against the original ordered-context baseline, logistic's pooled Brier gains are positive with saved paired intervals: action **+0.0978 [0.0231, 0.1663]**, cooperation **+0.1583 [0.0912, 0.2691]**, coordination **+0.0441 [0.0269, 0.0684]**. The comparisons are much more qualified against the stronger secondary equilibrium selector. Logistic's Brier gains are −0.0134 [−0.0556, 0.0186], +0.0072 [−0.0033, 0.0218], and +0.0214 [−0.0041, 0.0632] respectively; all span zero. MLP's corresponding Brier gains also all have intervals spanning zero. Cooperation/coordination log-loss gains over payoff-dominant are positive for both learned methods; logistic's are +0.2306 [0.0408, 0.4611] and +0.2142 [0.0277, 0.4661], with lower point ECE. Action log-loss gains are uncertain. These game-then-episode bootstrap intervals use 500 resamples and fixed forecasts, with no refitting uncertainty or multiplicity adjustment. Source: [saved paired comparisons](results/overnight-20260910/secondary-baselines/full/controls-comparison/secondary-comparisons.json).

As in development, the known-family rate nearly matches learned cooperation and coordination. Family Brier is 0.0667/0.1397 versus logistic 0.0660/0.1412, with similar log loss and lower point ECE. The control results therefore support useful forecasting relative to an opponent-context prior, but not a claim that sophisticated continuous-payoff learning is necessary for these broad outcomes. The source shapes were present during fitting, which further limits generalization claims.

To attribute error to a particular presentation, the following **secondary descriptive per-variant breakdown** was computed only from saved joined predictions after both audits passed. It reproduces all 51 pooled broad-target method scores before splitting by the manifest variant, preserves the exact original all-method support, and reports points without new uncertainty intervals or refitting. Each variant has seven/five/four supported shape groups, 140/100/80 episodes, and 2,240/1,600/1,280 opportunities for action/cooperation/coordination. Entries are **Brier / log loss**. Source hashes, method support, and original prediction keys are saved in the independent [variant scores](results/overnight-20260910/independent-analysis/control-variant-breakdown/scores.json), [derivation](results/overnight-20260910/independent-analysis/control-variant-breakdown/derivation.json), and [reproduction code](results/overnight-20260910/independent-analysis/control-variant-breakdown/analysis.py).

| Variant | Target | Payoff-dominant | Family mean | Raw logistic | Structural logistic | Combined logistic | Combined MLP |
|---|---|---:|---:|---:|---:|---:|---:|
| Scale ×3 | Action0 | 0.1488 / 0.7336 | 0.2285 / 0.6487 | 0.2009 / 0.7588 | 0.1398 / 0.4230 | 0.1483 / 0.4507 | 0.1245 / 0.3916 |
| Scale ×3 | Mutual cooperation | 0.0802 / 0.4602 | 0.0691 / 0.2228 | 0.2195 / 0.6290 | 0.0717 / 0.2315 | 0.0660 / 0.2207 | 0.0684 / 0.2279 |
| Scale ×3 | Coordination | 0.1471 / 0.5401 | 0.1389 / 0.4061 | 0.2079 / 0.7660 | 0.1416 / 0.4139 | 0.1409 / 0.4183 | 0.1395 / 0.5173 |
| Offset +10 | Action0 | 0.1354 / 0.5953 | 0.2259 / 0.6434 | 0.2153 / 0.6185 | 0.1411 / 0.4278 | 0.1760 / 0.5069 | 0.1375 / 0.4157 |
| Offset +10 | Mutual cooperation | 0.0652 / 0.4375 | 0.0632 / 0.2282 | 0.2090 / 0.6088 | 0.0637 / 0.2293 | 0.0618 / 0.2186 | 0.0622 / 0.2163 |
| Offset +10 | Coordination | 0.1693 / 0.6782 | 0.1398 / 0.4254 | 0.2259 / 0.6528 | 0.1390 / 0.4210 | 0.1418 / 0.4296 | 0.1395 / 0.4248 |
| Abstract text | Action0 | 0.1347 / 0.5988 | 0.2275 / 0.6466 | 0.1701 / 0.5138 | 0.1364 / 0.4231 | 0.1348 / 0.4191 | 0.1293 / 0.4046 |
| Abstract text | Mutual cooperation | 0.0741 / 0.4737 | 0.0679 / 0.2310 | 0.1905 / 0.5609 | 0.0698 / 0.2415 | 0.0700 / 0.2402 | 0.0699 / 0.2388 |
| Abstract text | Coordination | 0.1716 / 0.7016 | 0.1403 / 0.4211 | 0.1663 / 0.4910 | 0.1416 / 0.4263 | 0.1411 / 0.4292 | 0.1428 / 0.4371 |

The pooled logistic action deficit relative to payoff-dominant is concentrated in **offset +10**: Brier 0.175953 versus 0.135376, a descriptive deficit of 0.040577, compared with near-ties for scale (0.1483 versus 0.1488) and text (0.1348 versus 0.1347). Structural-logistic action Brier remains about 0.1398/0.1411/0.1364 across scale/offset/text. The saved frozen probabilities show why predictor sensitivity must be considered: offset raises logistic action0 probabilities by about 0.0946 on the planned panel, while matched historical-to-offset behavior changes by −0.0177. These figures have different forecast/matching supports and are not a causal decomposition of score error, but they provide direct evidence of an affine-sensitive predictor alongside comparatively small aggregate observed action change. Large raw-logistic forecast sensitivity also accompanies poorer cooperation/coordination scores, especially under offset; it should not be mistaken for proof that players changed by a corresponding amount.

Text action prediction is comparatively accurate despite its observed historical action shift. Logistic and payoff-dominant nearly tie on Brier, with logistic lower on log loss. Conversely, scaling changes observed cooperation while its logistic forecast changes relatively little and remains accurate. Forecast accuracy and behavioral invariance therefore answer different questions. Per-variant point differences have not received additional uncertainty tests; no new method is chosen from this breakdown. Sources: [variant scores](results/overnight-20260910/independent-analysis/control-variant-breakdown/scores.json), [outcome-free forecast changes](controls-forecast-sensitivity.json), [matched observed effects](results/overnight-20260910/controls/sensitivity/controls-analysis.json).

Conditional forecast support is also larger than matched sensitivity support because it does not require a historical opportunity in both conditions. Across all variants the scorer retains four groups/131 eligible episodes/1,101 post-defection opportunities; three/63/95 forgiveness opportunities; and two/107/667 extraction opportunities. Logistic's Brier gains over the event-weighted secondary context are +0.0681 [−0.0050, 0.1424], +0.0241 [−0.0070, 0.0685], and +0.0313 [−0.0028, 0.0707] respectively. All span zero, as do their log-loss gain intervals. These prospective observations do not establish dependable conditional-mechanism prediction on this small control panel. Source: [conditional support and comparisons](results/overnight-20260910/secondary-baselines/full/controls-comparison/scores.json).

The controls provide evidence of observed presentation sensitivity and expose an offset-related weakness of the fixed logistic action predictor. They also retain useful broad-target forecast accuracy relative to the original context baseline. They do not establish equivalence across presentations, isolate transformation effects from historical drift, demonstrate a learned advantage over every simple behavioral comparator, or justify extrapolation to new strategic families. No forecasts, fitted models, supervised outputs, API calls, or study gates were changed in this interpretation.
