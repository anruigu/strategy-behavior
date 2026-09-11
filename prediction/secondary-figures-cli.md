Generate readable **derived** figures without changing audited scores, predictions, or frozen code:

```bash
TMPDIR=/shared/allie/home/.codex/tmp PYTHONDONTWRITEBYTECODE=1 \
/shared/allie/venvs/hole/bin/python -B -m prediction.secondary_figures \
  --run-root /shared/allie/strategy-behavior/prediction/results/overnight-20260910 \
  --stage all
```

`--stage` accepts `pilot`, `development`, `prospective`, `pair`, `model`, `controls`, or `all`. A refresh adds figures only for available results with `supervisor-audit.json` status `verified` and matching score hashes/classifications. Unchanged figures are reused after checking input and output hashes. The command makes no API calls and does not recompute scores or uncertainty.

At most two main figures are saved per stage under `RUN/report-figures/secondary/STAGE/`, each in PNG, SVG, and PDF:

- `brier-overview`: three broad-target panels, separate split rows, and a fixed method order. It includes original/secondary equilibrium selection, context baselines, family mean, learned predictors, and the three prompted methods when available. Grey cells mean unavailable scores. No averaging or sorting across distinct test populations occurs.
- `secondary-uncertainty`: three targets × two metrics, with separate split rows and paired intervals for the three prespecified learned predictors relative to the payoff-dominant secondary selector. Positive values mean lower learned-model loss. Bars retain the existing unadjusted 95% game/episode bootstrap intervals with fitted predictions fixed.

Pilot and development headings explicitly say **secondary post-pilot retrospective sensitivity**. New-outcome comparisons say **secondary post-pilot prospective comparison** only when their supervisor classification supports that designation. The event-weighted context comparator is included in the Brier overview; the uncertainty figure concentrates on the stronger equilibrium-selection comparison. All primary gate criteria remain unchanged.

Support labels count **canonical payoff-shape groups**. Affine and text controls can contain multiple variants within one group, so these labels are not counts of numerical payoff matrices or independent new games.

`plotted-values.json` records exact selected scores, support counts, contrasts, and method names. Each stage's `derivation.json` hashes the source scores, supervisor audit, renderer, and all output files; source hashes are checked before and after rendering. `RUN/report-figures/secondary/index.json` lists the available stages and figure paths; the adjacent aggregate `derivation.json` binds the stage audits and derived outputs for report inclusion. Temporary rendering happens under the same persistent storage root, and only this generator's own superseded derived files are replaced or removed. Audited source figures and scientific artifacts remain untouched.
