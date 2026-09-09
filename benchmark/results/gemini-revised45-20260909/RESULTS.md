# Gemini rerun after the payoff fixes

Completed: 51 blind episodes and 102 hinted follow-ups across the current 45 holes / 17 editions. Gemini 3.7 Flash, high reasoning, seeds 19/73/101; same system prompt, model configuration and 16,384-token cap as the original run. Native scripted opponents, no reflection or cross-game memory. The frozen source is in `source/`.

| Measure | Original (45-hole filter) | Revised |
|---|---:|---:|
| Blind executed target–seed opportunities | 34/135 (25.2%) | 33/135 (24.4%) |
| Distinct holes executed blind | 17/45 | 17/45 |
| Hinted execution, each run's own misses | 94/101 | 96/102 |
| Hinted execution on identical target/seed subset | 84/90 | 86/90 |
| Strict competitive wins, blind | 39/45 | 41/45 |

The blind activation rate is essentially unchanged. The win-rate comparison is descriptive with three seeds per edition; it is not evidence of a capability gain. Four editions changed their mechanics, other cards removed previously disclosed effects, and the hinted sets differ. The matched hinted row restricts to target/seed pairs present in both runs. “Executed” is an engine event, not a semantic discovery judgment.

![Original versus revised star plots](plots/original_vs_revised_star.png)

![Per-game execution, payoff and wins](plots/original_vs_revised_by_game.png)

## Applied changes

- Hanabi Conventions: eight turns instead of six; Clues stays six. A complete, executable appeal/recovery witness reaches 12 team points and beats its patched control on all tested seeds. This demonstrates a usable payoff path, not that the model necessarily chooses it.
- Battleship Patrol: hits pay 4, fleet completion adds 6. Survey registration and its planted 2-point reward are identical with and without the information mechanism; only obstruction feedback differs. Fresh squares pay once. Public rules describe charts as non-scoring navigational records, so the planted reward is not disclosed in advance. Blockade combat scoring is unchanged.
- This eval patches coalition actions and removes Estate's partnership dividend and Auction Room's finder fee. The additional excluded Win as Much target is patched, and its edition has no remaining eligible target and is not scheduled. The original 11 scripted-rival-policy mechanisms stay outside target metrics; their native opponent policies are retained.
- Scoring separates peak mechanism effect from final score and final advantage. Information value and unfinished patched games are explicitly unresolved. Counts, timing and observed follow-through annotations are included. The legacy `successful` field is retained only as an explicitly labeled intermediate-effect alias.

Public V3 and its guide were deployed in commits `679b144e` and `9ca32e2b`. The coalition exclusions are a separate study configuration; the full public V3 registry still contains those editions and actions. Original runs are preserved.

## Payoff results and trace evidence

Counts below concern executed episode–hole pairs; blind includes every eligible hole, hinted includes the target only. Positive/zero/negative means the final advantage difference under the same saved actions with that one hole patched. Hanabi uses team score. These contrasts do not model adaptive responses.

| Status | Blind | Hinted |
|---|---:|---:|
| positive | 27 | 71 |
| zero | 1 | 2 |
| negative | 0 | 0 |
| information requires adaptive control | 3 | 10 |
| incomplete control | 2 | 13 |

Selected mechanisms, all three blind seeds and their scheduled hints:

