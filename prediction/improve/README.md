# Prediction improvement study

This study compares frozen Qwen3 representations and LoRA adaptation with numerical, empirical, equilibrium, and prompted predictors. All empirical fitting runs through the Fleet Training API.

- [Research plan](../../research_logs/sep/0910-prediction-improve.md)
- [Results report, with inline figures when available](../IMPROVEMENT-REPORT.md)
- [Current execution checkpoint](../results/improve-20260910/operator-checkpoint.json)
- [Frozen scientific inputs and sources](../results/improve-20260910/training-freeze.json)

The earlier study is preserved in `prediction/results/overnight-20260910`. New artifacts are under `prediction/results/improve-20260910`. Technical retries retain their submissions, failures, and explicit amendments under `fleet-runtime`; they do not establish a predictive result.

## Implementation

| Stage | Documentation |
|---|---|
| Aggregation, fixed splits, and baseline fitting | [Data and baselines](data-baselines.md) |
| Frozen representations and LoRA training | [Transformer worker](transformer.md) |
| Fleet runtime dependency checks | [Bootstrap](bootstrap.md) |
| New cohort and forecast freeze | [Prospective design](prospective_design.md) |
| Artifact verification and automatic continuation | [Post-training execution](post_training.md) |
| Collection integrity | [Integration audit](integration-audit.md) |
| Game-level scoring and uncertainty | [Evaluation](evaluation.md) |
| Saved-score tables and inline plots | [Report rendering](report.md) |
| Cross-module verification | [Schema integration audit](schema-integration-audit.md) |

`post_training.py` defaults to a dry run. The supervisor launches its explicit execution mode only against a selected, recorded Fleet submission. It verifies training artifacts, applies the fixed development gate, freezes forecasts before fresh player calls, and uses the shared evaluation ledger. A completed pipeline still needs scientific interpretation; technical failures are reported separately from negative prediction evidence.
