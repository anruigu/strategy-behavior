# Data and numerical baseline protocol

`data.py` performs count-preserving export only. The original 72-shape snapshot remains the fitting cohort; the already inspected later 21 shapes are development data. No controls are added to training. Original files and scientific code are unchanged.

The exported `data.json` has `train_examples`, `development_examples`, the fixed player protocol/configurations, and three targets in the order `action0`, `cooperation`, `coordination`. Repetitions, balanced display swaps, and focal roles with identical game/payoffs and ordered model/opponent inputs are aggregated by summing successes and opportunities. Each example keeps `source_row_indices` and `episode_ids`, permitting predictions to be expanded onto the original focal rows for paired episode/game bootstrap scoring. Aggregation does not make those examples independent experimental units.

Each example provides `row_id` (also `example_id`), payoff-derived `group_id`, `game_id`, `family`, payoffs, identities, features, applicability, `input_text`, and target counts. IDs and taxonomy are metadata for joining/splitting; predictor text never includes them or outcomes. `y` may contain nulls; `mask` explicitly excludes missing targets. `weights[t] = opportunities[t] / sum_game(opportunities[t])`, giving each eligible canonical game unit mass per target. **Recompute weights after selecting training rows.** Normalize each target's loss by its training weight total; do not infer eligibility from a zero success count.

`folds.json` has ten fixed fits: seven `family_<family>` LOFO folds, `within_family_interpolation`, `within_family_extrapolation`, and `full`, whose evaluation cohort is the old 21 shapes. Each fold saves integer `train`/`test` indices, matching `train_row_ids`/`test_row_ids`, `test_dataset`, groups, family counts, and coordinate regions. Both sides of each within-family split contain all seven families. Structural applicability still means not every family contributes to every target.

The fixed invariant coordinate is canonical t for PD, Stag Hunt, Chicken and Harmony; canonical s for weak dominance, where t is constant; and `abs(S-T)/(max(payoffs)-min(payoffs))` for equal-diagonal coordination/anti-coordination. Values are rounded to 12 decimals. Within each family, distinct values are partitioned into lower/middle/upper blocks, with sizes floor(n/3), floor(n/3), and the remainder; ties never cross a boundary. Interpolation trains the outer blocks and tests the bracketed middle. Extrapolation trains the lower and middle blocks and tests the upper. Fewer than three distinct coordinates fails closed. No behavioral outcome chooses coordinates or thresholds.

`baselines.py` imports no original modeling/vendor package. It needs NumPy/SciPy in the Fleet image and the pure-Python original `games.py`. Its fixed methods are ordered context, family, original Nash selector, payoff-dominant selector, calibrated payoff-dominant selector, normalized-derived logistic, and raw-plus-derived logistic. The normalized feature set reproduces the original derived strategic features; combined adds four raw payoffs. Both numerical predictors use train-only scaling and ordered focal/opponent one-hot identities. Unknown identity categories are all-zero; unknown context/family falls back to the training population probability.

All fitted means, numerical heads, preprocessing, and theory calibration must execute in the Fleet job. The worker requires `IMPROVE_TRAINING_AUTHORITY=fleet_api`, `IMPROVE_FLEET_RUN_ID=<assigned run>`, and the matching `--fleet-run-id`; these are job provenance guards, not an authentication mechanism. The root agent owns API submission. Synthetic local tests do not consume empirical labels.

```bash
python -B -m prediction.improve.baselines train \
  --data /mnt/sfs/allie/.../data/data.json \
  --folds /mnt/sfs/allie/.../data/folds.json \
  --out /mnt/sfs/allie/.../baseline-job \
  --fleet-run-id ASSIGNED_RUN
```

Logistic heads minimize game-equal event cross entropy plus ridge on slopes, with an unpenalized intercept. Ridge strengths 0.001/0.01/0.1 use three deterministic training-group validation partitions, with train-only preprocessing and equal-game validation log loss. Theory calibration uses per-target monotone Platt scaling of clipped theory log odds (`p` clipped to 0.01–0.99), slope constrained nonnegative, and fixed ridge 0.01 toward identity calibration. This gives generic probability smoothing an explicit comparator. Theory ties retain a joint mixture of coordinated conventions.

Workers save per-fold fits, consolidated `fits.json`, JSONL forecasts, optimizer/inner-validation diagnostics, source/input hashes, versions, run ID, and completion hashes. Forecast records use `row_id`, game/group IDs, identities, method, split, `fold_id`, target and probability; structurally unsupported probabilities remain null. The separate `forecast` command applies saved parameters to metadata without fitting and saves its input hashes and creation timestamp. Fresh collection still requires the study-level freeze and chronology audits.
