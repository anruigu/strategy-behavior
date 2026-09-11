These are **secondary controls designed after inspecting pilot results**. They do not replace the original 15 methods, change gate criteria, or make the pilot analysis preregistered. Freezing them before new target outcomes supports a secondary prospective test. Every command is local CPU work; this module imports no inference clients and launches no paid jobs.

`secondary_payoff_dominant` selects the symmetric pure stage Nash profile with the highest common payoff whenever one exists. Equal-payoff symmetric-pure maximizers receive equal **joint profile** probability. For tied coordination equilibria this assigns 0.5 to `(0,0)` and 0.5 to `(1,1)`: action0 probability is 0.5 and coordination probability is 1. This is a mixture of coordinated conventions, not independent mixed actions or a public randomizer provided by the protocol. The forecast marginalizes balanced display swaps. A literal policy of always choosing displayed A would instead predict canonical action0 `1-swap` on each trial; that conditional information is not used here. With no symmetric pure equilibrium, the comparator retains independent symmetric mixed play. Supported targets are action0, first_action0, cooperation, and coordination; mechanically undefined targets remain null. No conditional-response forecasts are invented.

`secondary_pair_event` is an optional training-only ordered `(focal model, opponent model)` baseline. Let `N_g` be all eligible training opportunities in game `g`, and `S_gc`, `N_gc` be successes and opportunities for context `c`. Its forecast is:

```text
p_c = sum_g(S_gc / N_g) / sum_g(N_gc / N_g)
```

This applies equal-game event weights globally before restricting to a context, matching the original logistic training weights and event-Brier evaluation objective. Averaging `S_gc/N_gc` equally across context-specific games would define a different objective when context opportunity shares vary. Unknown contexts use the all-training equal-game event mean. Targets with no eligible training events predict null. Missing/zero exposure is excluded, with explicit per-game counts and weighted totals retained in the artifact. This is a weighting sensitivity check motivated by the pilot, not an added primary baseline.

Use the existing Python environment:

```bash
TMPDIR=/shared/allie/home/.codex/tmp PYTHONDONTWRITEBYTECODE=1 \
/shared/allie/venvs/hole/bin/python -B -m prediction.secondary_baselines fit \
  --training-records TRAINING.json --artifact secondary-fit.json
```

Omit `--training-records` for the deterministic equilibrium rule alone. `secondary-fit.json` stores configuration, post-pilot motivation, computational source hashes, training snapshot hashes, and optional ordered-context count audits. Full, pair-excluded, and model-excluded training snapshots can each produce a separate artifact; filtering remains the supervisor's responsibility.

Freeze predictions on **complete label-free metadata** before any target rollout:

```bash
/shared/allie/venvs/hole/bin/python -B -m prediction.secondary_baselines forecast \
  --artifact secondary-fit.json --input STAGE/metadata.json \
  --stage-root STAGE --output secondary-forecasts.jsonl
```

This writes `secondary-forecasts.jsonl` and `secondary-forecasts.manifest.json`. The sidecar includes the exact input hash expected by the unchanged prospective scorer, forecast bytes hash, creation timestamp, artifact/training/source hashes, and secondary classification. Both focal rows of every planned episode are required. `--stage-root` checks metadata against the full stage manifest and rejects a stage with any process/status/episode artifacts. Existing output files are never replaced.

An optional `--primary-forecasts PRIMARY.jsonl` copies a verified existing primary forecast and these secondary rows into a **new** combined export, preserving and hashing the source files. Such an export must itself be created before target play if used for prospective scoring. This option is unnecessary for the safer standalone workflow below, which allows secondary forecasts to be frozen well before primary forecasts are ready.

After outcomes arrive, score each standalone secondary export through the unchanged scorer:

```bash
/shared/allie/venvs/hole/bin/python -B -m prediction.prospective score \
  --forecasts secondary-forecasts.jsonl --records STAGE/collected/records.json \
  --stage-root STAGE --split prospective --out secondary-evaluation
```

Use the same split and focus arguments as the corresponding primary evaluation (`--focus-pair` or `--focus-model`), while preserving forecasts on full metadata. Controls use `--split prospective_controls`. The existing scorer verifies that actual forecast completion precedes the earliest target trace. Configuration timestamps alone do not establish prospectivity.

Compare the two independently audited evaluations offline:

```bash
/shared/allie/venvs/hole/bin/python -B -m prediction.secondary_baselines compare \
  --primary-evaluation PRIMARY_EVALUATION --secondary-evaluation secondary-evaluation \
  --out secondary-comparison --bootstrap 500
```

Both source audits must say `prospective_verified=true`, identify the same outcome snapshot/split, and retain their original source hashes. The helper checks probabilities against the audited source forecasts, outcomes against the original collection, duplicate method keys, complete focal support, row indices, episode/player identities, and fold metadata. It then concatenates scored rows and uses the existing game-equal scoring and paired bootstrap. It creates an analysis artifact, not a new forecast, and never backdates a combined prediction.

For explicitly post hoc pilot/development sensitivity:

```bash
/shared/allie/venvs/hole/bin/python -B -m prediction.secondary_baselines retrospective \
  --records ORIGINAL_RECORDS.json --evaluation PRIMARY_EVALUATION \
  --out secondary-retrospective --bootstrap 500
```

`PRIMARY_EVALUATION` must contain the preserved `run_config.json`, `folds.json`, and `predictions.jsonl`. The original input hash, saved test membership, identities, and labels are verified. Secondary context means are fit on each saved training partition only; no fold is regenerated or retuned. The audit retains original train/test indices and per-fold count fits. Original predictions and methods remain unchanged. The output is explicitly marked `secondary_post_pilot_retrospective_sensitivity` and not prospective.

Both analysis commands write `joined-predictions.jsonl`, `scores.json`, `secondary-comparisons.json`, and `audit.json`, plus plots when supported scores exist. `scores.json` retains original marginal/ordered-pair comparisons and adds `comparisons_to_secondary`; positive differences mean the named method improves on the indicated secondary baseline. These contrasts use the same common support and game/episode bootstrap as the original scoring. Empty support is retained rather than converted to zero error. Output directories must be new.

```bash
TMPDIR=/shared/allie/home/.codex/tmp PYTHONDONTWRITEBYTECODE=1 \
/shared/allie/venvs/hole/bin/python -B -m unittest prediction.test_secondary_baselines -v
```
