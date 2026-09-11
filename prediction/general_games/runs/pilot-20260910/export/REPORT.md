# General TextArena coverage · first dataset and pilot

The catalog contains **12 families, 49 native parameter configurations, and 196 seeded instances** (113 distinct opening-state groups). Seeds are repetitions, not additional game designs.

Live collection: **96/96 complete episodes**, 477 focal actions, 18 native invalid actions. Status counts: `{'complete': 96}`. Scripted fixtures are excluded.

| Family | Complete / planned | Focal actions | Native invalid | Strict wins / full solutions | Draws |
|---|---:|---:|---:|---:|---:|
| Connect Four | 8 / 8 | 58 | 2 | 4 | 1 |
| Nim | 8 / 8 | 32 | 1 | 2 | 0 |
| Kuhn Poker | 8 / 8 | 24 | 0 | 6 | 0 |
| Liar's Dice | 8 / 8 | 26 | 1 | 3 | 0 |
| Blind Auction | 8 / 8 | 18 | 4 | 4 | 0 |
| Resource Negotiation | 8 / 8 | 28 | 0 | 0 | 5 |
| Iterated Prisoner's Dilemma | 8 / 8 | 48 | 0 | 8 | 0 |
| Colonel Blotto | 8 / 8 | 22 | 0 | 1 | 1 |
| Pig Dice | 8 / 8 | 72 | 0 | 5 | 0 |
| Tower of Hanoi | 8 / 8 | 78 | 6 | 6 | 0 |
| Mastermind | 8 / 8 | 30 | 2 | 8 | 0 |
| Wordle | 8 / 8 | 41 | 2 | 6 | 0 |

| Model / prompt | Complete | Native invalid / focal actions | Two-player wins / episodes | Draws | Single-player solutions / episodes |
|---|---:|---:|---:|---:|---:|
| qwen-3.8-27b / normal | 24 | 3 / 113 | 11 / 18 | 2 | 5 / 6 |
| qwen-3.8-27b / active_exploration | 24 | 3 / 106 | 7 / 18 | 3 | 5 / 6 |
| glm / normal | 24 | 9 / 132 | 8 / 18 | 0 | 4 / 6 |
| glm / active_exploration | 24 | 3 / 126 | 7 / 18 | 2 | 6 / 6 |

These small descriptive counts are conditional on each family's particular scripted opponent and seed/seat blocks. They do not establish a model ranking or an exploration benefit.

Nine families are two-player games against an information-restricted scripted opponent; three are single-player tasks. Provider is uniformly OpenRouter, temperature 0.7, requested reasoning low, maximum output 16,384 tokens. Native horizons vary.

Each family uses one base configuration, two seed/seat blocks, two models, and normal/exploration prompts. Seats alternate across the two blocks in two-player games: seed and seat are not independently crossed.

**This collection measures coverage and observable behavior. It does not establish whether general games are harder to predict, or whether few-shot prompting beats a learned predictor.** The catalog has 49 validated configurations; this plan selects 12, with 12 represented by complete model episodes. No predictor evaluation is performed by this export.

Comparison with the current Gameable Games pilot:

| Property | General TextArena | Gameable Games |
|---|---|---|
| Selection | Purposive breadth across ordinary game structures | Behavioral mechanisms and gameability controls |
| Catalog | 12 families; 49 parameter configurations; 196 seed instances | 24 families; 3,256 base variants + 2,800 controls |
| Live collection | 96 planned episodes; 12 families | 144 complete episodes; 10 families |
| Actors | One focal model + one bot, or one solver | One focal model + two scripted rivals |
| Horizon | Native termination, externally bounded | Six focal actions |
| Shared protocol | Qwen / GLM, normal / exploration, 0.7, low reasoning, 16,384 cap | Same |
| Provider | OpenRouter | 77 FLT + 67 OpenRouter episodes |
| Labels | Native validity, outcomes, family-specific behavior | Validity, outcomes, mechanism-specific behavior |

`comparison-episodes.jsonl` aligns model, provider, prompt, seat, player count, invalid-action rate and win credit across both exports. These are descriptive measurements, not difficulty-adjusted scores. Win credit, action opportunity counts, opponents, horizons and family composition differ. Report family-level results and macro averages, and examine the OpenRouter subset separately; the Gameable provider assignment was not random. Do not compare pooled raw scores or convert unsupported social/exploitation labels to zero.

For a predictor comparison, collect multiple parameter configurations and independent seed × seat trials in both tracks; use identical player inputs and matched training/example budgets. Evaluate within each track on held-out configurations and whole families, then train on one track and test on the other. Compare Brier/log loss for shared binary targets and supported behavioral rates, plus family-normalized next-action loss with explicit legal-action representations. Report completion/missingness and family-level uncertainty. The supplied grouped splits prevent repeated trajectories leaking across sets; the current base-only pilot cannot identify parameter generalization.

Validation: 196 scripted fixture replays; 1761 fixture transitions; 803 live transitions replayed; 477 focal actions linked to exact raw successful provider calls. Future outcomes and global/other-player hidden states are stored only outside `inputs` and outside pre-action `messages`. Native engine acceptance is not a claim of honesty or rule adherence.

Observed inference usage (includes retries, including any incomplete episodes):

```json
{
  "requests": 490,
  "status:ok": 477,
  "reported_cost_usd": 1.1362969669999998,
  "prompt_tokens": 310614,
  "completion_tokens": 347498,
  "total_tokens": 658112,
  "status:invalid_response": 8,
  "status:truncated": 5
}
```

See the [dataset card](../../../data/20260910-v1/DATASET_CARD.md) and [collection instructions](../../../README.md) for sampling, labels, native engine quirks, provenance, and commands. Engine source: [TextArena](https://github.com/TextArena/TextArena), installed version 0.7.4; the installed code is fingerprinted rather than upgraded.
