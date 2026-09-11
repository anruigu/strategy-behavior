# Implementation contract

This fixes interfaces shared by parallel implementers. Root owns orchestration, inference client, manifests, run state and integrated reporting. Do not edit `plan.md`.

Python package `prediction` at repository root. Use `/shared/allie/venvs/hole/bin/python -B`; numerical additions, caches and artifacts must remain under `/shared/allie`.

## games.py

`make_game(game_id, R, S, T, P, **metadata) -> dict` returns JSON-serializable game with `id`, `group_id`, `family`, `payoffs` (dictionary R/S/T/P), `features` (finite numeric dictionary), and metadata. `group_id` invariant to global positive-affine transformations and simultaneous swapping of actions. Raw parameters preserved; normalized features separate. Generator may expose additional helpers.

`generate_games(seed=20260910, n=24) -> list[dict]` reproducible structural coverage and continuous payoff values. `render_game(game, representation='matrix', swap=False) -> str` displays self/other payoffs exactly, no family names. Abstract text and neutral narrative preserve the same payoffs. `payoff(game, action_i, action_j) -> tuple[float,float]` canonical actions are integers 0/1. `game['applicability']` records mechanically justified semantic phenotype applicability and designated cooperative/defective action where supported.

## measurements.py

`measure_episode(trace) -> list[dict]`, one record for each focal player. Trace keys: `id`, `game` (complete game dict), `models` (two model IDs), `trial_id`, `representation`, `swap` (bool), `rounds` (list). Each round has `round` (1-indexed), `actions` ([canonical int0/int1]), `payoffs` ([float,float]); it may include request checkpoint metadata. Completed traces have `status='complete'`.

Each record: `episode_id`, `game_id`, `group_id`, `family`, `model`, `opponent`, `pair` (sorted IDs joined with `|`), `trial_id`, `representation`, `features` (copy game features), `payoffs` (R/S/T/P), `targets` mapping name -> `{value: float|null, successes: int, opportunities: int, applicable: bool}`. Include `action0`, `first_action0`, `cooperation`, `retaliation`, `forgiveness`, `coordination`, `exploitation`; add other clearly named rates if useful. Rates must be in [0,1], absent opportunities produce null. Put signed contrasts, welfare, etc. in separate descriptive fields, never invent binomial counts. Two focal rows from one episode are dependent.

## modeling.py / analysis.py

Input list of measurement records, game features and target fields as above. Train per-target predictors only on supported rows; scores compare common held-out rows. Explicit baseline fallback for insufficient training support. Scaling/encoding fit only on training data. No game/group/family IDs in numeric game predictors (family permitted only taxonomy comparator and split definitions); no observed behavioral statistics in ex-ante features. Model and opponent identity permitted by declared ablation; unseen identity uses unknown fallback. Save numerical artifacts, split membership, per-row forecasts and scores. Unit-test numerical/split behavior with meaningful synthetic cases.

Root can call CLI entry points; document arguments. Keep API calls out of modeling modules. Do not run on test labels before agreed freeze. Matplotlib config /shared/allie/home/.codex/tmp/matplotlib-prediction.
