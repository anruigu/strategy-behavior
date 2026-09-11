The continuation driver waits for the existing matrix pipeline, then executes the already bounded prospective and control stages. Importing the module and running its tests make no API calls. Launching the driver can make paid calls after its prespecified screen passes.

```bash
TMPDIR=/shared/allie/home/.codex/tmp \
PYTHONDONTWRITEBYTECODE=1 \
/shared/allie/venvs/hole/bin/python -B -m prediction.after_matrix \
  --run-root /shared/allie/strategy-behavior/prediction/runs/RUN
```

Only one driver may hold `after-matrix.lock`. It waits for `pipeline-status.json` phase `awaiting_prospective_stage`. An upstream stopped/error state or an already terminal continuation exits without inference. Reporting errors are logged in `logs/after-report-warnings.jsonl` and do not abort scientific execution.

The initial screen uses saved development comparisons against the ordered `(focal model, opponent model)` baseline. A positive screen means at least one of `raw_logistic`, `combined_logistic_both`, or `combined_mlp_both` improves event Brier by at least 0.005, with paired-bootstrap lower bound strictly above zero, for `action0`, `cooperation`, or `coordination` on family or random-group holdouts. Inconclusive evidence also proceeds to the single fixed prospective cohort. A decisive stop requires all three methods' universal `action0` comparisons in both splits and an upper Brier-improvement interval strictly below 0.005 for **every available prespecified contrast**. Only that stop is labeled `informative_negative`. Missing or wide intervals do not establish a negative. These are unadjusted descriptive intervals across multiple contrasts, not a multiplicity-adjusted discovery procedure.

Positive or inconclusive retrospective evidence freezes a 21-game prospective manifest from seed 20260912, rejecting any training canonical-group overlap. The exact four-player configuration, protocol, source hashes, source directory, and existing $3,000 ledger are inherited from the primary manifest and checked against development. Each game has all ten unordered pairs, two trials, and alternating action display swaps: 420 planned episodes. The player-stage limit is $250. The cohort is not enlarged in response to results.

Three immutable training snapshots retain all training rows, exclude every Kimi/GPT-OSS interaction, or exclude every interaction involving GPT-OSS. Both focal rows remain together. Three numerical bundles are fit and forecast the **entire** planned prospective metadata, including the excluded pair/model. The prompted zero-shot, few-shot, and game-theory baselines then use Kimi with training records only and a separate $150 stage limit. Every numerical and prompted forecast must reach its final export before player launch. Failed prompted queries retain missing probabilities.

The driver then uses the existing launch/wait mechanism and the frozen collection script. Scoring validates source hashes, complete planned identity, and forecast completion strictly before the earliest actual episode start. Outputs are:

- `prospective/evaluation`: numerical and prompted comparisons, with common-support scoring and explicit missingness.
- `prospective/evaluation-numerical`: numerical-only comparisons, preserving evidence when prompted forecasts fail.
- `prospective/evaluation-pair`: the excluded-pair fit, scored only on the held unordered pair after full-stage identity validation.
- `prospective/evaluation-model`: the excluded-model fit, scored on every episode containing the held model after full-stage identity validation.

Each evaluation saves scores, joined predictions, hash/timestamp audit, and coverage. Calibration/comparison plots are saved when supported scores exist; empty common support is a valid documented result and does not require plot files. Numerical-only scoring runs before the combined prompted comparison. Gate 6/7 records retain these audits and contrasts. At least 90% completed episode coverage is required before scientific or control decisions; partial scores remain available after a coverage stop. The second expansion screen uses the numerical-only prospective scores and the same three methods/targets, requiring a 0.005 point improvement over ordered context. Its interval is reported but need not exclude zero. Without this trigger, paid controls are skipped. A decisive interval-based exclusion is labeled `informative_negative`; otherwise the completed prospective evaluation ends `complete_through_gate7` with explicit `inconclusive / controls unsupported` evidence.

If the prospective screen passes, controls use the first seven primary pilot games, which must cover seven families. Each receives scale ×3, offset +10, and abstract text variants. `make_game` derives exact two-decimal payoffs; the source canonical group is asserted unchanged. Game metadata records `control_variant`, `source_game_id`, and `source_group_id`. Scale/offset use matrix presentation; abstract text uses `text`. Two trials use swaps false/true, with all ten pairs: another 420 episodes, capped at $200. The original full training fit forecasts all controls before their launch. No prospective labels enter a refit. Results are saved under `controls/evaluation`; successful completion ends with `complete_through_gate7`. No Gate 8 tuning, embeddings, narrative, or counterfactual-dose work runs.

Offline label sensitivity runs before either continuation decision in `primary-pilot/label-analysis`. If controls run, paired source-game sensitivity is saved to `controls/sensitivity`. Both analyses include derivation data and figures; neither launches inference.

Durable states progress through freezing, prompted forecasts, prospective rollout/scoring, and controls. `after-matrix-plan.json` freezes seeds, source and input hashes, screens, budgets, and exclusions. Every subprocess has a marker under `steps/after-*.json` binding exact arguments, input bytes, computational source hashes, and all declared/generated output hashes, including figures. Completed steps are reused only when those hashes match. Manifests, snapshots, fits, forecasts, and evaluation outputs are never overwritten. `forecast-freeze.json` binds all completed forecasts before launch; scoring independently audits actual trace timing.

An incomplete/error step, changed artifact, unexpected existing player stage without its freeze, incompatible source/protocol, or failed prospective audit stops with durable `after_matrix_error`. Such a checkpoint requires explicit inspection before resume; the driver does not silently retry a partial fit, prompted run, or forecast export. Missing player outcomes are recorded, not fabricated; integrity errors stop expansion. Final reporting runs for both informative negatives and completion.

```bash
TMPDIR=/shared/allie/home/.codex/tmp PYTHONDONTWRITEBYTECODE=1 \
/shared/allie/venvs/hole/bin/python -B -m unittest prediction.test_after_matrix -v
```
