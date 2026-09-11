# Gate 3 diagnostics CLI and formulas

`diagnostics.py` is a read-only consumer of completed measurement records. It makes no model requests and changes no rollout code, manifest or source snapshot. Completion and failure accounting remain the runner's responsibility: records alone cannot identify episodes that never completed.

```bash
/shared/allie/venvs/hole/bin/python -B -m prediction.diagnostics \
  --records /shared/allie/strategy-behavior/prediction/results/records.json \
  --out /shared/allie/strategy-behavior/prediction/results/diagnostics \
  --bootstrap 300 --seed 20260910
```

Run from the repository root. The records path is a JSON list or `{ "records": [...] }`. Output must remain under `/shared/allie`. `--no-plots` produces numerical artifacts alone; `--bootstrap 0` disables intervals. No SciPy or scikit-learn dependency is introduced. Plotting uses NumPy and Matplotlib, with its cache under `/shared/allie/home/.codex/tmp/matplotlib-prediction`.

## Outputs

- `diagnostics.json`: input-file hash and normalized-record digest; dataset sizes; support by target, family, model, model/family and directed model/opponent pair; repeatability statistics, exclusions and game-cluster intervals; descriptive variance statistics.
- `derivation.json`: the same record digest, source row indices, contributing episode IDs, per-cell/per-trial successes and opportunities, actual display-label counts, split-half numerators/denominators, retained paired points, and game summaries. It preserves the sufficient statistics for every plotted or reported rate.
- `model_family.{png,svg,pdf}`: every available target in one panel grid. Color is the equal-game macro rate, and annotations show eligible games G, unique eligible episodes E, and focal opportunities N. Unsupported or unobserved cells are gray NA.
- `model_opponent.{png,svg,pdf}`: the same target grid for directed focal-model/opponent cells; the diagonal is self-play. Cells pool supported games using the same weighting convention.
- `replicate_agreement_game.{png,svg,pdf}` and `replicate_agreement_cell.{png,svg,pdf}`: matched split-half plots, correlation and interval where defined, and retained game/point counts. Points are unjittered observations; duplicated values may overlap.

The synthetic visual check is stored separately under `/shared/allie/home/.codex/tmp/diagnostics-preview`. Its numbers are generated test data and must never be reported as pilot outcomes.

## Support and aggregation

For target k, a focal row is eligible exactly when `applicable=true` and `opportunities>0`. Missing target fields, explicit unsupported targets, and applicable targets with no observed opportunities remain distinct. Stored rates must agree with successes/opportunities. Duplicate `(episode_id,player_index)` records are rejected when that index is present.

Within a selected summary subset, pool eligible counts separately for each `game_id`:

`r_g = sum(successes in game g) / sum(opportunities in game g)`.

The primary descriptive summary is `mean_g(r_g)` over eligible games, giving every game equal weight. `pooled_event_rate=sum_g(successes)/sum_g(opportunities)` is also saved for audit, but is not the heatmap value. In particular, conditional rates pool qualifying events inside a game; they do not average a one-event trial equally with a ten-event trial before that game rate is calculated.

Each support object records total/eligible rows, unique episodes, games, structural groups, successes and opportunities, as well as the per-game inputs to its macro mean. `eligible_trials` means unique eligible episode IDs, not the number of distinct small integer `trial_id` values. Both focal rows in self-play may be eligible, but count as one episode. Pooled focal opportunities can include both directions of an episode and are not independent samples.

Within each selected game, the pooling weights reflect available focal observations. These are not equal-opponent macro summaries. In a partial dataset, changed opponent composition can change the game mean; use completion metadata and the balanced repeatability subset before drawing substantive conclusions.

## Split-half repeatability

The fixed pilot split is trials `{0,1}` versus `{2,3}`. Cells are `(game_id, focal model, opponent, representation)`. Both focal rows of a self-play episode are pooled inside their common trial, preserving their episode grouping. Any additional trial IDs contribute to support/variance but are not used in this prespecified four-trial split.

A cell contributes a paired point only if:

