The fresh design was prepared without model calls at **2026-09-10 15:04:19 UTC**. The immutable machine-readable evidence is [prospective-design/audit.json](../results/improve-20260910/prospective-design/audit.json); its SHA-256 is `bda5bd50117850310390f2f024e2dfbc8ccadc9ab1e74010a3393fcf3392b37e`.

All 14 focused unit tests passed in 4.07 seconds. A subsequent check of the actual inputs verified the original source files and data hashes, every prepared artifact hash, absence of fresh-player startup markers, and exact agreement with the separately exported training metadata and folds. These checks do not train a model or write fresh outcomes.

| Check | Verified result |
|---|---|
| Previously observed canonical groups | 93: 72 training plus 21 later groups; seven control source groups overlap training. |
| Fresh cohort | 28 unique canonical groups; four per each of seven families; no observed-group overlap. |
| Protocol | Original four player configurations, eight rounds, public history, temperature 0.7, 4096-token cap, two maximum attempts; identity undisclosed. |
| Player schedule | 560 episodes, 1120 focal rows; all ten unordered model pairs per game with two opposite-label trials. |
| Label and context balance | 280 episodes per display orientation; 224 self-play and 336 cross-play episodes. |
| Forecast queries | 448 unique ordered contexts, expanded to the exact 1120 focal rows; self-play context expands to four rows and cross-play to two. |
| Full scope | Exact 1152 training-context IDs and indices from the 72-game export; all 448 fresh contexts. |
| Family-excluded scopes | Exact independently exported LOFO membership; whole family excluded from both focal roles and every training/example row; 64 fresh contexts per scope. |
| LOFO training sizes | 976 contexts for excluding PD, Stag Hunt, or Chicken; 992 for Harmony, coordination, or anti-coordination; 1008 for weak dominance. |
| Kimi query count | 896 total across full and seven family-excluded contexts, with restricted training records supplied before selecting examples. |
| Inference budget metadata | New authorization ledger; $150 shared evaluation ceiling, within the original forecast CLI limit and stricter than the plan's initial $200 cap. |

The code rejects duplicate/malformed forecast probabilities and structurally unsupported non-null probabilities. A missing required method remains visible in declared all-method support even when a pre-outcome technical exclusion allows the run to proceed; numerical-only support is separately exported. The first forecast freeze rejects any fresh status/process/calls/episodes marker. An identical completed freeze can resume after player startup while still checking its bound evidence. The normalized predictions file is always directly hashed and coverage is recomputed from its actual contents.

The root driver must bind the complete candidate/source protocol, Fleet job and artifact lineage for **all** fitted components, preprocessing provenance, full and LOFO trained artifacts, Kimi prompt/example snapshots, and technical-exclusion evidence before collection. File hashes alone cannot prove remote training execution. Actual call trace timestamps must later confirm forecast completion preceded fresh player calls.

A bounded read-only review of the initial root-owned inference wrapper identified two points requiring correction before launch:

1. Running the wrapper with `python -m prediction.improve.inference` imports the `prediction` package before its `sys.path.insert(source)` call. That insertion alone did not redirect package imports: `find_spec` still resolved runner and forecast modules from the live checkout. Enforce the package source path and validate the actual loaded module path. At review time the runner/client/budget bytes matched the old frozen source, but the old player snapshot contained no `llm_forecast.py`; the latter requires the root's new complete snapshot.
2. The initial players branch checked the forecast artifact map and development gate, but did not independently compare `design_audit_sha256` or call `verify_prepared`. The launch path must also verify the prepared manifest, metadata, scopes, original inputs, and source hashes; relying on callers to remember every such file in the forecast evidence list is insufficient.

Both findings were sent to the driver owner. This document records the reviewed implementation and does not certify a later wrapper revision without another check. Ledger construction and actual inference launch are root-owned; the canonical ledger wrapper, rather than distinct symlink filenames passed to SQLite, should enforce the one shared evaluation ceiling.

The scientific scope is deliberately limited: four fresh shapes per known family do not establish transfer to an eighth class; full and family-excluded settings reuse the same outcomes; fixed-fit game/episode intervals do not quantify uncertainty across training seeds or a population of strategic families. Canonical action 0 includes payoff-to-action identification and convention selection. Two opposite-label trials balance the target but provide little replication within an individual game/context. None of the present preparation checks establishes predictive improvement.

Follow-up: the root corrected package-path isolation and forecast/design binding. A 64-query family-excluded preparation smoke test then passed from the archived source with no model calls. The implementation and synthetic collector audit are documented in [integration-audit.md](integration-audit.md).
