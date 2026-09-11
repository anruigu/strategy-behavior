# Frozen prospective forecasts and later outcome joins

`prospective.py` builds planned focal-player metadata and scores existing forecasts. It makes no API calls and never refits predictors or rewrites source forecasts.

Before any target rollout, build metadata from the final stage manifest, then use those exact rows as the input to `prediction.modeling forecast`:

```bash
/shared/allie/venvs/hole/bin/python -B -m prediction.prospective build-rows \
  --manifest prediction/results/RUN/test/manifest.json \
  --output prediction/results/RUN/test-metadata.json
/shared/allie/venvs/hole/bin/python -B -m prediction.modeling forecast \
  --artifact prediction/results/RUN/training-models.pkl \
  --input prediction/results/RUN/test-metadata.json \
  --output prediction/results/RUN/test-forecasts.jsonl
```

The metadata has exactly two focal rows per planned episode, preserving the manifest order, model roles, trial, representation, swap and game features/payoffs. It contains no targets. `planned_manifest_sha256` binds the entire stage configuration, including the decision protocol, to the numerical forecast input hash. Output metadata and its companion manifest refuse overwrite.

After collecting outcomes:

```bash
/shared/allie/venvs/hole/bin/python -B -m prediction.prospective score \
  --forecasts prediction/results/RUN/test-forecasts.jsonl \
  --llm-forecasts prediction/results/RUN/prompted-test/forecasts.jsonl \
  --records prediction/results/RUN/test/collected/records.json \
  --stage-root prediction/results/RUN/test \
  --out prediction/results/RUN/prospective-evaluation \
  --split prospective --bootstrap 300
```

Omit `--llm-forecasts` when unavailable. Numerical forecasts join on episode, player, target and method. LLM forecasts join on game, ordered model/opponent context, target and method, then broadcast the identical saved probability across planned trials and both self-play focal rows. The resulting methods share a common observation `row_index` and retain game/episode clustering.

Duplicate or conflicting keys, unexpected outcomes, incompatible game/model metadata, invalid probabilities, prepopulated forecast labels and forecast/hash mismatches raise an error. Missing outcomes remain visible in `coverage.json`; zero opportunities produce an unscorable null rate, while unknown counts remain null. The helper validates every outcome and forecast before applying an optional focus:

```bash
# Score a joint new-game/new-pair test using forecasts from the pair-excluded fit.
... score ... --focus-pair 'kimi-k3|gpt-oss-model-id' --split prospective_pair
# Keep both focal roles whenever the excluded model appears in either role.
... score ... --focus-model 'gpt-oss-model-id' --split prospective_model
```

Use actual manifest model IDs in these placeholders. Focus options are mutually exclusive. Even for a focused score, create numerical forecasts for the complete metadata file so the full stage/input hash remains verifiable.

Prospective verification requires the numerical forecast hash and input hash, compatible frozen LLM inputs/protocol when present, and all forecast completion/export timestamps strictly before the earliest saved target trace start. Completed, progress and incomplete traces contribute timestamps. Every observed outcome episode must have trace timing evidence. A missing or failed temporal audit still permits scoring, but uses an `unverified_` split prefix, marks `prospective_verified=false`, and labels plots accordingly. Without `--stage-root`, there is no verified prospective claim; `--planned-rows` can still supply immutable metadata for identity checks. These checks rely on saved timestamps and hashes, not external notarization.

The new output directory contains `joined-predictions.jsonl`, `scores.json`, `coverage.json`, `audit.json`, and available Brier/calibration plots. The audit records source hashes and timing evidence. Input bytes are checked again after scoring to detect concurrent changes; the source forecast files remain untouched. Existing output directories are refused.

Run the synthetic tests with:

```bash
/shared/allie/venvs/hole/bin/python -B -m unittest prediction.test_prospective -v
```