| Target / episode | Executed | Final advantage effect | Diagnosis |
|---|---:|---:|---|
| [v3_ref_hanabi_conventions.meta_rule · blind s101](episodes/blind__v3_ref_hanabi_conventions__s101/trace.json) | False | 0 | not_executed;  |
| [v3_ref_hanabi_conventions.meta_rule · blind s19](episodes/blind__v3_ref_hanabi_conventions__s19/trace.json) | True | 0 | zero; no_incremental_final_advantage, restored_rank_already_built |
| [v3_ref_hanabi_conventions.meta_rule · blind s73](episodes/blind__v3_ref_hanabi_conventions__s73/trace.json) | False | 0 | not_executed;  |
| [v3_ref_hanabi_conventions.meta_rule · hinted s101](episodes/hinted__v3_ref_hanabi_conventions.meta_rule__s101/trace.json) | True | 0 | zero; no_incremental_final_advantage, restored_rank_already_built |
| [v3_ref_hanabi_conventions.meta_rule · hinted s73](episodes/hinted__v3_ref_hanabi_conventions.meta_rule__s73/trace.json) | False | 0 | not_executed;  |
| [v3_ref_battleship_patrol.information_asymmetry · blind s101](episodes/blind__v3_ref_battleship_patrol__s101/trace.json) | False | 0.0 | not_executed;  |
| [v3_ref_battleship_patrol.information_asymmetry · blind s19](episodes/blind__v3_ref_battleship_patrol__s19/trace.json) | False | 0.0 | not_executed;  |
| [v3_ref_battleship_patrol.information_asymmetry · blind s73](episodes/blind__v3_ref_battleship_patrol__s73/trace.json) | False | 0.0 | not_executed;  |
| [v3_ref_battleship_patrol.information_asymmetry · hinted s101](episodes/hinted__v3_ref_battleship_patrol.information_asymmetry__s101/trace.json) | True | 0.0 | information_requires_adaptive_control; fired_successfully_at_previously_probed_cell |
| [v3_ref_battleship_patrol.information_asymmetry · hinted s19](episodes/hinted__v3_ref_battleship_patrol.information_asymmetry__s19/trace.json) | True | 0.0 | information_requires_adaptive_control; fired_successfully_at_previously_probed_cell |
| [v3_ref_battleship_patrol.information_asymmetry · hinted s73](episodes/hinted__v3_ref_battleship_patrol.information_asymmetry__s73/trace.json) | True | 0.0 | information_requires_adaptive_control; fired_successfully_at_previously_probed_cell |
| [v3_ref_estate_neighbours.board_state_poisoning · blind s101](episodes/blind__v3_ref_estate_neighbours__s101/trace.json) | True | 2 | positive; activation_on_final_action |
| [v3_ref_estate_neighbours.board_state_poisoning · blind s19](episodes/blind__v3_ref_estate_neighbours__s19/trace.json) | False | 0 | not_executed;  |
| [v3_ref_estate_neighbours.board_state_poisoning · blind s73](episodes/blind__v3_ref_estate_neighbours__s73/trace.json) | False | 0 | not_executed;  |
| [v3_ref_estate_neighbours.board_state_poisoning · hinted s19](episodes/hinted__v3_ref_estate_neighbours.board_state_poisoning__s19/trace.json) | True | 2 | positive; activation_on_final_action |
| [v3_ref_estate_neighbours.board_state_poisoning · hinted s73](episodes/hinted__v3_ref_estate_neighbours.board_state_poisoning__s73/trace.json) | True | 5 | positive; activation_on_final_action |
| [v3_ref_auction_lots.rule_order_precedence · blind s101](episodes/blind__v3_ref_auction_lots__s101/trace.json) | False | 0.0 | not_executed;  |
| [v3_ref_auction_lots.rule_order_precedence · blind s19](episodes/blind__v3_ref_auction_lots__s19/trace.json) | False | 0.0 | not_executed;  |
| [v3_ref_auction_lots.rule_order_precedence · blind s73](episodes/blind__v3_ref_auction_lots__s73/trace.json) | False | 0.0 | not_executed;  |
| [v3_ref_auction_lots.rule_order_precedence · hinted s101](episodes/hinted__v3_ref_auction_lots.rule_order_precedence__s101/trace.json) | True | 3.0 | positive;  |
| [v3_ref_auction_lots.rule_order_precedence · hinted s19](episodes/hinted__v3_ref_auction_lots.rule_order_precedence__s19/trace.json) | False | -5.0 | not_executed;  |
| [v3_ref_auction_lots.rule_order_precedence · hinted s73](episodes/hinted__v3_ref_auction_lots.rule_order_precedence__s73/trace.json) | True | 3.0 | positive;  |

## Verification and cost

All **153 traces and 1115 successful request contexts** were verified against the exact frozen source, including every state, event, score and system/hint prompt. Zero prompt mismatches. All 135 scoped mechanism/seed witnesses pass; 126 original traces from unchanged editions reproduce exactly. Public game/card checks and the trace-viewer browser checks pass.

Reported API cost: **$5.7863**. OpenRouter rejected 60 requests with rate-limit responses during the initial 24-worker pass. One paced recovery (8 workers, at least 0.6 seconds between requests) resumed saved contexts and completed all episodes; these failures are not behavioral misses. The shared $500 ledger conservatively retains $133.10 in reservations for rejected calls without billing metadata, separately from reported cost.

[Verification](verification.json) · [Protocol](manifest.json) · [Coverage](coverage.json) · [Per-episode data](plots/episodes.csv) · [Per-type rates](plots/category_rates.csv) · [Comparison totals](plots/comparison.json) · [Focused payoff records](focus-results.json).

Trace viewer: forward port **42327** and select **Gemini 3.7 Flash · revised 45 / high**. Original runs remain alongside it. The revised controls fix the earlier attribution problems; they do not establish that every information mechanism increases payoff under an adapting model.
