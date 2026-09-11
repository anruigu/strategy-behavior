# Live pilot watcher

Run from the project root after any manual collection or diagnostic refresh has finished:

```bash
/shared/allie/venvs/hole/bin/python -B -m prediction.watch \
  --run-root /shared/allie/strategy-behavior/prediction/runs/RUN_NAME \
  --interval 120
```

The watcher monitors only `pilot` and `pilot-oss`. It makes no model API calls, starts no source jobs, and writes no gates or pipeline status. It writes its own `watcher-status.json`, owns a `watcher.lock`, refreshes collection/diagnostic artifacts, and renders `prediction/REPORT.md`. The advisory lock excludes other watchers for this run; it does not coordinate manual diagnostic processes.

Every 120 seconds by default, it examines each source's process and status markers. Process ownership requires the exact recorded manifest argument and a `runner.py` command. A zombie or dead PID is stopped. A stopped source with a current-launch `complete` or `finished_with_errors` status is normally terminal. Full error-free coverage yields `complete`; failed episodes, reported episode errors, or incomplete coverage yield `complete_with_errors`. Source error details and actual counts are retained. A stopped process without a valid current terminal marker is interrupted. Missing process markers receive a 300-second startup grace. Unknown process state remains pending rather than certifying completion.

A live source keeps the watcher running even if the other source has stopped or failed. After at least 30 additional source completions, the watcher runs `combine_pilot.combine`, then `diagnostics.run` on `primary-pilot/records.json` with 100 bootstrap replicates and output `pilot/diagnostics`, then `report.render`. The frozen collector and primary manifest determine admissible records, including quarantine filtering. The first refresh is immediate when the initial source total is at least 30; a changed launch marker also forces a refresh after a previous successful refresh. Report notices update on source state changes even below the collection threshold.

When both sources have stopped, it performs a final collection, diagnostics with 300 bootstrap replicates, and report rendering. It records `complete` only if both sources ended without errors and the combined primary collection has every planned episode. Normal terminal runners with failed or missing episodes yield `complete_with_errors`, with actual validated coverage and missing episodes preserved. The watcher applies no percentage-based coverage gate; the pipeline evaluates that separately. Interrupted source processes, final integrity errors, failed final collection, or failed final reporting yield `interrupted`. Required missing manifests cannot certify completion. The report labels running, interrupted, and normally finished partial displays honestly and includes validated episode counts. Collection completion does not assert that later study gates are complete. Both normal terminal states return CLI exit code zero; interrupted returns one.

`--max-hours` defaults to 24 and stops only this watcher. SIGINT and SIGTERM request the same graceful stop. Idle waits use short interruptible chunks; an active collection or plotting operation finishes before the stop request is handled. `--once` performs one observation and eligible refresh. `--minimum-new`, `--startup-grace`, and `--report` override the remaining defaults. All write paths must resolve under `/shared/allie`.

Verification:

```bash
/shared/allie/venvs/hole/bin/python -B -m unittest prediction.test_watch -v
```

The tests cover process ownership, zombie detection, startup grace, stale completion markers, partial-source failures, refresh thresholds, report notices, collection failures, and the final completion audit. They use synthetic markers and injected collectors; they launch no inference jobs.
