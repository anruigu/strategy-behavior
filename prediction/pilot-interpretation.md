# Interpretation of the completed primary pilot

The pilot contains reproducible differences in aggregate action choice, mutual cooperation, and coordination across its sampled games. It also shows substantial model/context noise and sharply uneven support for conditional behavior. These observations justify evaluating prespecified predictors on held-out games; they do not establish that payoff features predict unseen games, that learned predictors beat baselines, or that the conditional statistics identify retaliatory or forgiving intentions.

This interpretation uses the immutable [final records](results/overnight-20260910/primary-pilot/final-records.json) and their [final diagnostics](results/overnight-20260910/primary-pilot/diagnostics/diagnostics.json), available on 2026-09-10. Both the semantic record digest and the source-file SHA-256 in the diagnostics match the immutable records. No numerical forecast scores were consulted.

## Coverage and dependence

There are **958 of 960 planned complete episodes (99.79%)**, 1,916 focal-player records, 24 games, 24 distinct game-shape groups, four models, and seven canonical families. Every retained focal record covers eight rounds, giving 7,664 joint rounds and 15,328 focal action opportunities. The two focal rows from an episode are dependent; mutual cooperation and coordination are identical between those rows. Neither the focal-row count nor an opportunity total is an independent sample size.

| Focal model | Episodes involving model / 384 planned | Focal records / 480 planned |
|---|---:|---:|
| Claude Haiku 4.5 | 384 | 480 |
| GPT OSS 20B | 383 | 479 |
| Kimi K3 | 382 | 477 |
| Qwen 3.8 27B | 384 | 480 |

The missing cells reconstructed from the balanced design are pilot-g0002, GPT OSS 20B × Kimi K3, trial 1; and pilot-g0009, Kimi K3 self-play, trial 3. Both games are Chicken variants. This reconstruction identifies absent observations, not their failure mechanism. Both missing episodes used swapped labels: the final collection has 480 unswapped and 478 swapped episodes. The balanced split-half calculations exclude the affected three ordered focal-model/opponent cells, leaving 381 of 384 cells for unconditional action measures. Thus the reported agreement does not compare an unbalanced surviving three-trial cell with a complete four-trial cell.

These are 24 numerical game shapes, not 24 independent game families. Family-specific conclusions rest on only three or four shapes.

## What varies across games, families, and models

All rates below pool counts within each eligible game and then weight games equally. NA denotes a structurally unsupported target or no observed opportunities; it is never a zero rate. The definitions are fixed in [measurements.md](measurements.md). In particular, cooperation means the frequency of the mutually cooperative outcome, whereas individual cooperation counts the focal cooperative action. Coordination means occupancy of an admissible strict pure equilibrium in games with multiple such equilibria; it includes anti-coordination outcomes.

| Family | Games | Episodes | Mutual cooperation | Individual cooperation | Coordination |
|---|---:|---:|---:|---:|---:|
| Prisoner's Dilemma | 4 | 160 | 0.085 | 0.195 | NA |
| Stag Hunt | 4 | 160 | 0.973 | 0.984 | 0.977 |
| Chicken | 4 | 158 | 0.274 | 0.531 | 0.514 |
| Harmony | 3 | 120 | 1.000 | 1.000 | NA |
| Equal-diagonal coordination | 3 | 120 | NA | NA | 0.959 |
| Equal-diagonal anti-coordination | 3 | 120 | NA | NA | 0.599 |
| Weak dominance | 3 | 120 | 0.968 | 0.983 | NA |

The strongest descriptive variation is between strategic settings: mutual cooperation is nearly universal in Harmony, Stag Hunt, and weak-dominance games, but uncommon in PD and much lower in Chicken. The absence of a privileged cooperative action in the equal-diagonal families is a semantic applicability decision; their NA cooperation entries do not show antisocial behavior. The gap between mutual and individual cooperation in Chicken reflects asymmetric outcomes. Anti-coordination's lower coordination rate refers to achieving the asymmetric strict equilibria, not matching action labels.

Across individual games, mutual cooperation ranges from 0.031 to 1.000; coordination ranges from 0.463 to 0.994. Canonical action0 ranges from 0 to 1 across games even though its aggregate rate is 0.496. The aggregate near one-half does not imply random choice: which canonical action is attractive changes across game orientations, and display labels are counterbalanced separately.

| Focal model | Action0 (24 games) | Mutual cooperation (18 games) | Individual cooperation (18 games) | Coordination (14 games) |
|---|---:|---:|---:|---:|
| Claude Haiku 4.5 | 0.519 | 0.667 | 0.783 | 0.764 |
| GPT OSS 20B | 0.470 | 0.581 | 0.666 | 0.755 |
| Kimi K3 | 0.492 | 0.637 | 0.714 | 0.757 |
| Qwen 3.8 27B | 0.500 | 0.611 | 0.678 | 0.764 |

