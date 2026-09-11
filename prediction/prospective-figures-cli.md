Refresh readable primary prospective figures from preserved scores:

```bash
TMPDIR=/shared/allie/home/.codex/tmp PYTHONDONTWRITEBYTECODE=1 \
/shared/allie/venvs/hole/bin/python -B -m prediction.prospective_figures \
  --run-root /shared/allie/strategy-behavior/prediction/results/overnight-20260910 \
  --stage all
```

Stages are `full` (numerical plus prompted methods), `numerical`, `pair`, `model`, `controls`, or `all`. The command only reads existing evaluations, verifies the completed primary marker's output hashes, independently rechecks forecast-before-play chronology, and copies saved statistics into figures. Incomplete or unverified stages remain absent. Input, audit, renderer, and transitive forecast/outcome hashes are captured before rendering and checked again before publishing. No models are fitted, scores recomputed, forecasts rewritten, or API calls made.

Each available stage creates exactly two PNGs, with matching SVG/PDF exports, under `RUN/report-figures/prospective/STAGE/`:

- `broad-target-scores`: action 0, mutual cooperation, and coordination; Brier and log loss with existing score confidence intervals. Nine fixed baseline, learned, and prompted methods are shown when present. The original all-method common support is retained even when other methods are omitted from the display. Methods are never sorted by observed performance.
- `broad-target-calibration`: the saved ten-bin numerical and prompted calibration curves, including few-shot forecasts. Dot area increases with the original game-equal event mass. Sparse bins have no displayed uncertainty. Connecting segments are visual guides.

`plotted-values.json` records exact selected score rows, calibration bins, confidence intervals, and support counts. `derivation.json` has status `verified_derived_figure`, records the source evaluation directory and all input/output hashes, and lists `replaces_png_paths`. For the report, include the two PNGs from each verified stage derivation and suppress only those two original PNG paths from inline presentation. Preserve all original plots and link their source scores for omitted conditional targets and identity/feature ablations. The report integration requires no changes to scoring or evaluation directories.

These are presentation choices made after results. Individual-score intervals are not paired significance tests; saved paired contrasts remain in the primary summary and source evaluations. All intervals are descriptive and unadjusted, conditional on fixed fitted forecasts. Each figure keeps its own test population; numerical-only and prompted evaluations can have different common support. Controls reuse canonical shapes, hence support labels say **shape groups**, not distinct new games.
