# General TextArena coverage v1 · 2026-09-10

Purpose: learn and evaluate behavior prediction across a broad selection of ordinary text games, alongside the separately built Gameable Games dataset. Predictors may consume game rules/parameters, player identity, role/seat, prompt condition and actor-visible context. Targets include native validity, outcomes and supported behavioral decisions. Gameability is not a selection criterion, and native quirks are not curated away.

## Design and coverage

**12 families; 49 native parameter configurations; 196 seeded instances using four seeds; 113 distinct opening-state groups.** Each configuration is a base setting or a one-variable change from that base. The design is a small coverage sample rather than a full Cartesian product. Seeds are replications, not new game families or parameter variants. Deterministic games can share identical openings across seeds; these share an opening-group identifier.

| Family | Strategic structure | Native parameters varied | Players |
|---|---|---|---:|
| Connect Four | Spatial board strategy | Rows, columns | 2 |
| Nim | Combinatorial strategy | Pile sizes and count | 2 |
| Kuhn Poker | Hidden-card wagering | Number of rounds | 2 |
| Liar's Dice | Private information, bidding and challenge | Dice per player | 2 |
| Blind Auction | Private valuations and sealed bids | Capital, items, conversation rounds | 2 |
| Resource Negotiation | Bargaining with private inventories/values | Turn limit | 2 |
| Iterated Prisoner's Dilemma | Repeated cooperation and defection | Rounds, communication turns, temptation payoff | 2 |
| Colonel Blotto | Simultaneous resource allocation | Battlefields, units, rounds | 2 |
| Pig Dice | Risk-taking with chance | Winning score, turn limit | 2 |
| Tower of Hanoi | Single-player planning | Disks, turn limit | 1 |
| Mastermind | Information search | Code length, alphabet, duplicate policy, turn limit | 1 |
| Wordle | Language inference | Guess limit | 1 |

Exact settings, environment IDs, public descriptions, objectives and opponent policies are in [catalog.json](catalog.json). The implementation calls native raw registry environments, bypassing optional TextArena prompt/action wrappers. Native rules and actor-specific opening observations accompany every instance. Native reset/step/reward/invalid-action semantics are unchanged. The adapter records invalid-move events and isolates global random state while delegating transitions to TextArena.

This first selection does not cover more than two players, teams, LLM-versus-LLM play, long-form role-playing, real-time action, arbitrary natural-language rules, or the full TextArena catalog. The two-player baseline policies differ by family and are not claimed to be optimal or equally strong. Private-card, dice, valuation, and pending simultaneous-action information is restricted to the acting player. Single-player scripted solvers are used only for validation. The Wordle validation solver uses the engine's public candidate lexicon; live models receive only the native player observations and public constructor settings.

## Collection and sampling

The separate [live pilot](../../runs/pilot-20260910/export/REPORT.md) plans **96 episodes**: 12 base configurations × two model identities × two prompt conditions × two seed/seat blocks. Models are Qwen 3.8 27B and GLM 5.3, routed through OpenRouter. Shared settings with Gameable Games are temperature 0.7, low requested reasoning and a 16,384-token output cap. Native action syntax and the native game history replace Gameable Games' JSON action interface. Single-player prompts clarify the win objective. The model does not receive evaluator snapshots, opponent private observations, or environment seeds.

Two-player focal seats are 0 for seed 6100 and 1 for seed 6101; seed and seat are confounded in this pilot. Single-player trials use seat 0 for both seeds. Opponent randomness is separately deterministic by seed, actor and action index. Shared seeds align models and prompt conditions within each family but do not make different games strategically identical. Model sampling is unseeded. Native turn limits and stopping rules differ across families, unlike Gameable Games' fixed six focal actions.

The catalog includes all four seeds 6100–6103. Only 6100–6101 and the 12 base configurations are in the first LLM pilot. The 196 scripted fixtures and 1,761 replayed transitions are validation data, not empirical player behavior and not predictor training labels.

Final pilot coverage is **96/96 complete episodes and 477 focal actions**, including 18 native invalid submissions. All 803 native transitions passed replay. All 490 inference attempts were linked to saved checkpoints and reconciled with both ledgers: 477 successful responses, eight empty responses, and five truncated responses. The latter 13 responses were retried and are not game actions. Reported cost was $1.1363, with no unresolved billing reservations. Native completion includes ordinary endings and invalid-action penalties; it does not imply that the focal player won or solved the task.

An additional [full-catalog plan](../../runs/full-catalog-v1/plan.json) prepares 1,360 episodes: every native configuration × four seeds × all focal seats × two models × two prompts. It has **zero collected episodes** in this release. This larger design independently crosses seed and seat and is ready for the later parameter-generalization experiment.

## Inputs, targets and missingness

