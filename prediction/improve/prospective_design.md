The fresh cohort contains **28 new canonical shapes, four per declared family**, generated with fixed seed 20260913 and checked against all 93 previously observed shapes. The prior 72 training shapes, 21 later shapes, and seven control source shapes are read-only inputs; the control shapes are duplicates within the 72. All candidate generation uses payoff metadata only. A deterministic prefix is extended if a candidate collides with observed groups, preserving the four-per-family quotas without inspecting fresh outcomes.

The player manifest copies the original four model configurations, eight-round public-history protocol, sampling settings, and frozen source hashes. Every shape has all ten unordered pairs and two opposite-label trials: 560 matches, 1120 focal rows, 280 episodes per display orientation, 224 self-play episodes, and 336 cross-play episodes. Forecast input is metadata only. No player calls, training, fitting, or model inference occur in this module.

Preparation is local and authorized; only the root driver may launch forecast or player calls after freezing the complete method/source protocol:

```bash
/shared/allie/venvs/hole/bin/python -B -m prediction.improve.prospective_design \
  --previous-root /shared/allie/strategy-behavior/prediction/results/overnight-20260910 \
  --run-root /shared/allie/strategy-behavior/prediction/results/improve-20260910
```

The generated stage points to RUN/authorization-budget.sqlite, a new root-owned authorization ledger containing the imported prior commitment. It does not modify or use the old run's mutable ledger. Following root's concrete budget amendment, the shared evaluation ceiling is 150 USD, stricter than the plan's 200 USD ceiling and compatible with the original Kimi CLI's 150 USD maximum. The root-owned inference.py wrapper routes every original Ledger constructor to the canonical RUN/eval-budget.sqlite filename, so all scopes and players share one SQLite database and journal path. Per-output budget.sqlite symlinks are display conveniences only. The manifest sets stage_budget_usd to 150; a per-process cap alone is not a combined cap. The original runner and Kimi CLI use the literal stage filename budget.sqlite. Ledger initialization, imported accounting, wrapper validation, and API calls belong to root.

Artifacts are immutable:

| Path relative to new run | Content |
|---|---|
| fresh-prospective/manifest.json | Exact original-runner-compatible 560-episode manifest. |
| fresh-prospective/metadata.json | 1120 target-free original-schema focal rows in manifest order. |
| prospective-design/queries.json | 448 deduplicated game/model/opponent contexts, using data.py metadata-derived IDs. |
| prospective-design/training-example-metadata.json | 1152 metadata-only contexts in the same order and with the same IDs as the training exporter. |
| prospective-design/scopes.json | Full 72 and seven family-excluded memberships in original-row and aggregated-example coordinates. |
| prospective-design/expansion.json | Each query's exact player episode/role/trial/display expansion. |
| prospective-design/players.json | The fixed player configuration and protocol for the old forecast CLI. |
| prospective-design/scopes/SCOPE/training-records.json | Only the permitted original training rows for this scope, retaining all labels/counts. |
| prospective-design/scopes/SCOPE/games.json | Full 28 or the held family's four query games with fixed protocol. |
| prospective-design/scopes/SCOPE/queries.json | The exact 448 or 64 prepared query contexts. |
| prospective-design/audit.json | Source/input/artifact hashes, seed, group counts, chronology requirement, and scope inventory. |

Scopes are full and family_FAMILY, with settings full and family_excluded. Full uses all 1152 training contexts from 72 shapes and 448 fresh query contexts. Family-excluded scopes remove the held family from every original training row, both focal roles, repeated episodes, and every aggregated example. They query only that family's 64 contexts from four new shapes. Together the seven family scopes partition the same 448 contexts / 1120 player rows used by full. The real training membership sizes are 976 contexts when excluding PD, Stag Hunt, or Chicken; 992 for Harmony, equal-diagonal coordination, or anti-coordination; 1008 for weak dominance. No later 21-shape development outcomes enter fitting or examples.

The data exporter and this design share metadata_examples(records, protocol). Its IDs exclude outcomes, trials, and display swaps. Context forecasts marginalize the balanced orientations and are expanded to player outcomes only for scoring; self-play queries expand to four focal rows, cross-play queries to two. This expansion must preserve both focal roles and entire episodes in any bootstrap. Group IDs remain in metadata for splitting and grouping; game IDs and named family labels are not placed in predictor text. The explicit taxonomy baseline alone may consume family labels.

**Kimi three-example comparator.** Reuse the unchanged original CLI separately for each of the eight scopes. This is 448 full-training queries plus 7 × 64 family-excluded queries, 896 prompted forecasts. Every scope receives its own restricted training-records.json before the original example selector runs. It selects three distinct permitted training shapes, prioritizes the exact ordered model/opponent context, and excludes query groups. There are no target-shape examples in either setting. The original visible prompt strips opaque IDs and family names.

The root-owned adapter uses these arguments (preparation only is shown):

```text
-m prediction.llm_forecast
--games RUN/prospective-design/scopes/SCOPE/games.json
--players RUN/prospective-design/players.json
--training-records RUN/prospective-design/scopes/SCOPE/training-records.json
--modes few_shot
--forecaster kimi-k3
--ledger RUN/authorization-budget.sqlite
--stage-budget 150
--out RUN/fresh-forecasts/few_shot/SCOPE
--prepare-only
```

