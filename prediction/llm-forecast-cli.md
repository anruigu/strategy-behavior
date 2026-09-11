# Prompted ex-ante forecast baselines

Implementation: `llm_forecast.py`. Tests: `test_llm_forecast.py`. Importing the module and using `--prepare-only` do not instantiate the inference client or make model calls.

Prepare the immutable inputs and prompts:

```sh
/shared/allie/venvs/hole/bin/python -B -m prediction.llm_forecast \
  --games /shared/allie/strategy-behavior/prediction/results/TEST/games.json \
  --players /shared/allie/strategy-behavior/prediction/results/RUN/pilot/manifest.json \
  --training-records /shared/allie/strategy-behavior/prediction/results/RUN/pilot/collected/records.json \
  --modes zero_shot few_shot game_theory \
  --forecaster kimi-k3 \
  --ledger /shared/allie/strategy-behavior/prediction/results/RUN/budget.sqlite \
  --out /shared/allie/strategy-behavior/prediction/results/RUN/prompted-test \
  --prepare-only
```

The paths above are placeholders. Run the same command without `--prepare-only` to execute or resume. The execution command makes inference calls charged/reserved through `prediction.client.Client`. The global ledger must already exist with its $3,000 ceiling; this module creates a separate stage ledger capped at $150 by default. `--stage-budget` may lower that cap. Hosted allocation accounting follows the existing Client convention. `--workers` defaults to eight and cannot exceed eight. Each query has at most two attempts, including failed-format/failed-transport responses. The forecaster uses temperature zero, low reasoning effort, and a 4,096-token completion limit.

`--games` accepts a game list or a manifest containing `games`. `--players` accepts a JSON file containing the configuration mapping, a manifest containing `models`, a configuration list, or an inline JSON list of configured player model names. **When either input is a full gameplay manifest, the player horizon, temperature, completion cap, and maximum total attempts are inherited from its protocol.** If both inputs contain protocols they must agree. Explicit `--player-rounds`, `--player-temperature`, `--player-max-tokens`, and `--player-max-attempts` options cannot contradict an inherited manifest. With plain lists only, these options override the defaults of eight rounds, temperature 0.7, 4,096 completion tokens, and two total attempts. This permits a revised 16,384-token gameplay protocol without changing the forecaster's own 4,096-token cap. Player configurations must agree with the resolved temperature and retain null seed/low reasoning effort. No player API client is instantiated. Defaults omit few-shot mode; requesting `few_shot` requires eligible training records.

Each forecast query is one game × ordered focal/opponent pair × mode. Self-play gets one model-pair query. These predictions marginalize a balanced mixture of both action-label orientations; they are reused for both self-play focal rows and independent trials when evaluated. The prompt states the complete resolved gameplay protocol, includes both payoff-table orientations, withholds opponent identity from the *players* while giving it to the *forecaster*, and defines all eleven current measurement targets. The schema requires a finite probability for structurally supported targets and null otherwise. Conditional-rate forecasts condition on a qualifying opportunity; they do not claim that an opportunity will occur.

Game features and applicability are recomputed from payoffs. Zero-shot receives protocol, payoffs and mechanically defined target sets. Game-theory mode adds derived numeric payoff features, without taxonomy labels or a request for a reasoning trace. Few-shot adds up to three other-game examples selected deterministically by normalized payoff/incentive distance. Exact ordered-pair examples are preferred when available; otherwise the example's different pair is explicitly disclosed. All query-game canonical groups, including affine/action-swapped equivalents, are excluded from the training pool. The caller is responsible for passing only the split's training records; excluded query groups are an additional safeguard.

Few-shot example counts pool successes and opportunities within an exact payoff configuration and ordered model pair. Differently oriented canonical coordinates are not pooled together. Selected examples have distinct canonical groups. Prompts include observed denominators, number of episodes/focal rows, and swap counts, and explicitly state that rounds/focal rows are correlated. Selection depends on ex-ante metadata rather than outcome values. No eligible examples produces an error before inputs are frozen or calls are made.

Artifacts:

- `inputs.json`: timestamped immutable games, player/forecaster configurations, protocol/definitions, training records, source hashes and budget identity.
- `query-index.json`, `queries/*.json`: immutable exact queries and full prompts, selected-example provenance, prompt/context hashes.
- `calls/*.json`: all raw inference requests/responses and individual cost reservations through Client.
- `results/*.json`: successful probability vector or preserved failed attempts/errors. Completed resumes verify the saved prompt, schema, successful attempt and raw call response/settings.
- `forecasts.jsonl`: one metadata-only row per query and target; status and structural applicability are explicit. Observed labels/counts are null and `eligible=false` before evaluation.
- `status.json`: completion counts, all task errors, current stage/global ledger summaries, completion timestamp and exported forecast-file hash.

Resume permits regeneration only under identical frozen input/context identity. Changing any source hash, player, game, training record, mode, forecaster or budget specification requires a new output directory. Terminal or two-attempt failures are preserved rather than receiving a fresh retry allowance.

To evaluate, join each metadata forecast to completed measurement rows on `(game_id, model, opponent)`, then copy each observation's `episode_id`, `player_index`, `trial_id`, `swap`, target `value`, `successes`, and `opportunities`; assign a common observation `row_index`, split and fold across all compared methods. Set eligibility from observed structural support and positive opportunities, leaving failed forecasts null. The forecast probabilities must remain unchanged. `method` is `llm_zero_shot`, `llm_few_shot`, or `llm_game_theory`. For self-play, attach the same pair-level forecast to both dependent focal rows. Preserve game/episode clustering and exclude observed zero-opportunity conditional rates from scoring.

These forecasts are prospective evidence only if their saved completion timestamps precede target rollout collection. Running this module after target outcomes exist can still produce a blinded payoff-only baseline but should not be described as prospective.

Run offline tests:

```sh
/shared/allie/venvs/hole/bin/python -B -m unittest prediction.test_llm_forecast
```

All thirteen tests passed using fake clients only. They cover finite-probability parsing and null semantics, forbidden test groups including affine copies, deterministic label-blind example selection, pooled counts, prompt isolation, frozen inputs, raw-response verification, bounded attempts, concurrency, metadata-only exports, dynamic manifest-derived player settings and rejection of conflicting protocols. Use training records from the intended permitted training protocol; these measurement rows alone cannot establish which historical completion cap produced them.