`episodes.jsonl` contains `inputs`, `labels`, status, provenance links, and split metadata. `inputs` includes public game representations, player/provider identity, seat, prompt context, and the focal player's native reset observations. `opening_messages` uses those reset observations even if a scripted opponent acts before the focal player's first turn. It does not include future moves. For next-action prediction, `actions.jsonl` adds the exact pre-action `messages`, a raw `target_action`, native validity and family-specific action targets.

Episode labels:

- Native invalid-action rate and native acceptance rate across all observed focal submissions. Acceptance is not equivalent to semantic rule adherence.
- Native terminal reward; strict two-player win, draw, or full single-player solution; win credit is 1 for a strict win, 0.5 for a two-player draw, 0 otherwise. Partial puzzle credit remains a native reward, not a solved task. Native reward values are not pooled across families.
- Cooperation/defection rates on Prisoner's Dilemma **decision-phase opportunities only**. The native parser treats any decision without `[Defect]` as cooperation; action rows separately record whether an explicit decision token was present.
- Pig risk-taking on valid decisions with a positive unbanked total: roll versus hold. Initial zero-risk rolls are excluded from that denominator.
- Action rows also preserve submitted tokens, negotiation offer/accept syntax, and submitted auction bid totals. These syntactic measurements do not assert that a trade executed or that bids won items.
- Unsupported cooperation, coordination, deception, exploration, exploitation and intention labels stay null with zero opportunity denominator. Ordinary games are not labeled "zero exploitation" merely because they were not selected for gameability.

Inference failures are separate from game behavior; responses with truncation, refusal, empty output or transport failure are not passed to the game. Native invalid submissions are preserved, including any native retry or terminal penalty. External action limits produce censored episodes with null terminal outcomes. Incomplete/censored episodes retain observed partial actions and rates; filter or report these explicitly. Completion conditioning can bias summaries.

## Splits and comparison protocol

[splits.json](splits.json) supplies three distinct grouping schemes: whole families, whole parameter configurations, and whole opening states. Each scheme assigns groups approximately 60/20/20 to train/validation/test by a fixed hash ordering. They are separate evaluation protocols, not three simultaneous requirements. Same-opening seed repetitions and all their model/prompt/seat trajectories share an opening split. Whole configurations and families also group all their repetitions. IDs, seeds, split labels and evaluator state are metadata, not model features.

The live pilot has only one configuration per family, so configuration and family transfer are not independently estimable. Some split categories may have little or no live support despite having catalog coverage. A larger collection should cross seed and seat and sample multiple native configurations per family. Fix splits before selecting demonstrations or fitting learned predictors.

Compare the two tracks with matched player representations, training counts, few-shot example budgets and evaluation targets. First evaluate held-out configurations/families within each track; then test transfer in both directions. Report family-level Brier/log loss or supported rate errors and macro averages. Next-action loss requires an explicit action representation because native action alphabets differ. Include missingness and uncertainty grouped by game/family. Do not interpret the small pilot's wins, invalid rates, or raw score differences as predictor difficulty or model rankings.

The companion `comparison-episodes.jsonl` aligns both pilots for descriptive analysis. Important remaining differences are family selection, number of actors, native horizons, opponent policies, action formats and reward semantics. Gameable Games also mixes 77 FLT and 67 OpenRouter episodes with nonrandom provider assignment. A comparison restricted to OpenRouter is useful but does not remove the other confounds. Predictor training and few-shot-versus-learned evaluation on these general games have not yet been performed.

## Reproducibility and known native quirks

The installed **TextArena 0.7.4** defines the benchmark; current upstream behavior may differ. [Official source](https://github.com/TextArena/TextArena). Installed Python code is hashed and archived with its license. Project collection code and inference helpers are fingerprinted in the manifest/plan. Wordle target vocabulary and all validity dictionaries are fingerprinted at reset. Replay checks include those fingerprints, native states, actor observations, raw actions and provider calls. Run with the pinned local environment; missing Wordle corpora may trigger the native library's NLTK download behavior.

Known semantics are retained: Prisoner's Dilemma defaults unrecognized decisions to cooperation; Tower of Hanoi can parse several bracketed moves from one response; some native turn limits are checked before incrementing the counter; Kuhn Poker initializes another hand even after setting the terminal outcome. Consequently, an API response, a submitted action, a native turn and an internal move are not universally the same unit. This release counts submitted responses as actions and preserves native transitions so these distinctions remain inspectable.

Two native payoff details also matter: this Kuhn Poker implementation changes the legal-action tree for bets/calls without adding their extra chips to the pot, and Blind Auction deducts all submitted valid bids from capital, including losing bids. The archived native implementation is the ground truth; family names should not be taken as proof of textbook payoff semantics. Thus this track is a coverage sample selected independently of gameability, not an audited exploit-free control set.

`instances.evaluator.json`, `fixtures.evaluator.json`, raw calls, and episode checkpoints may contain secrets or future labels. They are separated from prediction features by schema, not by access control. Keep them outside training feature pipelines. The dataset contains generated game text and model responses, not human participant records.