Root invokes these unchanged CLI arguments through the inference.py wrapper to enforce canonical shared-ledger routing. Removing --prepare-only makes paid inference and is not performed by this module. The legacy Kimi prompt requests all 11 descriptive targets and shows the corresponding permitted example counts. Only action0, mutual cooperation, and coordination enter the follow-up's primary improvement claim. This legacy comparator therefore retains richer example supervision than the three-target learned heads; it is documented rather than silently altered. No game-playing agent is fine-tuned.

**Forecast and chronology interface.** Root normalizes candidate exports to JSON/JSONL rows with scope_id, method, row_id, target, and prediction. row_id is the aggregated context ID. target is one of action0/cooperation/coordination. Structurally supported targets require a finite probability in [0, 1]. Inapplicable targets must be null or absent. Fresh successes, opportunities, observed values, or target supervision are forbidden in these pre-outcome rows.

forecast_coverage(scopes, queries, predictions, required_methods, numerical_methods, technical_exclusions=()) rejects duplicate keys, undeclared scopes/methods/queries, incorrect target masks, nonfinite/out-of-range probabilities, and outcome-bearing rows. Its 24 scope×target cells preserve all-declared-method and numerical-only query intersections separately, plus every method's valid IDs and all missing predictions. Missing/invalid forecasts are never assigned a favorable default. An incomplete scope/method can pass the technical gate only with an explicit timestamped technical-exclusion record containing scope_id, method, reason, and created_utc. The exclusion does not silently remove missing predictions from the all-declared-method intersection. Entirely absent required methods can therefore leave all-method support empty; numerical-only results must remain separately labeled.

freeze_forecast_evidence(run_root, files, coverage, normalized_predictions_path, created_utc=None) re-reads the actual normalized forecast bytes, recomputes coverage on the exact prepared queries/scopes, and binds their hash alongside all supplied concrete evidence files. Root must include the machine-readable candidate protocol, original output files, full model/checkpoint and calibration/head artifacts, training partition provenance, Fleet submission/result records, Kimi prompt/example snapshots, timing records, and any exclusion evidence. The helper does not verify remote-service execution merely from an arbitrary label; root must audit that every fitted component—including calibration and probability heads—was trained through the Fleet API on its exact permitted scope. Learned preprocessing/scaling must also have training-only provenance. Deterministic equilibrium rules do not acquire training labels through this helper.

The first freeze rejects any fresh process.json, status.json, episodes directory, or calls directory. It binds the prepared design audit and all forecast/provenance files. A completed identical freeze can be verified and reused after players start; it cannot be replaced with changed evidence. verify_prepared(run_root) likewise supports read-only resume after startup and detects modified data, metadata, scopes, source, or original inputs. The prepared audit binds the original frozen player source bytes as well as the new design/data implementations; the driver must verify the design audit hash and import the actual frozen player source directory before launch. prepare() itself always requires an unstarted stage and is not a post-launch regeneration command. The root driver remains responsible for requiring successful optimization/technical diagnostics, applying the stated development gate, and checking both budgets before invoking the original frozen runner. Collection must later recheck actual trace start times against the forecast freeze, not rely solely on file ordering or a claimed creation timestamp.

**Scientific limits to retain.** The 28 fresh shapes are four examples of each of the same seven archetypes, not 28 new families or an eighth strategic class. Full 72 and family-excluded forecasts are two settings on the same player outcomes; they are not independent replications. A shape/episode bootstrap is conditional on fitted predictors and does not establish uncertainty over a population of strategic families or training seeds. Primary structural target support is 28 action shapes, 20 cooperation shapes, and 16 coordination shapes before collection failures; their maximum focal opportunity counts are 8960 / 6400 / 5120. Rare conditional targets are outside the primary claim.

The fixed two trials per pair provide one instance of each display orientation. They support a balanced target, but only limited repeatability measurement for any specific new game/context. Canonical action0 remains an encoded-action target: gains can reflect identifying the dominant/cooperative action or selecting a convention, not necessarily fine-grained behavioral sensitivity within a family. The corrected interpolation/extrapolation folds belong to data.py; family coverage and bracketing should be evaluated there using metadata, without consulting fresh outcomes. The improvement threshold and fixed candidate set must be frozen before comparing improvement scores. A technical exclusion recorded after fresh behavior is visible is not a pre-outcome exclusion.

Verification:

```bash
/shared/allie/venvs/hole/bin/python -B -m unittest prediction.improve.test_prospective_design -v
```

Fourteen meaningful tests cover family quotas and collision continuation, complete pair/label schedules, payoff/protocol corruption, new-ledger isolation, whole-episode LOFO exclusion, query expansion and self-play dependence, training/query leakage, outcome-free metadata, missing-method common support, invalid and unsupported probabilities, all startup markers, immutable resume, source/input mutations, forged coverage, and late exclusions. A separate read-only check against the actual original data verifies the 93-group union, 28 new groups, 1152 / 448 training/query contexts, and exact scope sizes. No model training, player calls, or fresh outcomes are produced by these checks.

Actual preparation completed at 2026-09-10 15:04:19 UTC in results/improve-20260910. A subsequent read-only verification checked every prepared/source/input hash, absence of player startup markers, and exact agreement of training metadata IDs and all eight scope training-index arrays with data/data.json and data/folds.json. The original runner, datasets, and ledgers were not modified.
