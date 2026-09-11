# Execution record: repeated-game prediction

Started 2026-09-10. Authority: execute `plan.md`, autonomously through Gates 1–7; stop expansion if substantial negative results make it uninformative. Gate 8 is outside this run. The user authorized a **$3,000 maximum overnight inference budget**, with economical use. All artifacts and temporary files live under `/shared/allie`.

## Gate 1: proceed with a narrower question

The [prediction literature audit](literature-prediction.md) identifies close precedents for learned LLM behavior prediction, game embeddings, and few-shot agent identification. This study will not claim those broad ideas are new. Companion reviews cover [repeated games](literature-games.md) and [agent identification](literature-identification.md).

The question is: **with the decision protocol fixed, can payoffs predict mechanically measured behavior before an autonomous repeated symmetric 2×2 interaction starts, including transfer across payoff regions, structural families, and model pairings?** This is a proposed empirical distinction, not an established priority claim.

## Protocol decisions before outcomes

- Eight simultaneous rounds, announced horizon, complete public action/payoff history. Each player maximizes its own cumulative points. Each round uses a fresh request with the full public history; private reasoning is not propagated or exposed to the opponent. Opponent model names are withheld from players; the predictor may know them.
- Payoffs are `(R,R), (S,T), (T,S), (P,P)` in canonical coordinates. Players see neutral labels A/B and no named game family. Each independent trial uses an explicitly recorded label permutation, with identical rules and sampling configuration across games.
- Intended player roster: Claude Haiku 4.5, Kimi K3, Qwen 3.8 27B, Gemma 4 31B. Availability and response-format checks may replace an unavailable endpoint before the roster is frozen; no replacement based on behavioral results. Requested temperature 0.7, low reasoning effort where supported, a common fixed completion cap chosen in preflight, no tools or negotiation. Actual settings and model identifiers are saved.
- Pilot: 24 different game structures, all ten unordered pairings of four models, four independent trials each (two per action-label orientation). Self-play uses independent contexts and requests. Both focal directions are measured, with uncertainty clustered by game and entire episode.
- Canonical payoff shape, not display label or affine payoff variant, defines the game-split group. Action permutations and affine transformations cannot straddle game/family/parameter train/test partitions. Pair, model and representation holdouts deliberately test a different axis and may reuse game shapes; that overlap is reported explicitly. Positive scale and additive-offset invariance are tested as sensitivity controls rather than assumed.
- Matrix is the primary presentation. Abstract-text and neutral-narrative renderers are implemented as specified in the plan. A small prespecified representation transfer control is allowed under Gate 6; broader framing research remains Gate 8.
- A/B action rates and first action are universal, mechanically defined targets. Cooperation, retaliation, forgiveness, coordination and exploitation receive explicit applicability rules, event counts and opportunity denominators. Undefined conditional rates are missing, never zero. Retaliation/forgiveness in natural trajectories are descriptive conditionals, not identified causal responses or evidence of intent.
- Preserve all completed, incomplete, invalid and failed requests. An invalid action does not become a default move. Resume checkpoints verify the complete decision context and immutable protocol identity. Retries are bounded and individually charged.

## Predictions and gates

The analysis compares marginal/model-pair, family, raw-payoff, game-feature and combined predictors. Small regularized logistic/linear models and an MLP provide the primary learned approaches. A shallow forest was considered conditionally in the initial execution note but was not included in the final frozen 15-method set; no forest result is claimed. Identity ablations distinguish game, focal model, opponent and pair effects. A prompted LLM receives only game/protocol information and training examples permitted by the split; zero-shot, few-shot and explicit game-feature prompts are recorded separately.

The primary test is structural family transfer, with random-group, parameter interpolation/extrapolation, unordered-pair, model and representation holdouts reported separately. Tuning and scaling use training data only. Unknown model identities map to a declared population fallback; no unseen-model embedding is inferred without evidence. Family evaluation is not replaced by random trial holdout.

Gate 3 asks whether the measurement/rollout protocol is reliable and whether aggregate behavioral differences exceed repeat noise. Gate 4 expands game coverage only if the pilot is informative. Gates 5–7 compare predictions and test transfer even if an initial estimator fails: one failed model does not establish absence of signal. Strong, consistent failures versus baselines and weak repeatability justify stopping expansion and reporting a negative result.

For new prospective test games, save timestamped model artifacts and forecasts **before** collecting their rollouts. Keep exploratory grouped-validation scores separate from prospective evidence. Select a compact prespecified candidate set rather than repeatedly modifying features against test results.

Report MAE/RMSE of measured rates, correlations, probability calibration, Brier and log loss where applicable, game/episode-block uncertainty and missingness. Conditional-rate scoring uses eligible event denominators and reports sparse support. Primary summaries weight game structures equally; extra rounds or model pairs do not create more independent games.

## Resource and completion policy

A new durable ledger enforces the $3,000 ceiling across all prediction calls, including forecasts and retries. A smaller pilot allocation and stage-specific call limits prevent unnecessary expansion; the ceiling is not a spending target. Unknown billing retains a conservative reservation. Hosted FLT usage is reported separately from dollar charges rather than treated as zero compute. No fine-tuning/GPU rental is authorized by progression through Gate 7.

Each gate will have a saved decision with counts, costs, evidence and limitations. Main outputs: literature map, frozen protocol/manifests, generator and deterministic measurement code, complete rollout dataset, fitted predictors and forecasts, split audits, machine-readable metrics and a single Markdown report with plots displayed inline. Negative results and uncompleted conditions remain visible.

## Collection calibration revision

