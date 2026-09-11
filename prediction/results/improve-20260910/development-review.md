The fixed development stop is correct. Both Qwen heads are worse than the strongest declared numerical comparator on every target in both leave-family-out evaluation and old21 development. All twelve saved paired Brier intervals have upper bounds below zero, satisfying the stronger condition needed to exclude a +0.005 meaningful gain. No fresh player status, traces, collected outcomes, or fresh evaluation exists.

All values below use equal mass per eligible canonical game and event weights within a game. Intervals are the saved 95% percentile intervals from 500 whole-game bootstrap samples; positive baseline-minus-head gain favors the head.

| Split / target | Strongest declared numerical comparator | Its Brier | Calibrated theory Brier | Frozen Brier | LoRA Brier |
|---|---|---:|---:|---:|---:|
| family / action0 | calibrated_payoff_dominant | 0.147284 | 0.147284 | 0.282962 | 0.282941 |
| family / cooperation | calibrated_payoff_dominant | 0.079293 | 0.079293 | 0.339515 | 0.357898 |
| family / coordination | calibrated_payoff_dominant | 0.140468 | 0.140468 | 0.350000 | 0.352439 |
| development / action0 | normalized_logistic | 0.137647 | 0.137697 | 0.229994 | 0.222971 |
| development / cooperation | combined_logistic | 0.056336 | 0.061493 | 0.236371 | 0.225703 |
| development / coordination | family | 0.138752 | 0.141063 | 0.182687 | 0.189043 |

The following contrasts use the same fixed calibrated-theory comparator throughout, avoiding selection of the point-best comparator for the scientific comparison.

| Split / target | Calibrated theory minus frozen Brier [95% interval] | Calibrated theory minus LoRA Brier [95% interval] |
|---|---:|---:|
| family / action0 | -0.1357 [-0.1705, -0.1042] | -0.1357 [-0.1689, -0.1040] |
| family / cooperation | -0.2602 [-0.3311, -0.1883] | -0.2786 [-0.3505, -0.2068] |
| family / coordination | -0.2095 [-0.2529, -0.1737] | -0.2120 [-0.2577, -0.1737] |
| development / action0 | -0.0923 [-0.1371, -0.0500] | -0.0853 [-0.1318, -0.0433] |
| development / cooperation | -0.1749 [-0.2814, -0.0668] | -0.1642 [-0.2773, -0.0551] |
| development / coordination | -0.0416 [-0.0710, -0.0186] | -0.0480 [-0.0733, -0.0249] |

The gate-selected old21 comparators are normalized logistic for action, combined logistic for cooperation, and the family mean for coordination. Their Brier-gain intervals against frozen/LoRA are:

| Old21 target | Strongest minus frozen | Strongest minus LoRA |
|---|---:|---:|
| action0 | -0.0923 [-0.1358, -0.0537] | -0.0853 [-0.1317, -0.0444] |
| cooperation | -0.1800 [-0.2876, -0.0714] | -0.1694 [-0.2801, -0.0597] |
| coordination | -0.0439 [-0.0772, -0.0196] | -0.0503 [-0.0778, -0.0257] |

Calibrated theory also has lower log loss than either head on all six split/target combinations, with all corresponding game-bootstrap intervals below zero. On LOFO, its action/cooperation/coordination log losses are 0.4699/0.2680/0.4147, compared with frozen 0.8538/1.1067/1.2358 and LoRA 0.8630/1.1991/1.2742. On old21 they are 0.4230/0.2232/0.4138, versus frozen 0.7065/0.7130/0.5508 and LoRA 0.7010/0.6722/0.5657. Calibrated theory has lower point ECE in all six cells; ten-bin ECE is descriptive and is not a proper scoring rule.

The LOFO seven-family sensitivity retains negative Brier and log-loss intervals for both heads versus calibrated theory on all three targets. Only seven family clusters exist, with fewer families structurally eligible for some targets; these intervals are a sensitivity check, not precise uncertainty for a broad population of strategic families.

LoRA is not a consistent improvement over the frozen head. On old21 its Brier gains are +0.0070 action, +0.0107 cooperation, and −0.0064 coordination; all three game-bootstrap intervals cross zero. Under LOFO it worsens cooperation Brier by 0.0184 (frozen-minus-LoRA interval [−0.0273, −0.0096]); action and coordination Brier differences are uncertain. The training-only finding that all ten LoRA objectives worsened is distinct from these held-out comparisons.

Reused Kimi few-shot forecasts exist only on old21 development and cover every eligible context. Its Brier scores are 0.131262/0.061827/0.141496 and log losses 0.390862/0.221719/0.423962 for action/cooperation/coordination. It has the lowest observed action Brier among these candidates, but no Kimi-versus-theory paired interval was produced by the fixed scorer; this point ranking is not a claim of established superiority. Kimi was not evaluated on LOFO or the corrected within-family splits.

The corrected within-family interpolation/extrapolation point results also favor the simple comparators. Frozen/LoRA Briers are respectively 0.260750/0.258120, 0.217070/0.213034, 0.261694/0.249645 for interpolation; 0.335210/0.343889, 0.283933/0.279071, 0.192926/0.192756 for extrapolation. The corresponding strongest declared numerical scores are 0.134322/0.068722/0.137459 and 0.142669/0.070901/0.134333. These are reported checks, not additional architecture-selection gates.

Support was verified using saved group identities and counts, not just equal totals: all 24 split/target/support cells retain every eligible context and have identical game/count support across their candidate methods. LOFO action/cooperation/coordination uses 72/52/42 games, 1,152/832/672 contexts and 30,688/22,368/17,888 opportunities. Old21 uses 21/14/12 games, 336/224/192 contexts and 6,720/4,480/3,840 opportunities. There are no omitted forecasts or incomplete-coverage overrides. Structurally undefined targets are excluded rather than treated as zero.

Interpretation is bounded: 72 training shapes, four fixed players, seven sampled strategic families, one model revision, one optimization seed, and one two-epoch LoRA schedule. Old21 outcomes were already inspected in the earlier POC, so this is development evidence, not a new prospective replication. The bootstrap holds fitted models fixed, resamples whole games without refitting, and supplies no multiplicity or comparator-selection adjustment. Action0 is an encoded action coordinate, not a universal cooperation label.

Optimization was finite and operationally complete, but none of the ten frozen heads met strict gradient tolerance, and all ten LoRA full-training objectives increased from their same-fold frozen warm starts (+0.041544 to +0.068589). The negative result applies to this fixed representation/training procedure. It does not show that all transformer fine-tuning, other representations, or better-optimized heads cannot predict behavior.

Verified sources: [scores](development-evaluation/scores.json), [paired intervals](development-evaluation/paired-comparisons.json), [scoring audit](development-evaluation/audit.json), [fixed gate](development-gate.json), and [training diagnostics](training-diagnostics-final.md). Exact extracted values, gate recomputation, support checks and source hashes are in [development-review.json](development-review.json). This review only reads saved results; it performs no fitting, new forecast scoring, or API calls.
