# Improvement report renderer

`report.py` reads completed score artifacts, root-owned decision records, and saved operational metadata. It performs no fitting or model/API calls. It does not inspect player outcomes directly or derive an improvement decision from point estimates.

```bash
python -B -m prediction.improve.report \
  --run-root prediction/results/improve-20260910 \
  --out prediction/IMPROVEMENT-REPORT.md \
  --development-eval prediction/results/improve-20260910/development-evaluation \
  --fresh-eval prediction/results/improve-20260910/fresh-evaluation
```

The two evaluation paths shown are defaults and may be overridden. `--figures` optionally changes the generated figure directory; its default is `RUN/report-figures`. Every figure exports standalone PNG, SVG, and PDF files. The Markdown report embeds PNGs and links vector versions. Outputs can be refreshed as decisions and results arrive, without modifying numerical artifacts.

`final-disposition.json` takes precedence over `development-gate.json`. The renderer uses their saved `decision`/`status` and `summary`/`conclusion`/`reason`/`message` fields. With neither file present it reports a pending decision. Missing evaluations appear explicitly; no synthetic values or placeholder success claims enter the real report.

Completed `scores.json`, `paired-comparisons.json`, and `group-level.jsonl` must match a verified evaluator `audit.json`; their hashes are rechecked after rendering. Candidate tables cover all three primary targets and every available declared split. Plots show Brier/log-loss panels, calibration curves, and paired Brier gains over calibrated theory with game and seven-family sensitivity intervals. If prompted coverage changes support, the nonprompted numerical/transformer comparison is also shown.

Job tables use only allowlisted names, statuses, and timestamps from this run's saved Fleet submissions/monitor records. Observed wall time and completed worker time are labeled separately; allocated GPU hours or a dollar price are not inferred. The inference ledger is read through a query-only SQLite connection. `report-artifacts.json` records the observed input hashes, timed ledger snapshot, output hashes, and that no fitting or score-derived decision occurred. Operational records can change while the experiment runs; they are point-in-time observations, unlike the rechecked numerical outputs.