Coordination differs little across these pooled model summaries, while individual cooperation differs more. Mutual cooperation is an outcome of a dyad, so these are model-associated outcomes averaged over the sampled opponents, not isolated traits of the focal model. The table provides descriptive contrasts without model-ranking significance tests. Opponent composition and self-play contributions are retained in the underlying counts.

## Support for each target

G counts games with at least one eligible observation; E counts distinct episodes containing an eligible focal observation; N counts focal opportunities. These are full-collection support counts, which can exceed the subset retained for balanced split-half agreement.

| Target | Eligible G | Eligible E | Eligible focal rows | N | Equal-game rate | Pooled-event rate |
|---|---:|---:|---:|---:|---:|---:|
| Action0 | 24 | 958 | 1,916 | 15,328 | 0.496 | 0.495 |
| First action0 | 24 | 958 | 1,916 | 1,916 | 0.510 | 0.509 |
| Mutual cooperation | 18 | 718 | 1,436 | 11,488 | 0.624 | 0.625 |
| Individual cooperation | 18 | 718 | 1,436 | 11,488 | 0.711 | 0.711 |
| Retaliation: D after opponent D | 15 | 332 | 631 | 2,824 | 0.448 | 0.707 |
| Forgiveness | 11 | 205 | 253 | 295 | 0.366 | 0.288 |
| Coordination | 14 | 558 | 1,116 | 8,928 | 0.760 | 0.761 |
| Exploitation | 8 | 304 | 532 | 1,842 | 0.537 | 0.505 |
| Defection after opponent cooperation | 18 | 700 | 1,324 | 7,228 | 0.268 | 0.141 |
| Defection after mutual cooperation | 18 | 575 | 1,150 | 6,372 | 0.151 | 0.055 |
| Defection after focal C / opponent D | 15 | 311 | 425 | 856 | 0.480 | 0.525 |

No target fields are missing from the collection. Cooperation-related semantics are unsupported in 480 focal rows, coordination in 800, and exploitation in 1,280. These structural exclusions differ from applicable-but-unobserved histories.

**Conditional composition is a material limitation.** The pooled retaliation rate is 0.707, but its equal-game mean is 0.448. PD contributes 1,767 of 2,824 retaliation opportunities and Chicken another 998; Stag Hunt contributes only 34 and weak dominance 25. Harmony has no such observed events. Thus pooled and macro rates answer different questions rather than contradicting each other.

Forgiveness has only 295 opportunities: 153 in Chicken, 131 in PD, eight in Stag Hunt, and three in weak dominance. The weak-dominance macro rate of 1.000 comes from just three successes in one eligible game and two episodes. It is not evidence of a reliable forgiving strategy. Model-specific forgiveness support also differs: Claude has 50 opportunities across nine games; GPT OSS 89 across 11; Kimi 91 across ten; Qwen 65 across nine. Their macro rates (0.531, 0.317, 0.402, and 0.198) therefore should not be treated as a clean ranking on a common opportunity distribution.

Exploitation is defined only in the four PD and four Chicken games. It records an action with unilateral self-gain, opponent harm relative to the alternate focal action, and a realized payoff advantage. It does not infer exploitation of a predictable opponent or strategic intent; mutual DD in PD is excluded. Its model macro rates range from 0.350 for Claude to 0.693 for Qwen, with 436–475 opportunities per model across these eight games. Changing opponents and histories still changes which extraction opportunities occur.

## Balanced split-half repeatability

Halves are trials 0/1 versus 2/3: each contains one standard and one swapped display. Cells require all four trials, matching label composition, and positive target opportunities in both halves. Cell statistics weight games equally, and game statistics pool the same eligible cells on each side. Intervals below are 95% percentile intervals from 300 game-shape cluster bootstrap replicates. They are descriptive and unadjusted for multiple targets.

| Target | Paired games | Game r [95% CI] | Game MAE | Paired cells | Cell r [95% CI] | Cell MAE |
|---|---:|---|---:|---:|---|---:|
| Action0 | 24 | 0.996 [0.990, 0.999] | 0.024 | 381 | 0.878 [0.770, 0.944] | 0.109 |
| First action0 | 24 | 0.986 [0.974, 0.995] | 0.040 | 381 | 0.750 [0.594, 0.860] | 0.151 |
| Mutual cooperation | 18 | 0.994 [0.987, 0.999] | 0.029 | 285 | 0.949 [0.913, 0.973] | 0.069 |
| Individual cooperation | 18 | 0.997 [0.993, 0.999] | 0.019 | 285 | 0.947 [0.891, 0.972] | 0.063 |
| Retaliation | 12 | 0.633 [−0.081, 0.997] | 0.134 | 129 | 0.549 [0.040, 0.895] | 0.207 |
| Forgiveness | 9 | 0.936 [0.567, 0.995] | 0.070 | 63 | 0.384 [−0.181, 0.709] | 0.257 |
| Coordination | 14 | 0.951 [0.892, 0.990] | 0.053 | 221 | 0.737 [0.591, 0.825] | 0.117 |
| Exploitation | 8 | 0.615 [−0.601, 0.959] | 0.078 | 115 | 0.510 [0.419, 0.611] | 0.244 |

