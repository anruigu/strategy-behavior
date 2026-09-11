# Primary transfer overview

Run the CPU-only renderer whenever additional saved evaluations are complete:

```bash
/shared/allie/venvs/hole/bin/python -B -m prediction.summary_figures \
  --run-root /shared/allie/strategy-behavior/prediction/results/overnight-20260910
```

Outputs default to RUN/report-figures; `--out` overrides this directory. The Python entry point is `run(run_root, out=None, color_limit=.35)`. All output directories must resolve under `/shared/allie`.

The fixed method is the original primary `combined_logistic_both` predictor, compared with the original ordered focal-model/opponent-model `pair` baseline. The plot copies the saved paired event-Brier improvement, with positive values meaning baseline Brier minus method Brier. It neither fits predictors, recomputes scores, selects a winning method, nor recalculates pairwise support.

The three targets are canonical action0, mutual cooperation, and coordination. Pilot and development panels show family, random-group, payoff interpolation, payoff extrapolation, pair, and model splits. The first four withhold payoff shapes; the latter two intentionally reuse known game shapes. The prospective panel reads full numerical evaluation, held-pair evaluation, held-model evaluation, and controls evaluation. Prospective pair/model tests also use new games; controls reuse source shapes. The full prospective input is specifically `prospective/evaluation-numerical/scores.json`, preserving that evaluation's original numerical-method common support rather than changing support through the separate prompted-forecast evaluation.

Sources are:

- `pilot/evaluation/scores.json`
- `development/evaluation/scores.json`
- `prospective/evaluation-numerical/scores.json`
- `prospective/evaluation-pair/scores.json`
- `prospective/evaluation-model/scores.json`
- `controls/evaluation/scores.json`

Prospective/control cells are displayed only when the adjacent saved audit declares verified prospectivity and the expected requested/effective split. Pending scores, missing audits, or unverified results remain explicitly labeled gray cells. Existing evaluations must contain unique matching split/target/method keys, the declared ordered baseline, common-support counts shared by both methods, and a saved Brier contrast consistent with the two saved scores. Missing common support is gray NA, never a fabricated zero.

Each cell prints the signed saved improvement, G (canonical payoff-shape groups), and an interval descriptor: CI > 0, CI < 0, CI spans 0, or CI NA. The descriptors refer to the saved paired 95% intervals, not corrected hypothesis tests. They are descriptive, unadjusted for multiplicity, and conditional on fixed fitted forecasts. No interval is invented for a single eligible group. G is a shape-group count: three affine/text variants of one source shape do not become three independent game groups.

All figures share a fixed symmetric color scale, green for improvement and red for degradation. Colors saturate at ±0.35 by default; printed numbers remain the saved values rounded to three decimals. `--color-limit` changes only that display scale. The full interval bounds, score/support records, eligible episode/opportunity counts, source file hashes, and plotting-source hash are archived in `derivation.json`. Sources are rechecked after rendering to catch a concurrent rewrite.

The renderer writes a compact three-panel overview and one readable figure per stage:

- `primary-transfer-overview.png`, `.svg`, `.pdf`
- `primary-transfer-pilot.png`, `.svg`, `.pdf`
- `primary-transfer-development.png`, `.svg`, `.pdf`
- `primary-transfer-prospective.png`, `.svg`, `.pdf`

These are refreshable derived artifacts. The renderer changes no primary scores, forecasts, audits, gates, or report source. Secondary methods are intentionally excluded from this primary-method figure.
