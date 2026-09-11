# Game-structure prediction pilot

Offline prediction of revised45 behavioral activation from ex-ante structural features. This package is separate from `mechanism_pred/`, which predicts negotiation outcomes with an LLM.

[Completed pilot report](../../research_logs/sep/prediction-pilot-results.md).

The first evaluation is negative: the fixed 14-feature structural logistic model performs worse than the player-model/prompt baseline under held-out game-family and family-purged mechanism validation. This is an exploratory result for one representation and estimator, not a conclusion that structural prediction is impossible.

## Pipeline

1. `features45.py`: reads the frozen revised45 engine source and canonical witness definitions; generates 135 feature rows, checks all 45 witnesses on three seeds and their one-mechanism patches. Never reads player outcomes. Seven interface features plus seven witness features; the latter assume designer/oracle access.
2. `snapshot45.py`: takes a fixed snapshot of completed revised-game outcomes and records source hashes. Old disclosed-rules data is excluded; missing outcomes are not zeros. Refuses to overwrite its snapshot.
3. `model45.py`: NumPy-only penalized logistic regression, with train-fold-only scaling and categorical vocabularies. No game/target/family/seed/taxonomy identifiers enter structural predictors. Taxonomy is used only by its explicit baseline and for split construction.
4. `run45.py`: fixed L2=10, four grouped holdout schemes, separate unhinted and hinted cohorts, Brier/log-loss evaluation, fold audit, out-of-fold probabilities and fitted forecast artifacts. No hyperparameter tuning.
5. `report45.py`: inline metrics and calibration plots plus limitations and per-family failure analysis.
6. `forecast45.py`: makes timestamped forecasts from a saved artifact for known player-model/prompt contexts; marks targets seen in training and refuses to overwrite predictions.

All scripts operate without inference/API requests. Use `/shared/allie/venvs/hole/bin/python -B`. Set `OPENBLAS_NUM_THREADS=1` and `OMP_NUM_THREADS=1` for fitting; set `TMPDIR` and `MPLCONFIGDIR` under `/shared/allie/home/.codex/tmp`.

Initial immutable inputs and complete output live under `benchmark/results/prediction45-pilot-20260910/`. For a new data cutoff, use a new output directory, run feature extraction and snapshotting there, then run fitting/reporting. Do not update a completed pilot's behavioral snapshot in place.

## Interpretation

Primary outcome is `P(engine activation | structure, known model, prompt)`. Independent discovery labels do not exist; activation is not discovery, and hinted rescue is not `P(execute | discovered)`. Hinted trials are selected on prior exploration misses and therefore modeled separately.

Canonical witness length is not minimum search complexity. Score contrasts use fixed witness prefixes plus deterministic normal-policy continuations on vulnerable and patched engines; they are not optimal expected payoff estimates. All feature evidence is exported for audit.

All model, prompt and seed variants of a held-out target stay outside training. Family splits hold out every edition sharing the same engine `BASE`; strict mechanism splits additionally purge all families represented by that mechanism. This tests retrospective out-of-sample prediction, not a prospective study. Fresh game families with forecasts frozen before behavior collection are the next validation stage.

Regression tests cover grouped leakage, training-only scaling, identifier isolation, numerical convergence, serialization and forecast input/context validation.