Action choice, cooperation, and coordination have stable pooled game profiles in this sample. Aggregation reduces noise: the higher game-level correlations do not imply that every model/opponent cell is equally stable. First-action cell MAE is 0.151, despite game r of 0.986. Forgiveness is the clearest warning: a game r of 0.936 on nine selected games coexists with cell r of 0.384, a confidence interval spanning zero, and cell MAE of 0.257. Its aggregate correlation should not certify reliable pair-specific forgiveness.

Retaliation and exploitation game-level intervals are very wide and include zero. Their cell-level positive correlations still describe noisy conditional measurements, with MAEs of 0.207 and 0.244. They do not establish uniformly dependable targets for small held-out partitions.

The diagnostics' no-eligible-opportunities-in-half exclusion bucket includes structurally unsupported games as well as absent conditional histories. For example, the 96 cooperation exclusions in that bucket correspond to six unsupported games × 16 ordered focal/opponent cells; they are not failed cooperation measurements. Three additional cells are excluded for missing design trials.

## Actual action-label sensitivity

The prespecified [label analysis](results/overnight-20260910/primary-pilot/label-analysis/controls-analysis.json) uses the same immutable record file, with a matching SHA-256. Its contrast is **swapped trials 1/3 minus unswapped trials 0/2**, after restoring canonical action coding. It compares two trials per condition, pools counts within the same eligible game/model/opponent cells, weights source games equally, and uses 500 paired game-shape bootstrap replicates. For unconditional targets, excluding incomplete design cells leaves 952 episodes: 476 per label condition across 381 cells and 24 games. N below is the focal opportunity count; E counts distinct eligible episodes.

| Target | Paired games | Change [95% paired-game CI] | Eligible E, unswapped / swapped | N, unswapped / swapped |
|---|---:|---|---:|---:|
| Action0 | 24 | −0.0815 [−0.1687, −0.0135] | 476 / 476 | 7,616 / 7,616 |
| First action0 | 24 | −0.1052 [−0.2170, −0.0085] | 476 / 476 | 952 / 952 |
| Mutual cooperation | 18 | −0.0152 [−0.0424, 0.0170] | 356 / 356 | 5,696 / 5,696 |
| Individual cooperation | 18 | −0.0131 [−0.0360, 0.0091] | 356 / 356 | 5,696 / 5,696 |
| Coordination | 14 | 0.0023 [−0.0263, 0.0306] | 276 / 276 | 4,416 / 4,416 |
| Retaliation | 11 | −0.0069 [−0.0473, 0.0285] | 153 / 156 | 1,325 / 1,400 |
| Forgiveness | 9 | −0.0945 [−0.1791, 0.0056] | 71 / 70 | 102 / 95 |
| Exploitation | 8 | 0.0701 [−0.0681, 0.2263] | 146 / 145 | 920 / 852 |

The broad aggregate action0 rate falls from 0.537 to 0.455, and first action0 from 0.564 to 0.458. These are changes in the underlying canonical choices, not the automatic consequence of renaming A and B. The overall outcome summaries change less: mutual cooperation moves from 0.632 to 0.617, and coordination from 0.758 to 0.761.

| Focal model | Action0 change [95% paired-game CI] | Eligible games | Action opportunities per label condition |
|---|---|---:|---:|
| Claude Haiku 4.5 | −0.1052 [−0.2240, −0.0047] | 24 | 1,920 |
| GPT OSS 20B | −0.0012 [−0.0928, 0.0747] | 24 | 1,904 |
| Kimi K3 | −0.1192 [−0.1922, −0.0573] | 24 | 1,872 |
| Qwen 3.8 27B | −0.1005 [−0.1870, −0.0195] | 24 | 1,920 |

Claude has the largest first-action shift: −0.2042 [−0.3500, −0.0708], with 240 first-action opportunities per condition across 24 games. GPT OSS's near-zero signed action0 mean does not imply invariant choices: its mean absolute game-level change is 0.136, so shifts in opposite directions cancel in the signed average. Absolute changes also contain ordinary finite-trial noise.

