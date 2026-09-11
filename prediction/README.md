# Repeated-game prediction study

The new parameterized Gameable Games dataset is a separate study: see
[the scale-up dataset and collection tools](scaleup/README.md) and its
[interactive dataset viewer](http://localhost:42329). It covers 24 compact
families, 20 mechanisms, controlled parameter sweeps, and full trajectories.

The [results report](REPORT.md) is the single entry point for findings, gate decisions, costs, and inline figures. The [plan](plan.md) defines the research question; [execution decisions](execution.md) record the operational choices and calibration roster revision. The [coverage audit](plan-coverage.md) distinguishes the core Gate 1–7 experiments from plan checklist items that remain unrun. This study concerns autonomous repeated symmetric 2×2 games. The earlier engine-exploit prediction experiment is a separate dataset and task.

## Current run

Artifacts live in `results/overnight-20260910/`. The primary roster is Claude Haiku 4.5, Kimi K3, Qwen 3.8 27B, and GPT-OSS-20B. Each interaction has eight simultaneous rounds with complete public history, neutral A/B labels, and an own-total-points objective. Each model pair has both label orientations. No LLM judges score behavior.

- `primary-pilot-manifest.json`: 24 games × 10 pairings × 4 trials. `pilot/` retains the original calibration source; `pilot-oss/` supplies replacement pairings. The compatibility-checked primary labels are in `primary-pilot/`.
- `development/`: 48 new game shapes × 10 pairings × 2 trials, conditional on the pilot's reliability and measurable variation. `training-records.json` fixes the combined training snapshot.
- `prospective/`: 21 further game shapes, conditional on sufficient grouped-validation signal. Forecast artifacts must be saved before any player rollout. Fits excluding a model or pairing test joint new-game/identity transfer.
- `controls/`: limited positive-scale, additive-offset, and abstract-text variants, conditional on prospective signal. Narrative framing and Gate 8 research are deferred.
- `gates.json`, `pipeline-status.json`, stage `status.json`, and `steps/`: machine-readable progress and decision evidence. A running process or an implemented analysis is not a completed research gate.
- `budget.sqlite`: global reservations and reported charges against the $3,000 ceiling. Smaller stage ledgers also enforce limits. Unknown billing remains reserved. Hosted FLT usage is counted separately from reported dollar charges.

The original player runtime is frozen under `source/`, with hashes in `source-manifest.json`. Numerical, forecasting, and measurement source was additionally archived under `analysis-source-v1/`, and the full audited execution code under `execution-source-v1/`, before empirical numerical evaluation. Preserve manifests, raw calls, incomplete episodes, fit audits, and forecast sidecars when reproducing an analysis.

Secondary payoff-dominant equilibrium and event-weighted context baselines were added after viewing the pilot. They preserve the original methods and gate criteria. Their source is archived separately under `secondary-source-v1/`; their future forecasts are frozen under `secondary-baselines/` before prospective player runs. Pilot and development comparisons using these methods are explicitly retrospective. See the [secondary baseline interfaces](secondary-baselines-cli.md). The consolidated report includes secondary analyses only after their input-stability audit passes.

## Reproduce analyses

Use `/shared/allie/venvs/hole/bin/python -B` from `/shared/allie/strategy-behavior`. Keep all temporary and dependency files under `/shared/allie`. Numerical dependencies are isolated in `prediction/vendor`; commands must retain the recorded versions and thread settings for the closest reproduction.

Exact numerical versions are listed in [requirements-numerical.txt](requirements-numerical.txt). The run's `environment.json` records Python, package locations and versions, thread settings, and the inference SDK version. The existing shared environment was not upgraded.

```bash
export PYTHONDONTWRITEBYTECODE=1
export TMPDIR=/shared/allie/home/.codex/tmp
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
export MPLCONFIGDIR=/shared/allie/home/.codex/tmp/matplotlib-prediction
export JOBLIB_TEMP_FOLDER=/shared/allie/home/.codex/tmp/joblib-prediction

/shared/allie/venvs/hole/bin/python -B prediction/combine_pilot.py \
  --run-root prediction/results/overnight-20260910
/shared/allie/venvs/hole/bin/python -B -m prediction.diagnostics \
  --records prediction/results/overnight-20260910/primary-pilot/final-records.json \
  --out prediction/results/overnight-20260910/reanalysis/diagnostics \
  --bootstrap 300
/shared/allie/venvs/hole/bin/python -B -m prediction.modeling evaluate \
  --input prediction/results/overnight-20260910/training-records.json \
  --outdir prediction/results/overnight-20260910/reanalysis/evaluation \
  --splits family,random_group,interpolation,extrapolation,pair,model \
  --bootstrap 500
```

Run these only after their input snapshots exist. Use fresh output paths to preserve the original analysis. The [numerical CLI](modeling-cli.md), [prospective join CLI](prospective-cli.md), [LLM forecasting CLI](llm-forecast-cli.md), [continuation driver](after-matrix-cli.md), [sensitivity analysis](controls_analysis.md), and [diagnostics documentation](diagnostics.md) specify interfaces and support rules. Analysis and collection commands make no model calls. `runner.py` and non-prepare-only `llm_forecast.py` perform paid inference; pipeline drivers can launch them.

## Interpretation

The primary learned outputs are conditional expected event rates/probabilities, not a fitted joint distribution over full behavioral trajectories. Game-family holdout is the main structural test. Random-shape, parameter-region, model, pair, and presentation tests answer different questions and remain separately labeled. Both focal players stay together in episode-cluster uncertainty; the independent game count is never inflated by the number of rounds.

The ordered model/opponent mean is the main context baseline. A stationary stage-game Nash selector is a limited comparator and does not characterize the equilibria of the repeated game. Conditional targets are undefined without observed opportunities; retaliation, forgiveness, and exploitation summaries do not establish intent or causal responses. The [measurement formulas](measurements.md), [Nash review](nash-comparator-review.md), and [literature map](literature.md) state the scope in detail.

## Asymmetric payoff pilot

The separate [payoff-mixing readout](asymmetry-pilot.md) crosses four independently chosen player payoff schedules. Its artifacts are under `results/asymmetry-20260910-openrouter/`; they are not included in the core study counts or fits. `asymmetry_smoke.py` supports separate utilities for the two players and renders each player's actual perspective. The original `games.py`, runner, measurements and trained predictors retain their symmetric contracts.

```bash
# Read-only reanalysis of the completed pilot; no model calls.
/shared/allie/venvs/hole/bin/python -B -m prediction.asymmetry_smoke \
  --out prediction/results/asymmetry-20260910-openrouter --analyze-only
/shared/allie/venvs/hole/bin/python -B -m prediction.asymmetry_readout \
  --out prediction/results/asymmetry-20260910-openrouter
/shared/allie/venvs/hole/bin/python -B -m unittest prediction.test_asymmetry_smoke

# A fresh directory with --prepare-only freezes the design without inference.
# Omitting --prepare-only launches 64 forecasts followed by 64 eight-round
# matches, with bounded retries and a separate $20 accounting ceiling.
/shared/allie/venvs/hole/bin/python -B -m prediction.asymmetry_smoke \
  --out prediction/results/asymmetry-reproduction --prepare-only
```

Kimi K3 forecasts use OpenRouter in this pilot because the original FLT Kimi route was unavailable. The failed forecast-only attempt remains under `results/asymmetry-20260910/`, including its original source snapshot. No matches ran in that attempt. The completed experiment freezes every forecast before any player request, balances both model seat orders and both display label orientations, and retains all raw calls.

### Few-shot versus learned predictors

`asymmetry_predictors.py` uses the first 64 asymmetric-pilot matches as a training pool and forecasts 64 fresh matches on the same balanced grid. Every query excludes its entire payoff-equivalence group from fitting and example selection, including player swaps, independent action relabeling, and independent positive affine utility transformations. This is prediction of held-out payoff combinations on fresh repetitions, not a new-shape generalization test.

Kimi gets three nearest distinct allowed game groups, selected by normalized payoffs and matched to the ordered player-model pair. Observed example frequencies pool the two label orientations. Logistic and 16-unit tanh MLP predictors use all allowed training matches with both players' raw/normalized payoffs, best-response gaps, dominance and pure-equilibrium features, display orientation, and model identities. The existing numerical estimator implementations supply train-only scaling, grouped inner tuning for logistic regression, and fixed MLP settings; the symmetric four-payoff features and old fitted weights are not reused. These methods share the allowed training pool but do not receive equal numbers of examples.

Artifacts live under `results/asymmetry-predictors-20260910/`. `manifest.json`, `training-traces.json`, `queries.json`, `numeric.json`, saved models, and `forecast-freeze.json` preserve the full comparison. Original zero-shot forecasts are reused unchanged, and all methods are scored on the same fresh outcomes. The paired bootstrap keeps both focal roles together and resamples payoff groups and whole test episodes, conditional on the fixed fits and forecasts.

```bash
# Existing results: audit and score without inference.
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  /shared/allie/venvs/hole/bin/python -B -m prediction.asymmetry_predictors \
  --out prediction/results/asymmetry-predictors-20260910 --action analyze
MPLCONFIGDIR=/shared/allie/home/.codex/tmp/matplotlib-prediction \
  /shared/allie/venvs/hole/bin/python -B -m prediction.asymmetry_predictors_readout \
  --out prediction/results/asymmetry-predictors-20260910
/shared/allie/venvs/hole/bin/python -B -m unittest \
  prediction.test_asymmetry_predictors prediction.test_asymmetry_smoke

# Fresh output path: prepare only makes no inference calls.
/shared/allie/venvs/hole/bin/python -B -m prediction.asymmetry_predictors \
  --out prediction/results/asymmetry-predictors-reproduction --action prepare
# --action predict fits numerical models and requests few-shot forecasts.
# --action play requires frozen predictions and requests fresh player actions.
# --action run performs all stages under a separate $20 accounting ceiling.
```
