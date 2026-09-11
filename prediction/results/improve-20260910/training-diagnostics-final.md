All 20 fixed transformer fits now have completed artifacts with matching training row IDs, game groups, three-target support, and Fleet lineage. Every LoRA fit completed its declared two epochs and expected optimizer steps. The 90 successful saved baseline optimizer records were reused after their original audit hashes were reverified. Audit snapshot: 2026-09-10T16:38:31.946661+00:00.

All ten frozen heads reduced their finite training objectives; 0/10 met the strict 1e-6 gradient tolerance. Maximum gradients range from 0.000452 to 0.000929. The recorded 200 iterations is the configured cap; closure evaluations include line-search calls and do not establish actual iteration counts.

Relative to each fit's own frozen warm start, final LoRA full-training objectives were higher in 10/10 folds, lower in 0/10, and equal in 0/10. Changes range from +0.041544 to +0.068589; median +0.057084. This is a training optimization limitation, not a held-out predictive result. `optimization_success` certifies completion of the fixed steps.

| Training fold | Frozen objective | Frozen maximum gradient | LoRA objective | LoRA minus frozen | Completed LoRA steps |
|---|---:|---:|---:|---:|---:|
| family_anti_coordination | 0.306008 | 0.000452 | 0.358388 | +0.052380 | 62 |
| family_chicken | 0.261760 | 0.000681 | 0.303304 | +0.041544 | 62 |
| family_coordination | 0.361691 | 0.000525 | 0.430280 | +0.068589 | 62 |
| family_harmony | 0.380055 | 0.00063 | 0.442597 | +0.062542 | 62 |
| family_prisoners_dilemma | 0.329520 | 0.000739 | 0.377435 | +0.047915 | 62 |
| family_stag_hunt | 0.393400 | 0.000929 | 0.446355 | +0.052955 | 62 |
| family_weak_dominance | 0.368979 | 0.000667 | 0.437115 | +0.068137 | 64 |
| within_family_interpolation | 0.340251 | 0.00074 | 0.399235 | +0.058984 | 52 |
| within_family_extrapolation | 0.322785 | 0.000885 | 0.379847 | +0.057062 | 42 |
| full | 0.353483 | 0.000862 | 0.410590 | +0.057107 | 72 |

These comparisons use the same target weighting and head regularization within each fold. A first stochastic minibatch loss is not a comparable full-training starting objective. Different folds have overlapping training sets, so no confidence interval or independent-sample claim is attached to their objective changes.

All inspected fits used PyTorch 2.11.0+cu128, Transformers 5.8.0, PEFT 0.18.1, NumPy 2.3.5, and Safetensors 0.8.0. Baselines used SciPy 1.15.3. The fixed model revision, one optimization seed, and schedule remain unchanged. The initial audit contains the preserved runtime preflight and baseline details.

No empirical fitting, model loading, API calls, or held-out scoring occurred in this audit. Completed fit artifacts do not mean the ongoing fresh forecast phase or downstream evaluation is complete.

Full diagnostics and verified source hashes: [training-diagnostics-final.json](training-diagnostics-final.json). Initial snapshot preserved: [training-diagnostics-initial.md](training-diagnostics-initial.md). Reproducible inspection: [audit_final_training.py](independent-analysis/audit_final_training.py); it refuses to overwrite this audit.