The [saved per-game derivation](results/overnight-20260910/primary-pilot/label-analysis/derivation.json) locates the three largest canonical action shifts in the three equal-diagonal coordination games:

| Game | Action0 unswapped → swapped | First action0 change | Coordination unswapped → swapped |
|---|---|---:|---|
| pilot-g0004 | 0.678 → 0.000 | −0.775 | 0.944 → 1.000 |
| pilot-g0018 | 0.991 → 0.422 | −0.750 | 0.981 → 0.906 |
| pilot-g0011 | 0.531 → 0.000 | −0.775 | 0.925 → 1.000 |

Each of these comparisons has 320 focal round opportunities and 40 first-action opportunities per condition. In all three games R=P, so both successful diagonal equilibria give the same payoff to each player. Selecting a different diagonal can therefore change canonical action0 dramatically while preserving the payoff of a successfully coordinated outcome. The off-diagonal payoffs differ, and observed miscoordination changes as well: these results do not establish invariance of the entire realized payoff distribution. They are consistent with display-sensitive equilibrium selection among equal-payoff coordinated outcomes.

High balanced split-half repeatability and label sensitivity can coexist because each repeatability half contains the same mixture of standard and swapped labels. Reproducing that mixture does not test invariance to its components. Conversely, aggregate cooperation/coordination intervals spanning zero are not equivalence tests; no equivalence margin was specified. Small model-specific differences can coexist with small aggregate changes—for example, Qwen's mutual-cooperation change is −0.0188 [−0.0326, −0.0052] on 18 games with 1,440 opportunities per condition. All intervals are descriptive and unadjusted for the many model/target comparisons.

Conditional label comparisons remain especially limited. Forgiveness retains only 55 cells, nine games, and 102 versus 95 opportunities; its apparent decrease is uncertain and mixes changing histories with responses. Exploitation's interval spans substantial changes in both directions on only eight games. The two label conditions can generate different opportunity sets even when their episode designs are balanced. This label result neither evaluates the separate scale/offset/text controls nor demonstrates held-out prediction success.

## What variance justifies, and what it does not

| Target | Between-cell variance | Within-cell trial variance | Between-game variance |
|---|---:|---:|---:|
| Action0 | 0.1350 | 0.0546 | 0.1218 |
| Mutual cooperation | 0.1725 | 0.0207 | 0.1626 |
| Coordination | 0.0552 | 0.0345 | 0.0453 |
| Retaliation | 0.1363 | 0.0988 | 0.0979 |
| Forgiveness | 0.1612 | 0.1247 | 0.0616 |
| Exploitation | 0.0892 | 0.1009 | 0.0097 |

The contrast is strongest for mutual cooperation: its between-cell variance is 0.1725 [0.1035, 0.1973], whereas within-cell trial variance is 0.0207 [0.0133, 0.0286]. Combined with its split-half agreement, this supports treating broad game-associated differences as observable. Exploitation offers much less evidence of a stable game-only profile: between-game variance is 0.0097 [0.0005, 0.0158], within-game cell variance is 0.0714, and within-cell trial variance is 0.1009 [0.0867, 0.1168].

These summaries are not a formal variance-components model or an intraclass correlation. Between-cell variance concerns estimated pooled cell means; within-cell trial variance averages finite-trial rate variation, with different eligibility and denominators. Between-game variation also includes family differences and game orientation. Subtracting or dividing these quantities would not automatically estimate latent signal, measurement reliability, or a prediction ceiling.

The pilot therefore supports proceeding with the already specified predictive evaluation and with target-specific support reporting. It does not show generalization to unseen families, payoff regions, model pairs, alternative representations, or future model versions. Those claims require their own frozen forecasts and held-out observations. Behavioral variance alone does not identify payoff structure as the cause, separate structural features from family memorization, or establish that a learned forecast improves over simple game-theoretic or empirical comparators.

Finally, the social labels remain descriptive. Defection after opponent D is not a causal retaliation effect; even within PD its macro rate of 0.896 accompanies a 0.607 rate of defection after opponent C. The histories and agents producing those denominators differ. The narrower return sequence used for forgiveness avoids calling unconditional cooperation a return from defection, but still does not reveal intention. Eight-round public-history interactions and this fixed four-model roster delimit the conclusions.

## Provenance

Immutable record file SHA-256: 5fc20cea3eef808894edea2b9915850d6ffcaa3cba37e1b37453df13ccb78942.

Diagnostics semantic record digest: d6aa8cb1f988edbe27243307c56824d761f8c98d7413502c87bc5af51f8791ff.

The interpretation uses final descriptive diagnostics, the completed prespecified label analysis and its saved derivation, and immutable records for coverage, missing-cell, role, and support reconstruction. No new inferential analysis was run for this interpretation. It changes no source code, runner, study driver, forecasts, or gates.
