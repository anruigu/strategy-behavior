`post_training.py` continues the fixed improvement study after the **already submitted** Fleet training job. Its default invocation is a read-only dry run. It never imports the Fleet API client, submits another GPU job, cancels a job, fits a model, or reads fresh player outcomes during preparation. Root must explicitly authorize the daemon launch; paid Kimi/player calls require `--execute`.

```bash
/shared/allie/venvs/hole/bin/python -B -m prediction.improve.post_training \
  --run-root /shared/allie/strategy-behavior/prediction/results/improve-20260910
```

Adding `--execute` activates the continuation. `--interval` defaults to 30 seconds and must be between 1 and 60. `--deadline` optionally supplies an explicit timezone-aware wait deadline; otherwise the existing training freeze's conservative deadline applies. The driver only reads the existing worker's `fleet-runtime/training-status.json` and the explicitly selected local terminal monitor record. A failed worker, terminal monitor without verified worker completion, wrong job identity, or expired wait deadline stops downstream work. It does not submit, retry, or cancel GPU jobs. A blocked branch refreshes the declared report and records `behavioral_conclusion=Not evaluated: technical training block`; it does not label a dependency failure as a negative behavioral result. A report-rendering error is recorded separately without concealing the training block.

The driver acquires `RUN/execution.lock`, rejects a live competing Python executor for this run, and passes the locked descriptor to each owned inference subprocess. An orphaned child therefore retains the lock if its parent exits. No competing process is killed. Source, data, prepared queries, protocol, budget policy, and the explicitly selected submission/config are bound in an immutable `post-training/plan.json`. The inference wrapper is copied byte-for-byte into `post-training/inference.py`; its prompts and scientific implementation remain the prepared implementation.

After worker completion, the continuation follows this fixed sequence:

1. Verify the existing Fleet run identity, all 20 completed transformer fits, their exact training-row scopes and Fleet lineage, successful final LoRA optimization, baseline completion, and all saved retrospective/fresh forecast manifests. Map `/mnt/sfs/allie` artifact paths to their `/shared/allie` counterparts and verify their hashes.
2. Score the 20 transformer forecast files, the seven-baseline forecast file, and the saved old-21 Kimi predictions with the unchanged evaluator. Require the complete declared numerical-method/fold inventory. Apply the frozen development gate; a consistent-negative decision stops before fresh prompted or player calls and refreshes the report.
3. Otherwise execute the eight prepared Kimi scopes sequentially, each with its frozen eight-worker setting. Root selected this operational schedule to preserve existing wrapper records; it provides at most eight simultaneous Kimi queries and retains all 896 planned full-plus-family-excluded contexts. The canonical wrapper enforces the existing shared $150 evaluation ledger and the authorization ledger.
4. Join only the three primary targets, preserving exact query IDs, game/model/opponent metadata, and full/family-excluded scopes. Require all nine numerical methods. A terminal `finished_with_errors` Kimi scope receives an explicit timestamped technical-exclusion record linked to its status evidence. Missing Kimi probabilities remain null in all-declared-method support; numerical-only support is reported separately. Missing numerical predictions or malformed metadata stop the continuation.
5. Freeze normalized predictions, coverage, fitted artifacts, training/source lineage, prepared Kimi prompts/examples, raw prompted results/calls, and the development decision before any fresh player startup marker. Then run the frozen player wrapper with 32 episode workers.
6. Collect only terminal player results through the audited integration module, score the saved fresh forecasts, and render the declared final report at `prediction/IMPROVEMENT-REPORT.md`. `--report-out` can override that path under shared storage. Figures remain under `RUN/report-figures`.

Durable step state, child PIDs, logs, errors, and current phase are stored under `post-training`. Completed steps are reused only after verifying their input/source contract, output hashes, and nested artifact evidence. An existing evaluation cannot be adopted if its audit omits any currently required forecast file. A running prior child cannot be relaunched. Original inference checkpoints support bounded resume; partially written immutable scoring outputs are preserved and require an explicit checkpoint audit rather than automatic deletion or replacement. Reports are refreshable derived artifacts.

After fresh scoring finishes, the driver writes `fresh_results_complete_interpretation_pending`, with the explanation “Fresh results complete; scientific interpretation pending.” It does not select a winner or turn a permissive development gate into a positive scientific claim. Root retains scientific disposition. Both fresh forecasting settings use the same player outcomes, and technical exclusions do not establish either predictive success or behavioral failure.

Seventeen focused synthetic tests pass. They cover the dry-run boundary, negative-gate stopping, full continuation ordering, read-only wait/deadline/error handling, foreign job identity, locks and competing executors, completed-step and nested-artifact mutation, live-child resume prevention, exact metadata normalization, missing Kimi support, missing numerical rejection, required-input verification, remote/local path mapping, explicit retry selection and preserved prior evidence, submission/config mismatch, monitor-directory binding, and scalar source/output hashes. Tests use fake orchestration services and temporary files under shared storage; they launch no processes, model calls, or Fleet jobs. The actual-run CLI was exercised only in its default dry-run mode, which returned `paid_calls=false` and `fleet_calls=false` without creating continuation state.

```bash
/shared/allie/venvs/hole/bin/python -B -m unittest \
  prediction.improve.test_post_training -q
```

An already submitted technical retry can be selected with explicit artifacts. These options do not submit a job:

```bash
/shared/allie/venvs/hole/bin/python -B -m prediction.improve.post_training \
  --run-root /shared/allie/strategy-behavior/prediction/results/improve-20260910 \
  --submission fleet-runtime/retry-1-submit.json \
  --config fleet-runtime/retry-1-config.json \
  --monitor-dir fleet-runtime/retry-1-monitor
```

Relative selections resolve within `RUN`; absolute selections must also remain inside that run. Defaults preserve the original `fleet-runtime/main-submit.json`, `main-config-allie.json`, and `main-monitor` paths. The selected submission/config bytes, returned job identity, matching run directory/name, and monitor-directory path are bound into the version-2 continuation plan. The original main submission is also hashed when a retry is selected and is never overwritten. Selecting different artifacts cannot replace an existing immutable continuation plan.

While an explicit retry is starting, the shared worker-status file may still describe the known original job's terminal `error`, `failed`, or `stopped` state. Only that original identity, verified from preserved main submission evidence, is ignored while waiting for the selected retry. An unrelated or live foreign worker remains an error. The selected retry's monitor directory is used, so the original failed monitor cannot be mistaken for the retry's completion. The frozen worker itself still requires its explicit resume/archive procedure for an existing status file; the continuation does not mutate that file.

The generic provenance reader handles both hash dictionaries and the older prompted manifest's scalar `source_sha256` / `output_sha256`. A scalar source hash must identify its source path. A scalar output hash must identify an explicit output, a caller-supplied forecast path, or the unambiguous JSONL sibling of a `.manifest.json` file. Each resolved artifact is hashed and checked; an unbound scalar fails clearly instead of being skipped or treated as a dictionary.
