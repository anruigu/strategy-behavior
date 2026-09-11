# General Games · replicated v2

Purpose: predict ordinary native-game behavior and test training headroom beyond few-shot prompting. Families are selected for distinct decision structures, without selecting or modifying games for exploitability. This is a purposive sample, not random coverage of all games.

The design contains **16 families, 57 configurations, 114 fresh seeded instances, and 85 distinct opening-snapshot groups**. The last unit hashes configuration plus the native opening snapshot; it is not a count of unique actor-visible prompts or full future random streams. The engine remains installed TextArena 0.7.4.

| Native family | Players | Role in this study |
|---|---:|---|
| Connect Four | 2 | Historical training and catalog coverage |
| Nim | 2 | Historical training and catalog coverage |
| Kuhn Poker | 2 | Historical training and catalog coverage |
| Liar's Dice | 2 | Historical training and catalog coverage |
| Blind Auction | 2 | Repeated capital sweep |
| Resource Negotiation | 2 | Historical training and catalog coverage |
| Iterated Prisoner's Dilemma | 2 | Repeated payoff sweep |
| Colonel Blotto | 2 | Repeated unit-budget sweep |
| Pig Dice | 2 | Repeated winning-target sweep |
| Tower of Hanoi | 1 | Historical training and catalog coverage |
| Mastermind | 1 | Historical training and catalog coverage |
| Wordle | 1 | Historical training and catalog coverage |
| Iterated Ultimatum | 2 | Prospective new-family test |
| Two-Thirds Average | 2 | Prospective new-family test |
| Secretary | 1 | Prospective new-family test |
| Memory | 2 | Prospective new-family test |

The frozen new collection plan completed **592 episodes**: 320 training, 160 higher-parameter test and 112 new-family test. It uses 20 configurations / 40 seeded instances. Two world seeds cross every focal seat and both models independently. Each anchor condition has five independent LLM repetitions; new families have two. Including the 144 historical pilot/sweep episodes gives 736 completed combined observations across 28 configurations. The remaining catalog configurations are validated by scripted fixtures and have no model observations in this release.

Actor models are Qwen 3.8 27B and GLM 5.3 via OpenRouter, temperature .7, requested reasoning low, no model sampling seed, 16,384-token output cap and three attempts per decision. Fresh episodes use the original normal player prompt. Native action limits and rules remain unchanged; an external 128-total/64-focal-action cap yields censoring. Provider failures and native invalid actions have different provenance. Live completion is visible in the [viewer](http://localhost:42329/general/replicated); the [audited report](../study/REPORT.md) gives final realized counts and usage.

The four training anchors use lower/base values; higher values are held out, including corresponding historical high-value rows. All four new families are held out at every stage. Learning budgets are 120, 248 and 440 episodes. The primary outcome is native win/full solution; secondary targets describe supported executed actions with eligibility counts. Unsupported behavior remains null. These measurements do not infer intent, deception or exploitation. Native invalidity records engine handling, not psychological motivation.

All 2,112 final test predictions and fitted artifacts were frozen at 2026-09-11T00:29:27.934833+00:00, before the first test-player call at 2026-09-11T00:29:37.294870+00:00. The [protocol](../study/protocol.json), [freeze](../study/prediction/frozen.json), and per-stage manifests fix settings, source hashes, examples and predictions. Family-balanced evaluation averages repeated episode losses within conditions, then conditions within families. There are only four families per holdout. More training episodes add repetition/depth, not broader training-family coverage.

`mechanics.v2.json` is the corrected normalized forecaster specification. `mechanics.json` and the preflight manifests preserve earlier drafts; these do not define the scored final prompts. The full native code archive and scripted policy source remain authoritative. The correction did not alter actor prompts or collection behavior. Retained preflight inference is excluded from results and included in budget accounting.

Training features: use each exported row's `inputs` object. Native snapshots, targets, episode checkpoints, `*.evaluator.json`, raw calls and viewer evaluator states can contain hidden information or future outcomes. Exact player messages show what an actor received at a specific decision. Entire repeated conditions and opening groups must stay together in further data splits.

An additional 264 secondary forecasts pool training labels for identical visible demonstrations at 440 training episodes, retaining the exact original nested example IDs/order. This control was specified after test play began and uses training inputs/labels only. Its separate manifest under `study/prediction/supplemental-pooled-n440` records that later timing; it does not replace the original prospective comparisons.

Files: `catalog.json`, `instances.evaluator.json`, `fixtures.evaluator.json`, `label-definitions.json`, `mechanics.v2.json`, `native-source-hashes.json`, `native-source.tar.gz`, `collection-source.tar.gz`, and `TEXTARENA_LICENSE`. The [study directory](../study/) contains plans, raw provenance, forecasts, models, combined episode/action exports and audited analysis. Reproduction instructions and comparison limitations are in the [README](../README.md).