The first full-context collection exposed repeated Gemma-4-31B truncation at the common 4,096-token limit (17 of 336 finished requests in the interim audit; three matches exhausted bounded retries). Larger-cap diagnostic calls answered but took 106–207 seconds. GPT-OSS-20B answered the same three failed contexts correctly formatted in 5–14 seconds. Before the primary pilot analysis, the roster was revised to **Haiku 4.5, Kimi K3, Qwen 3.8 27B and GPT-OSS-20B**, retaining the common sampling settings and cap. This selection used technical reliability and latency, not behavioral rates.

All Gemma calibration calls and traces remain saved and excluded from primary labels. Unchanged non-Gemma pairings resume against their original immutable manifest and checkpoints; a separate immutable manifest collects GPT-OSS pairings. A compatibility audit verifies the identical game, prompts, sampling settings, horizon and action format before the two sources are combined. The primary pilot still contains 24 games × 10 pairings × 4 trials. Original source manifests and interrupted-run status remain available under `results/overnight-20260910/`.

## Independent audit before numerical evaluation

The first supervisor exited while rendering a budget read because SQLite URI read-only mode failed on the shared filesystem. Player collection continued. The report now uses an ordinary SELECT-only connection and marks temporary read failure without stopping science. Only the waiting supervisor was restarted; the player protocol and traces were unaffected.

Gate 3's negligible-variation stop checks both pooled game rates and game variation within each ordered focal/opponent context. Opposing model-pair effects must not cancel into a false conclusion of no signal. Final collection/diagnostic snapshots are separate from the live watcher's mutable outputs. Analysis step markers bind commands, input and computational-source hashes, and saved output hashes; development copies and validates the primary contract on every resume.

Before seeing numerical prediction results, the later spending rule was clarified: a positive unadjusted interval is a screening result, and an interval crossing zero is not evidence of no predictability. One fixed prospective cohort proceeds when the grouped results are positive or inconclusive. Early stopping for a small-effect negative requires adequate prespecified ordered-context contrasts and upper bounds below the declared 0.005 Brier improvement threshold. No predictors or hyperparameters are changed in response to this screen. Prospective missingness and coverage are checked before authorizing further controls. These are operational POC thresholds, not multiplicity-adjusted discovery tests.

An additional formula review identified a limitation of conditional-target comparisons: mean baselines and rate regressors use equal eligible focal-row rates within a game, while logistic fitting and event scoring weight opportunity counts. For varying conditional denominators, improved Brier scores may partly reflect objective weighting rather than structural information. The primary broad targets have eight opportunities per eligible focal row and avoid this discrepancy. The prespecified methods remain unchanged; conditional gains alone will not support a claim that game structure adds predictive information.

## Secondary checks motivated by the pilot

After inspecting the completed 24-game numerical results, a stronger equilibrium-selection comparator and an event-weighted ordered-context baseline were added as secondary sensitivity analyses. The original 15 methods, predictions, hyperparameters and spending gates remain unchanged. The equilibrium selector favors a highest-payoff symmetric pure stage equilibrium when available; tied pure equilibria form a joint mixture of coordinated conventions. This tests how much apparent learned improvement depends on the original comparator's stationary independent equilibrium selection. It does not exhaust repeated-game theory. The context baseline matches the global equal-game event weights before restricting to a focal/opponent context.

This code was archived as `results/overnight-20260910/secondary-source-v1/` at 06:52 UTC, before development collection finished and before any prospective or control player rollout. A separate CPU-only supervisor freezes full-training, excluded-pair and excluded-model secondary forecasts against the same complete future metadata. Forecast timestamps are later checked against actual first target traces. These are prospective secondary tests; comparisons on the pilot or combined training folds remain post hoc. A separate analysis wrapper snapshots inputs and source before computation and rechecks them before declaring an output verified. No additional model calls are needed for these checks.


## Final bounded-study decision

The core Gate 1–7 experiment and all ten secondary analysis jobs completed on 2026-09-10. The final primary pipeline reached `complete_through_gate7` at 09:24 UTC. There are **2,758 valid matches of 2,760 planned**, with only the two recorded pilot failures missing: 958 pilot, 960 additional training, 420 prospective new-game, and 420 control matches. The study contains 93 distinct canonical payoff shapes; the controls reuse seven of them. All 1,008 prompted forecasting queries completed before prospective play. Primary and secondary forecast timing, collection integrity, and saved-analysis provenance passed their respective audits.

The minimum feasibility criterion is supported: payoff information predicts event rates beyond model/opponent averages. The stronger claim remains unsupported. Game-family rates and a stronger equilibrium selector explain much of the improvement, few-shot prompting is competitive with learned predictors, and structural cooperation transfer fails especially on held-out Prisoner's Dilemma. The completed controls reveal presentation sensitivity and a raw-feature offset weakness, with few independent source shapes and historical rather than concurrent anchors. This evidence supports closing the bounded POC rather than starting embeddings, fine-tuning, or additional adaptive experiments.

This closes the core gate sequence, not every checklist item in the broader plan. The [coverage audit](plan-coverage.md) explicitly records unrun training-composition and fixed-game label-noise ablations, missing per-condition confidence intervals, and narrower parameter-region and output-distribution tests. These omissions are not described as preregistered deferrals.

The final experiment ledger records **$33.134662185 in reported charges**, **$42.210622185 including pending/unknown reservations**, and **45,871 recorded requests**, against the $3,000 ceiling. Hosted FLT requests used the existing allocation; the reported dollars do not price that allocation. Unresolved reservations remain preserved. No further experiment inference is scheduled by this run. The [consolidated report](REPORT.md) contains the final scores, uncertainty, controls, and inline figures.