1. All four design trials are observed, whether or not each trial has eligible target events.
2. Both halves contain equal numbers of swapped and unswapped episodes, and label compositions match between halves. Unknown label metadata is excluded.
3. Both halves have at least one eligible target opportunity.

Each half rate is its pooled success count divided by its pooled opportunity count. The number of eligible trials inside each half is saved: a sparse conditional can have only one contributing trial even though both design trials completed. Exclusion counts distinguish incomplete design, unbalanced/unknown labels, and zero-opportunity halves. The procedure does not impute missing rates.

The cell-level comparison uses all retained cell pairs, with each game receiving equal total weight and cells within that game receiving equal weights. The game-level comparison pools the **same retained cells** within each half and then compares one pair per game. It does not compare different collections of cells across halves.

Weighted Pearson correlation is covariance divided by the product of weighted standard deviations. It is null with fewer than three points or a constant/near-constant half; exact agreement between constant halves therefore has MAE=0 and RMSE=0 but no correlation. Weighted MAE and RMSE are saved alongside correlation. These are descriptive repeatability measures, not forecast performance on held-out strategic structures.

## Variance descriptions

For each cell, save the rate from pooling its eligible trials and the sample variance (`ddof=1`) of its individual eligible trial rates when at least two exist. Trial variance is deliberately based on trial-level rates, so each independent repetition contributes once; unequal conditional denominators make these variances heterogeneous.

- `between_cell_variance`: weighted population variance of pooled cell rates, giving games equal total weight and cells equal weight within game. This combines game, model, opponent and representation differences; it is not variance attributable to game structure alone.
- `within_cell_trial_variance`: average sample trial variance within each game, then the average over games with at least one repeat-supported cell. Games without two eligible trials in any cell are excluded and counted.
- `between_game_variance`: population variance across pooled game rates, using equal game weights and requiring at least two eligible games.
- `within_game_cell_variance`: average across games of the population variance of eligible cell means; games need at least two eligible cells.

These statistics use different observational levels. Between-cell variance contains trial noise, and conditional trial noise depends on opportunity count. No noise subtraction, causal explained-variance claim, or intraclass-correlation estimate is made. More between-cell than within-cell variation is a diagnostic observation, not proof that payoffs predict behavior.

## Uncertainty and limitations

Intervals are percentile 95% intervals from resampling complete `group_id` blocks with replacement. All games, model pairings, focal directions and trials within a sampled structural group remain together. Sampling a block twice creates distinct bootstrap block/game identities so equal-game weighting is preserved. Every interval reports the number of valid and requested replicates. Fewer than two original clusters gives no interval; fewer than `max(20, floor(repetitions/2))` valid replicates also gives no interval, rather than hiding degenerate correlations.

This bootstrap quantifies variation across observed game-shape blocks. It is not a nested bootstrap of new trials and makes no population claim beyond the sampled game design. Small numbers of eligible games remain a material limitation even if an interval exists. Affine/action-swapped sibling games sharing a group are resampled together. Point summaries still weight `game_id` equally; expanded datasets with unequal numbers of sibling variants should be stratified before interpreting those point summaries.

Diagnostics are Gate 3 evidence about data support and measurement variability. Reliable aggregate rates can coexist with failed structural generalization. High split-half agreement can be driven by model averages, while constant but reproducible behavior has no correlation. Claims of predictive signal must use the separately frozen model/baseline and holdout analyses.

## Functions and tests

Public entry points are `load_records(path)`, `validate_records(records)`, `summarize_support(rows,target)`, `derive_target(records,target)`, `build_diagnostics(records,bootstrap=300,seed=20260910)`, `render_figures(summary,derivation,out)`, and `run(records_path,out,bootstrap=300,seed=20260910,plots=True)`.

Run `/shared/allie/venvs/hole/bin/python -B -m unittest prediction.test_diagnostics -v`. Synthetic cases test event pooling versus equal-game averaging, unsupported/missing/empty support, required trials and balanced labels, undefined constant correlations, known variance and perfect nonconstant agreement, self-play episode dependence, duplicate rejection, and JSON file handling.
