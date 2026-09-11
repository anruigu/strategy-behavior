The initial training audit found no finite-value, training-scope, target-support, or fixed-step completion failures in the inspected artifacts. This is a partial audit: all ten baseline folds and the first two completed LoRA folds with their matching frozen heads (4 of 20 transformer fits), as of 2026-09-10T16:22:03.104163+00:00.

All 90 saved baseline optimizers report successful termination in 6–166 iterations; coefficients and objectives are finite. The ten-fold baseline stage took 40.6 seconds. Maximum raw gradient is 6.63e-7; only 27/90 meet 1e-8, so successful termination should not be described as universal gradient-tolerance convergence. Exact SciPy termination messages were not retained.

| Held-out family defining training fold | Frozen initial → final objective | Frozen maximum gradient | LoRA final objective | Change from frozen warm start | Fixed LoRA steps |
|---|---:|---:|---:|---:|---:|
| family_anti_coordination | 0.607573 → 0.306008 | 0.000452 | 0.358388 | +0.052380 | 62/62 |
| family_chicken | 0.562632 → 0.261760 | 0.000681 | 0.303304 | +0.041544 | 62/62 |

Both frozen heads missed the configured 1e-6 gradient tolerance. Their 209/215 closure evaluations include line-search calls; the artifact records the configured 200-iteration cap, not actual optimizer iteration counts. LoRA finished its fixed two epochs with finite diagnostics, but both full-training objectives worsened from the frozen starting point. These are reportable optimization limitations; neither proves worse held-out prediction. The first stochastic minibatch loss is not a comparable full-training starting loss.

Training counts match the fixed scopes: 1,152 aggregated contexts across 72 shapes; action/cooperation/coordination have 30,688/22,368/17,888 opportunities across 72/52/42 supported shapes. Both audited fold pairs support all three targets, with matching row IDs and supported-group counts.

Runtime: Python 3.12 worker environment, PyTorch 2.11.0+cu128, Transformers 5.8.0, PEFT 0.18.1, NumPy 2.3.5, SciPy 1.15.3, Safetensors 0.8.0, CUDA 12.8 on NVIDIA B300 SXM6. The recorded backend disables only cuDNN SDPA. Technical preflight passed with finite 2,560-dimensional representations; input lengths 266–284 fit the 512-token limit. Preflight lengths include metadata-only queries; no held-out outcome scores were computed.

The fixed single optimization seed and schedule remain unchanged. No empirical fitting, model loading, inference/API calls, or held-out scoring occurred during this audit. This audit does not certify the remaining transformer fits.

Detailed diagnostics and before/after-verified source hashes: [training-diagnostics-initial.json](training-diagnostics-initial.json). Reproducible read-only inspection and immutable audit writer: [audit_initial_training.py](independent-analysis/audit_initial_training.py). Rerunning preserves this initial snapshot by refusing to overwrite it.
