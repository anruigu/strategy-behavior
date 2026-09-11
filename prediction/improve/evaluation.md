# Saved-forecast evaluation

The evaluator performs no fitting, extraction, checkpoint loading, or model calls. Invoke it only after the relevant Fleet job outputs exist. Synthetic tests exercise the implementation locally without using empirical forecasts or outcomes.

```bash
python -B -m prediction.improve.evaluate \
  --data DATA/data.json --folds DATA/folds.json \
  --forecasts BASELINES/forecasts.jsonl TRANSFORMER/frozen/*/forecasts.jsonl TRANSFORMER/lora/*/forecasts.jsonl \
  --out NEW_EVALUATION_DIRECTORY
```

Every input forecast uses `row_id`, `game_id`, `group_id`, `model`, `opponent`, `method`, `split`, `fold_id`, `target`, and an explicit `prediction`. Duplicate queries, conflicting metadata, unplanned queries, nonfinite/out-of-range probabilities, or nonnull predictions for structurally undefined targets fail validation. Within any split that a method declares, every fold/query/target must be present. Missing probabilities may be explicit nulls and remain visible in coverage; they never become zero. An explicit incomplete override is available for reporting a technically incomplete source, with every omitted query listed in the audit.

Method availability is declared separately by split. Kimi's reused few-shot forecasts belong only to the old21 development cohort and later fresh settings. No Kimi results are invented for the 72-shape retrospective family/interpolation/extrapolation folds. The all-method support intersection includes methods actually available for that split. **Numerical-only support includes the seven numerical baselines plus both transformer probability heads**, excluding prompted Kimi: context, family, Nash, payoff-dominant, calibrated payoff-dominant, normalized logistic, combined logistic, frozen Qwen head, and LoRA Qwen head. Thus missing Kimi forecasts do not erase nonprompted transformer comparisons. Both support tables preserve exclusions and target-specific shape/context/opportunity counts.

Primary targets are action0, mutual cooperation, and coordination. Each eligible canonical game receives equal total mass; contexts within a game are weighted by target opportunity counts. Brier is the expected binary-event score, `p² - 2py + y`, with empirical rate `y=k/n`. Log loss clips probabilities to `[1e-7,1-1e-7]` only for scoring. Calibration uses ten fixed probability bins and the same event weights. Rate MSE measures squared error against the **aggregated game/ordered-context rate**, rather than individual trajectory rates. Consequently its absolute value omits some trajectory sampling variance.

`scores.json` contains each split's aggregate results and per-family breakdown, calibration bins, probability means, coverage, and available methods. The seven LOFO folds are pooled into the `family` split with each held-out game appearing once. `group-level.jsonl` saves the sufficient statistics underlying equal-game metrics and calibration. `paired-comparisons.json` compares each transformer with calibrated theory, uncalibrated payoff-dominant theory, family means, normalized/combined logistic, and Kimi where present, plus LoRA directly against the frozen head. Positive improvement means **baseline score minus candidate score**.

The primary paired bootstrap draws 500 canonical-game samples with seed 20260910, preserving every observed episode and both focal roles inside each selected game. It does not separately resample episodes within games. Aggregate retrospective LOFO (`family`) and fresh family-excluded (`fresh_family_excluded`) comparisons additionally draw the seven declared families as clusters; groups within a sampled family remain together. This is a sensitivity analysis with only seven family clusters, not precise uncertainty over an unrestricted population of strategic families. Structural masks mean some targets have fewer eligible families; zero-support bootstrap draws are excluded and counted. All intervals condition on fitted forecasts, without refitting or multiplicity adjustment.

The output directory must be new. `audit.json` binds the source forecast/data/fold bytes and computational source before computation, rechecks them, and saves output hashes. Fleet job/checkpoint provenance and actual forecast-before-player chronology remain required upstream checks; a successful local score join alone does not prove prospectivity.
