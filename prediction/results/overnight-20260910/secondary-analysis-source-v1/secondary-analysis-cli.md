This independent supervisor completes the remaining **CPU-only secondary analyses**. It neither edits the archived secondary forecast implementation nor launches player/forecaster calls. It leaves primary methods, paid-stage decisions, gate criteria, and original artifacts unchanged.

```bash
TMPDIR=/shared/allie/home/.codex/tmp PYTHONDONTWRITEBYTECODE=1 \
/shared/allie/venvs/hole/bin/python -B -m prediction.secondary_analysis \
  --run-root /shared/allie/strategy-behavior/prediction/runs/RUN \
  --bootstrap 500
```

A nonblocking `secondary-analysis.lock` prevents duplicate supervisors. Status is recorded in `RUN/independent-analysis/secondary-status.json`, with per-job logs under `RUN/logs/secondary-analysis-*.log` and durable guards under `RUN/steps/secondary-analysis-*.json`. The supervisor permits only the existing secondary `retrospective`/`compare` commands and the existing prospective `score` command. No fit, forecast, inference, ledger, or player-stage command is permitted.

It runs pilot retrospective sensitivity once the primary pilot numerical marker and fixed records are complete, then development sensitivity once the preserved 72-game evaluation is complete. It reuses the archived helper's saved-fold interface and marks these analyses post hoc. Outputs are:

| Analysis | Output directory within RUN |
|---|---|
| Pilot saved-fold sensitivity | `independent-analysis/pilot-secondary` |
| 72-game saved-fold sensitivity | `independent-analysis/development-secondary` |
| Full prospective secondary score/comparison | `secondary-baselines/full/prospective-evaluation`, `prospective-comparison` |
| Excluded-pair prospective score/comparison | `secondary-baselines/excluded_pair/prospective-evaluation`, `prospective-comparison` |
| Excluded-model prospective score/comparison | `secondary-baselines/excluded_model/prospective-evaluation`, `prospective-comparison` |
| Full controls secondary score/comparison | `secondary-baselines/full/controls-evaluation`, `controls-comparison` |

The four standalone frozen exports are `full/prospective.jsonl`, `full/controls.jsonl`, `excluded_pair/prospective.jsonl`, and `excluded_model/prospective.jsonl` under `RUN/secondary-baselines`. Their existing manifests, fit/training artifacts, exclusion plan, and freeze evidence are hashed and preserved. Every secondary score uses the complete outcome snapshot and stage metadata. Pair/model focus is applied through the existing scorer with exactly the frozen exclusions and `prospective_pair`/`prospective_model` split names. Full prospective uses `prospective`; controls use `prospective_controls`.

Full prospective comparisons include the primary numerical and prompted methods from `prospective/evaluation`. Pair/model comparisons use `prospective/evaluation-pair` and `prospective/evaluation-model`; controls use `controls/evaluation`. The primary numerical-only analysis and expansion screens remain unchanged.

Before each command, the supervisor snapshots all relevant input files, primary completion markers, transitive audit sources, frozen secondary artifacts, and computational source files. It checks completed upstream output hashes, runs the CPU helper, then recomputes every input hash and input-file membership. This closes the archived retrospective helper's read-before-hash race: results are not marked valid when the inputs it read changed during execution. Existing completed command markers are reused only when the command, initial source/input snapshot, and all output hashes still match. Partial/unmarked/error outputs require explicit checkpoint review rather than silent overwrite or retry.

After successful postchecks, the supervisor writes `OUTPUT/supervisor-audit.json` with `status="verified"`, the secondary classification, initial hashes, successful final checks, and scientific output hashes. The report should require this wrapper audit. Scientific `audit.json` stays untouched. A failed postcheck produces a durable error and **no** report-eligible wrapper. A later resume that detects a changed completed artifact records a job error/report_eligible=false in supervisor status; the previously written wrapper remains historical evidence and must not override that newer error.

Prospective validation independently rechecks the source audit's hash/input/timing flags and empty issue lists, numerical creation manifests or prompted completion timestamps, and the earliest actual trace start. A saved true flag cannot promote a late forecast. Comparison runs concatenate already verified scored predictions; they do not generate or backdate combined forecasts.

The supervisor continues after the paid pipeline terminates so ready analyses can finish. A prospective/control job may be skipped only when an actual gate record declined that cohort or its control follow-up, and the stage has no player process, status, episode directory, or primary scoring marker. Missing pilot/development results, missing results from a started future stage, or absent artifacts without a genuine no-expansion gate are technical errors, even after `complete_through_gate7`. Skips are checked again on process resume. Upstream technical failures, failed secondary prerequisites, changed artifacts, and invalid temporal audits are also reported as errors. Final status is `complete`, `complete_with_skips`, or `error`; it never declares missing work completed. Report rendering is best effort, once per waiting poll and around running analyses.

```bash
TMPDIR=/shared/allie/home/.codex/tmp PYTHONDONTWRITEBYTECODE=1 \
/shared/allie/venvs/hole/bin/python -B -m unittest prediction.test_secondary_analysis -v
```
