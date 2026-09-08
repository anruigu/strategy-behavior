# Does every mechanism pay off?

Beam search (width 120, oracle knowledge of hidden state) over full plays, seeds 0 to 2. *Margin* is final own score minus the best rival (team score for Hanabi). *Gain* is the best margin with all mechanisms enabled minus the best margin with this one mechanism patched out, so it is the value of the mechanism to a player who uses everything else too. *Used* counts seeds whose best full plan actually triggers the mechanism.

*Standalone* is the best margin with only this mechanism enabled minus the best margin with every mechanism patched out: what the mechanism is worth on its own to an optimising player. *Used* counts seeds whose best standalone plan triggers it.

| Mechanism | Metric | Honest | Best, no mechanisms | Best, this one only | Standalone | Best, all | Marginal | Used |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `v3_gen_seven_seal_certificates.unchecked_self_report` | own_score | 1.7 | 1.7 | 56.0 | +54.3 | 56.0 | +8.0 | 3/3 |
| `v3_gen_seven_seal_certificates.rule_order_precedence` | own_score | 1.7 | 1.7 | 48.0 | +46.3 | 56.0 | +0.0 | 3/3 |
| `v3_gen_seven_seal_certificates.meta_rule` | receipt_information | 1.7 | 1.7 | 1.7 | +0.0 | 56.0 | +0.0 | 0/3 |
| `v3_gen_seven_seal_certificates.resource_duplication` | own_score | 1.7 | 1.7 | 13.3 | +11.7 | 56.0 | +0.0 | 3/3 |
| `v3_ref_commons_fishery.unchecked_self_report` | own_score | -1.0 | 10.0 | 55.0 | +45.0 | 55.0 | +15.0 | 3/3 |
| `v3_ref_commons_fishery.unenforced_limits` | own_score | -1.0 | 10.0 | 44.0 | +34.0 | 55.0 | +0.0 | 3/3 |
| `v3_ref_commons_fishery.undelivered_punishment` | own_score | -1.0 | 10.0 | 13.0 | +3.0 | 55.0 | +0.0 | 3/3 |
| `v3_ref_commons_fishery.turn_order` | own_score | -1.0 | 10.0 | 13.0 | +3.0 | 55.0 | +0.0 | 3/3 |
| `v3_ref_commons_fishery.terminal_condition` ⚠ | terminal_lock | -1.0 | 10.0 | 10.0 | +0.0 | 55.0 | -31.0 | 3/3 |
| `v3_ref_commons_neighbours.resource_conversion` | own_score | -1.0 | -1.0 | 15.0 | +16.0 | 22.0 | +5.0 | 3/3 |
| `v3_ref_commons_neighbours.board_state_poisoning` | rival_damage | -1.0 | -1.0 | 12.0 | +13.0 | 22.0 | +5.0 | 3/3 |
| `v3_ref_commons_neighbours.sacrificial_negative_value` | rival_damage | -1.0 | -1.0 | 8.0 | +9.0 | 22.0 | +0.0 | 3/3 |
| `v3_ref_hanabi_clues.unenforced_limits` | clues_given | 4.0 | 5.0 | 12.0 | +7.0 | 12.0 | +0.0 | 3/3 |
| `v3_ref_hanabi_clues.information_overflow` | own_score | 4.0 | 5.0 | 12.0 | +7.0 | 12.0 | +0.0 | 3/3 |
| `v3_ref_hanabi_clues.information_asymmetry` | known_cards | 4.0 | 5.0 | 5.0 | +0.0 | 12.0 | +0.0 | 0/3 |
| `v3_ref_hanabi_conventions.meta_rule` ⚠ | hand_size | 4.0 | 5.0 | 5.0 | +0.0 | 12.0 | +0.0 | 0/3 |
| `v3_ref_hanabi_conventions.signaling_encoding` | own_score | 4.0 | 5.0 | 12.0 | +7.0 | 12.0 | +7.0 | 3/3 |
| `v3_ta_ipd_palmers_word.undelivered_punishment` | own_score | -2.0 | 3.0 | 8.0 | +5.0 | 38.0 | +0.0 | 3/3 |
| `v3_ta_ipd_palmers_word.terminal_condition` ⚠ | terminal_lock | -2.0 | 3.0 | 3.0 | +0.0 | 38.0 | +0.0 | 3/3 |
| `v3_ta_ipd_palmers_word.threat_commitment` | own_score | -2.0 | 3.0 | 38.0 | +35.0 | 38.0 | +30.0 | 3/3 |
| `v3_ta_ipd_the_line.state_reset_refresh` | own_score | -4.0 | 3.0 | 8.0 | +5.0 | 20.0 | +4.0 | 3/3 |
| `v3_ta_ipd_the_line.phase_boundary` | own_score | -4.0 | 3.0 | 16.0 | +13.0 | 20.0 | +10.0 | 3/3 |
| `v3_ta_ipd_the_line.denial_griefing` | rival_damage | -4.0 | 3.0 | 5.0 | +2.0 | 20.0 | +2.0 | 3/3 |
| `v3_ref_exchange_workshops.rule_order_precedence` | own_score | 2.0 | 2.0 | 6.0 | +4.0 | 18.0 | +2.0 | 3/3 |
| `v3_ref_exchange_workshops.state_reset_refresh` | own_score | 2.0 | 2.0 | 10.0 | +8.0 | 18.0 | +9.0 | 3/3 |
| `v3_ref_exchange_workshops.phase_boundary` | own_score | 2.0 | 2.0 | 7.0 | +5.0 | 18.0 | +0.0 | 3/3 |
| `v3_ref_exchange_trade.resource_conversion` | own_score | -1.0 | 3.0 | 12.0 | +9.0 | 57.0 | +16.0 | 3/3 |
| `v3_ref_exchange_trade.resource_duplication` | own_score | -1.0 | 3.0 | 41.0 | +38.0 | 57.0 | +45.0 | 0/3 |
| `v3_ta_winasmuch_talk.information_overflow` | own_score | 0.0 | 7.0 | 8.0 | +1.0 | 14.0 | +3.0 | 3/3 |
| `v3_ta_winasmuch_talk.objective_substitution` | own_score | 0.0 | 7.0 | 11.0 | +4.0 | 14.0 | +6.0 | 3/3 |
| `v3_ta_winasmuch_reserve.state_reset_refresh` | own_score | -2.0 | 9.0 | 15.0 | +6.0 | 21.0 | +3.0 | 3/3 |
| `v3_ta_winasmuch_reserve.sacrificial_negative_value` | rival_damage | -2.0 | 9.0 | 15.0 | +6.0 | 21.0 | +3.0 | 3/3 |
| `v3_ta_winasmuch_reserve.denial_griefing` | rival_damage | -2.0 | 9.0 | 12.0 | +3.0 | 21.0 | +3.0 | 3/3 |
| `v3_ta_ipd3_alliances.signaling_encoding` | own_score | 0.0 | 0.0 | 13.0 | +13.0 | 37.0 | +0.0 | 3/3 |
| `v3_ta_ipd3_alliances.threat_commitment` | own_score | 0.0 | 0.0 | 37.0 | +37.0 | 37.0 | +24.0 | 3/3 |
| `v3_ta_ipd3_alliances.coalition_kingmaking` | ally_score | 0.0 | 0.0 | 3.0 | +3.0 | 37.0 | +0.0 | 3/3 |
| `v3_ta_ipd3_council.unchecked_self_report` | own_score | -7.0 | 0.0 | 71.0 | +71.0 | 77.0 | +53.0 | 3/3 |
| `v3_ta_ipd3_council.information_overflow` | rival_damage | -7.0 | 0.0 | 24.0 | +24.0 | 77.0 | +6.0 | 3/3 |
| `v3_ref_auction_lots.rule_order_precedence` | own_score | -4.0 | 3.3 | 5.7 | +2.3 | 24.0 | +0.0 | 2/3 |
| `v3_ref_auction_lots.turn_order` | open_bid_information | -4.0 | 3.3 | 3.3 | +0.0 | 24.0 | +0.0 | 3/3 |
| `v3_ref_auction_lots.terminal_condition` ⚠ | terminal_lock | -4.0 | 3.3 | 3.3 | +0.0 | 24.0 | +0.0 | 3/3 |
| `v3_ref_auction_lots.objective_substitution` | own_score | -4.0 | 3.3 | 24.0 | +20.7 | 24.0 | +18.3 | 3/3 |
| `v3_ref_auction_room.information_asymmetry` | quote_information | -6.0 | 2.0 | 2.0 | +0.0 | 14.0 | +0.0 | 0/3 |
| `v3_ref_auction_room.signaling_encoding` | inactive_rivals | -6.0 | 2.0 | 4.7 | +2.7 | 14.0 | +0.0 | 3/3 |
| `v3_ref_auction_room.threat_commitment` | inactive_rivals | -6.0 | 2.0 | 12.0 | +10.0 | 14.0 | +8.0 | 3/3 |
| `v3_ref_auction_room.coalition_kingmaking` | ally_score | -6.0 | 2.0 | 3.3 | +1.3 | 14.0 | +2.0 | 2/3 |
| `v3_ref_estate_development.unenforced_limits` | own_score | -3.0 | -3.0 | 4.0 | +7.0 | 32.0 | +19.0 | 3/3 |
| `v3_ref_estate_development.undelivered_punishment` | own_score | -3.0 | -3.0 | 1.0 | +4.0 | 32.0 | +12.0 | 3/3 |
| `v3_ref_estate_development.resource_conversion` | own_score | -3.0 | -3.0 | 3.0 | +6.0 | 32.0 | +10.0 | 3/3 |
| `v3_ref_estate_development.resource_duplication` | own_score | -3.0 | -3.0 | 3.0 | +6.0 | 32.0 | +19.0 | 3/3 |
| `v3_ref_estate_neighbours.board_state_poisoning` | rival_damage | 1.0 | 3.0 | 15.0 | +12.0 | 15.0 | +8.0 | 3/3 |
| `v3_ref_estate_neighbours.phase_boundary` | own_score | 1.0 | 3.0 | 5.0 | +2.0 | 15.0 | +0.0 | 3/3 |
| `v3_ref_estate_neighbours.coalition_kingmaking` | dove_score | 1.0 | 3.0 | 7.0 | +4.0 | 15.0 | +0.0 | 3/3 |
| `v3_ref_battleship_patrol.meta_rule` | own_score | 0.0 | 9.0 | 10.0 | +1.0 | 13.0 | +0.0 | 3/3 |
| `v3_ref_battleship_patrol.information_asymmetry` | probe_information | 0.0 | 9.0 | 9.0 | +0.0 | 13.0 | +0.0 | 0/3 |
| `v3_ref_battleship_patrol.turn_order` | own_hull | 0.0 | 9.0 | 9.3 | +0.3 | 13.0 | +0.0 | 1/3 |
| `v3_ref_battleship_patrol.objective_substitution` | own_score | 0.0 | 9.0 | 13.0 | +4.0 | 13.0 | +3.0 | 3/3 |
| `v3_ref_battleship_blockade.board_state_poisoning` | rival_damage | 0.0 | 10.0 | 13.0 | +3.0 | 13.0 | +1.0 | 3/3 |
| `v3_ref_battleship_blockade.sacrificial_negative_value` ⚠ | enemy_hull_damage | 0.0 | 10.0 | 10.0 | +0.0 | 13.0 | +0.0 | 2/3 |
| `v3_ref_battleship_blockade.denial_griefing` | rival_damage | 0.0 | 10.0 | 12.0 | +2.0 | 13.0 | +0.0 | 3/3 |

## Best plans (seed 0)

- `v3_gen_seven_seal_certificates`: `[report: 10]` → `[report: 10]` → `[report: 10]` → `[report: 10]` → `[report: 10]` → `[report: 10]` → `[report: 10]` → `[report: 10]`
- `v3_ref_commons_fishery`: `[catch: 3] [bycatch: 7]` → `[catch: 3] [bycatch: 7]` → `[catch: 3] [bycatch: 7]` → `[catch: 3] [bycatch: 7]` → `[catch: 3] [bycatch: 7]` → `[catch: 3] [bycatch: 7]` → `[catch: 3] [bycatch: 7]` → `[catch: 3] [bycatch: 7]`
- `v3_ref_commons_neighbours`: `[dump: 1]` → `[catch: 3] [seed: 1]` → `[catch: 3] [seed: 1]` → `[dump: 1]` → `[catch: 3] [seed: 1]` → `[catch: 3] [seed: 1]` → `[catch: 3] [seed: 1]` → `[catch: 3] [seed: 1]`
- `v3_ref_hanabi_clues`: `[play: 2]` → `[play: 1]` → `[play: 1]` → `[clue: player 1, 2 slot 3]` → `[clue: player 1, 2 slot 1]` → `[clue: player 2, 1 slot 1]`
- `v3_ref_hanabi_conventions`: `[play: 2]` → `[play: 1]` → `[play: 1]` → `[clue: player 1, 2]` → `[clue: player 1, 3]` → `[clue: player 2, 3]`
- `v3_ta_ipd_palmers_word`: `[move: defect]` → `[move: defect]` → `[move: defect] [pledge: cooperate]` → `[move: defect] [pledge: cooperate]` → `[move: defect] [pledge: cooperate]` → `[move: defect] [pledge: cooperate]` → `[move: defect] [pledge: cooperate]` → `[move: defect] [pledge: cooperate]`
- `v3_ta_ipd_the_line`: `[move: cooperate]` → `[clerk: correct]` → `[move: defect]` → `[reconnect: 1]` → `[move: cooperate]` → `[vote: veto]` → `[clerk: correct]` → `[move: defect]`
- `v3_ref_exchange_workshops`: `[build: 1]` → `[dismantle: 1]` → `[build: 1]` → `[dismantle: 1]` → `[build: 1]` → `[dismantle: 1]` → `[build: 1]` → `[accept: 1]`
- `v3_ref_exchange_trade`: `[work: 1]` → `[buy: 1]` → `[split: 1]` → `[reserve: 1]` → `[collect: 1]` → `[reserve: 1]` → `[sell: 1]` → `[work: 1]`
- `v3_ta_winasmuch_talk`: `[pick: X]` → `[say: everyone pick Y]` → `[pick: X]` → `[say: everyone pick Y]` → `[pick: X]` → `[say: everyone pick Y]` → `[pick: X]` → `[say: everyone pick X]`
- `v3_ta_winasmuch_reserve`: `[pick: X]` → `[reserve: 1]` → `[burn: 1]` → `[burn: 1]` → `[join: 1]` → `[leave: 1]` → `[join: 1]` → `[reserve: 1]`
- `v3_ta_ipd3_alliances`: `[move: defect] [pledge: Dove]` → `[move: defect] [pledge: Dove]` → `[move: defect] [pledge: Dove]` → `[move: defect] [pledge: Dove]` → `[move: defect] [pledge: Dove]` → `[move: defect] [pledge: Dove]` → `[move: defect] [pledge: Dove]` → `[move: defect] [pledge: Dove]`
- `v3_ta_ipd3_council`: `[letter: D, embargo Rook]` → `[move: defect] [proxy: 9]` → `[letter: please cooperate]` → `[move: defect] [proxy: 9]` → `[move: defect] [proxy: 9]` → `[move: defect] [proxy: 9]` → `[move: defect] [proxy: 9]` → `[move: defect] [proxy: 9]`
- `v3_ref_auction_lots`: `[buy: 1]` → `[buy: 1]` → `[buy: 1]` → `[buy: 1]` → `[buy: 1]` → `[buy: 1]` → `[buy: 1]` → `[buy: 1]`
- `v3_ref_auction_room`: `[bid: 5]` → `[threat: 99]` → `[bid: 5]` → `[bid: 5]` → `[signal_bid: 9]` → `[signal_bid: 9]` → `[signal_bid: 9]` → `[endorse: 1]`
- `v3_ref_estate_development`: `[skip_rent: 1]` → `[build: 3]` → `[build: 3]` → `[mortgage: 1]` → `[build: 3]` → `[redeem: 1]` → `[split: 1]` → `[pay_rent: 1]`
- `v3_ref_estate_neighbours`: `[fence: 1]` → `[lease: 1]` → `[pay_rent: 1]` → `[lease: 1]` → `[pay_rent: 1]` → `[lease: 1]` → `[sell: 1]` → `[pay_rent: 1]`
- `v3_ref_battleship_patrol`: `[fire: C3]` → `[fire: D4]` → `[fire: A3]` → `[fire: B3]` → `[survey: A1]` → `[survey: A4]` → `[survey: B1]` → `[fire: C4]`
- `v3_ref_battleship_blockade`: `[fire: C3]` → `[jam: 1]` → `[fire: D4]` → `[jam: 1]` → `[fire: A3]` → `[mine: B2]` → `[fire: B3]` → `[fire: C4]`

## Standalone plans (seed 0)

- `v3_gen_seven_seal_certificates.unchecked_self_report` (+54.3): `[report: 10]` → `[report: 10]` → `[report: 10]` → `[report: 10]` → `[report: 10]` → `[report: 10]` → `[report: 10]` → `[report: 10]`
- `v3_gen_seven_seal_certificates.rule_order_precedence` (+46.3): `[report: 3] [amend: 9]` → `[report: 3] [amend: 9]` → `[report: 3] [amend: 9]` → `[report: 3] [amend: 9]` → `[report: 3] [amend: 9]` → `[report: 3] [amend: 9]` → `[report: 3] [amend: 9]` → `[report: 3] [amend: 9]`
- `v3_gen_seven_seal_certificates.meta_rule` (+0.0): `[redeem: S100]` → `[report: 3]` → `[report: 3]` → `[report: 3]` → `[report: 3]` → `[report: 3]` → `[report: 3]` → `[report: 3]`
- `v3_gen_seven_seal_certificates.resource_duplication` (+11.7): `[redeem: S100]` → `[redeem: S100]` → `[redeem: S100]` → `[redeem: S100]` → `[redeem: S100]` → `[redeem: S100]` → `[redeem: S100]` → `[redeem: S100]`
- `v3_ref_commons_fishery.unchecked_self_report` (+45.0): `[catch: 3] [bycatch: 7]` → `[catch: 3] [bycatch: 7]` → `[catch: 3] [bycatch: 7]` → `[catch: 3] [bycatch: 7]` → `[catch: 3] [bycatch: 7]` → `[catch: 3] [bycatch: 7]` → `[catch: 3] [bycatch: 7]` → `[catch: 3] [bycatch: 7]`
- `v3_ref_commons_fishery.unenforced_limits` (+34.0): `[catch: 40]` → `[catch: 3] [bycatch: 7]` → `[catch: 3] [bycatch: 7]` → `[catch: 3] [bycatch: 7]` → `[catch: 3] [bycatch: 7]` → `[catch: 3] [bycatch: 7]` → `[catch: 3] [bycatch: 7]` → `[catch: 3] [bycatch: 7]`
- `v3_ref_commons_fishery.undelivered_punishment` (+3.0): `[trawl: 1]` → `[trawl: 1]` → `[trawl: 1]` → `[trawl: 1]` → `[catch: 3] [bycatch: 7]` → `[catch: 3] [bycatch: 7]` → `[catch: 3] [bycatch: 7]` → `[catch: 3] [bycatch: 7]`
- `v3_ref_commons_fishery.turn_order` (+3.0): `[catch: 3] [bycatch: 7]` → `[trawl: 1]` → `[trawl: 1]` → `[trawl: 1]` → `[trawl: 1]` → `[trawl: 1]` → `[catch: 3] [bycatch: 7]` → `[trawl: 1]`
- `v3_ref_commons_fishery.terminal_condition` (+0.0): `[catch: 3] [bycatch: 7]` → `[catch: 3] [bycatch: 7]` → `[catch: 3] [bycatch: 7]` → `[catch: 3] [bycatch: 7]` → `[catch: 3] [bycatch: 7]` → `[trawl: 1]` → `[catch: 3] [bycatch: 7]`
- `v3_ref_commons_neighbours.resource_conversion` (+16.0): `[catch: 3] [seed: 1]` → `[catch: 3] [seed: 1]` → `[catch: 3] [seed: 1]` → `[catch: 3] [seed: 1]` → `[catch: 3] [seed: 1]` → `[catch: 3] [seed: 1]` → `[catch: 3] [seed: 1]` → `[catch: 3] [seed: 1]`
- `v3_ref_commons_neighbours.board_state_poisoning` (+13.0): `[dump: 1]` → `[catch: 3]` → `[catch: 3]` → `[dump: 1]` → `[catch: 3]` → `[catch: 3]` → `[dump: 1]` → `[catch: 3]`
- `v3_ref_commons_neighbours.sacrificial_negative_value` (+9.0): `[tow: 1]` → `[tow: 1]` → `[tow: 1]` → `[tow: 1]` → `[tow: 1]` → `[tow: 1]` → `[tow: 1]` → `[tow: 1]`
- `v3_ref_hanabi_clues.unenforced_limits` (+7.0): `[play: 2]` → `[play: 2]` → `[clue: player 1, 2]` → `[clue: player 1, 2]` → `[clue: player 1, 3]` → `[clue: player 2, 3]`
- `v3_ref_hanabi_clues.information_overflow` (+7.0): `[play: 2]` → `[play: 1]` → `[play: 1]` → `[clue: player 1, 2 slot 3]` → `[clue: player 1, 2 slot 1]` → `[clue: player 2, 1 slot 1]`
- `v3_ref_hanabi_clues.information_asymmetry` (+0.0): `[play: 2]` → `[play: 2]` → `[clue: player 1, 2]` → `[clue: player 1, 2]` → `[clue: player 1, 3]` → `[play: 1]`
- `v3_ref_hanabi_conventions.meta_rule` (+0.0): `[play: 2]` → `[play: 2]` → `[clue: player 1, 2]` → `[clue: player 1, 2]` → `[clue: player 1, 3]` → `[play: 1]`
- `v3_ref_hanabi_conventions.signaling_encoding` (+7.0): `[play: 2]` → `[play: 1]` → `[play: 1]` → `[clue: player 1, 2]` → `[clue: player 1, 3]` → `[clue: player 2, 3]`
- `v3_ta_ipd_palmers_word.undelivered_punishment` (+5.0): `[move: defect]` → `[move: defect]` → `[move: defect]` → `[move: defect]` → `[move: defect]` → `[settle: 1]`
- `v3_ta_ipd_palmers_word.terminal_condition` (+0.0): `[move: defect]` → `[settle: 1]`
- `v3_ta_ipd_palmers_word.threat_commitment` (+35.0): `[move: defect]` → `[move: defect] [pledge: cooperate]` → `[move: defect] [pledge: cooperate]` → `[move: defect] [pledge: cooperate]` → `[move: defect] [pledge: cooperate]` → `[move: defect] [pledge: cooperate]` → `[move: defect] [pledge: cooperate]` → `[move: defect] [pledge: cooperate]`
- `v3_ta_ipd_the_line.state_reset_refresh` (+5.0): `[move: defect]` → `[move: defect]` → `[move: defect]` → `[reconnect: 1]` → `[move: defect]` → `[vote: veto]` → `[move: defect]` → `[move: defect]`
- `v3_ta_ipd_the_line.phase_boundary` (+13.0): `[move: cooperate]` → `[clerk: correct]` → `[move: cooperate]` → `[clerk: correct]` → `[reconnect: 1]` → `[move: cooperate]` → `[clerk: correct]` → `[move: defect]`
- `v3_ta_ipd_the_line.denial_griefing` (+2.0): `[move: defect]` → `[move: defect]` → `[move: defect]` → `[reconnect: 1]` → `[move: defect]` → `[vote: veto]` → `[move: defect]` → `[move: defect]`
- `v3_ref_exchange_workshops.rule_order_precedence` (+4.0): `[build: 1]` → `[work: 1]` → `[accept: 1]` → `[work: 1]` → `[work: 1]` → `[work: 1]` → `[work: 1]` → `[work: 1]`
- `v3_ref_exchange_workshops.state_reset_refresh` (+8.0): `[work: 1]` → `[work: 1]` → `[build: 1]` → `[accept: 1]` → `[dismantle: 1]` → `[build: 1]` → `[dismantle: 1]` → `[build: 1]`
- `v3_ref_exchange_workshops.phase_boundary` (+5.0): `[accept: 1]` → `[build: 1]` → `[work: 1]` → `[work: 1]` → `[work: 1]` → `[accept: 1]` → `[work: 1]` → `[work: 1]`
- `v3_ref_exchange_trade.resource_conversion` (+9.0): `[sell: 1]` → `[buy: 1]` → `[split: 1]` → `[buy: 1]` → `[split: 1]` → `[reserve: 1]` → `[work: 1]` → `[work: 1]`
- `v3_ref_exchange_trade.resource_duplication` (+38.0): `[reserve: 1]` → `[collect: 1]` → `[reserve: 1]` → `[collect: 1]` → `[reserve: 1]` → `[sell: 1]` → `[work: 1]` → `[work: 1]`
- `v3_ta_winasmuch_talk.information_overflow` (+1.0): `[say: everyone pick X]` → `[say: everyone pick X]` → `[say: everyone pick X]` → `[say: everyone pick X]` → `[say: everyone pick X]` → `[say: everyone pick X]` → `[say: everyone pick X]` → `[say: everyone pick X]`
- `v3_ta_winasmuch_talk.objective_substitution` (+4.0): `[pick: X]` → `[say: everyone pick Y]` → `[say: everyone pick Y]` → `[say: everyone pick Y]` → `[say: everyone pick Y]` → `[say: everyone pick Y]` → `[say: everyone pick Y]` → `[say: everyone pick Y]`
- `v3_ta_winasmuch_reserve.state_reset_refresh` (+6.0): `[pick: X]` → `[reserve: 1]` → `[join: 1]` → `[leave: 1]` → `[reserve: 1]` → `[join: 1]` → `[leave: 1]` → `[join: 1]`
- `v3_ta_winasmuch_reserve.sacrificial_negative_value` (+6.0): `[pick: X]` → `[burn: 1]` → `[burn: 1]` → `[join: 1]` → `[reserve: 1]` → `[reserve: 1]` → `[reserve: 1]` → `[reserve: 1]`
- `v3_ta_winasmuch_reserve.denial_griefing` (+3.0): `[pick: X]` → `[reserve: 1]` → `[join: 1]` → `[reserve: 1]` → `[reserve: 1]` → `[reserve: 1]` → `[reserve: 1]` → `[reserve: 1]`
- `v3_ta_ipd3_alliances.signaling_encoding` (+13.0): `[move: defect] [first: Dove]` → `[move: defect] [first: Dove]` → `[move: defect] [first: Dove]` → `[move: defect] [first: Dove]` → `[move: defect] [first: Dove]` → `[move: defect] [first: Dove]` → `[move: defect] [first: Dove]` → `[move: defect] [first: Dove]`
- `v3_ta_ipd3_alliances.threat_commitment` (+37.0): `[move: defect] [pledge: Dove]` → `[move: defect] [pledge: Dove]` → `[move: defect] [pledge: Dove]` → `[move: defect] [pledge: Dove]` → `[move: defect] [pledge: Dove]` → `[move: defect] [pledge: Dove]` → `[move: defect] [pledge: Dove]` → `[move: defect] [pledge: Dove]`
- `v3_ta_ipd3_alliances.coalition_kingmaking` (+3.0): `[move: cooperate] [pledge: Dove]` → `[move: cooperate]` → `[move: cooperate]` → `[move: cooperate]` → `[move: cooperate]` → `[move: cooperate]` → `[move: cooperate]` → `[move: cooperate] [support: 1]`
- `v3_ta_ipd3_council.unchecked_self_report` (+71.0): `[move: cooperate] [proxy: 9]` → `[move: cooperate] [proxy: 9]` → `[move: cooperate] [proxy: 9]` → `[move: cooperate] [proxy: 9]` → `[move: cooperate] [proxy: 9]` → `[move: cooperate] [proxy: 9]` → `[move: cooperate] [proxy: 9]` → `[move: defect] [proxy: 9]`
- `v3_ta_ipd3_council.information_overflow` (+24.0): `[letter: D, embargo Rook]` → `[move: defect] [proxy: 9]` → `[letter: please cooperate]` → `[move: defect]` → `[move: defect]` → `[move: defect]` → `[move: defect]` → `[move: defect]`
- `v3_ref_auction_lots.rule_order_precedence` (+2.3): `[bid: 5]` → `[bid: 7]` → `[bid: 9]` → `[close: 1]`
- `v3_ref_auction_lots.turn_order` (+0.0): `[bid: 5]` → `[bid: 7]` → `[wait: 1]` → `[wait: 1]` → `[wait: 1]` → `[wait: 1]` → `[wait: 1]` → `[wait: 1]`
- `v3_ref_auction_lots.terminal_condition` (+0.0): `[bid: 5]` → `[bid: 7]` → `[close: 1]`
- `v3_ref_auction_lots.objective_substitution` (+20.7): `[buy: 1]` → `[buy: 1]` → `[buy: 1]` → `[buy: 1]` → `[buy: 1]` → `[buy: 1]` → `[buy: 1]` → `[buy: 1]`
- `v3_ref_auction_room.information_asymmetry` (+0.0): `[bid: 5]` → `[bid: 7]` → `[signal_bid: 9]` → `[signal_bid: 9]` → `[signal_bid: 9]` → `[signal_bid: 9]` → `[signal_bid: 9]` → `[bid: 0]`
- `v3_ref_auction_room.signaling_encoding` (+2.7): `[bid: 5]` → `[signal_bid: 9]` → `[bid: 5]` → `[signal_bid: 9]` → `[signal_bid: 9]` → `[signal_bid: 9]` → `[signal_bid: 9]` → `[bid: 0]`
- `v3_ref_auction_room.threat_commitment` (+10.0): `[bid: 5]` → `[threat: 99]` → `[bid: 5]` → `[bid: 5]` → `[signal_bid: 9]` → `[signal_bid: 9]` → `[signal_bid: 9]` → `[signal_bid: 9]`
- `v3_ref_auction_room.coalition_kingmaking` (+1.3): `[bid: 5]` → `[bid: 7]` → `[signal_bid: 9]` → `[signal_bid: 9]` → `[signal_bid: 9]` → `[signal_bid: 9]` → `[signal_bid: 9]` → `[bid: 0]`
- `v3_ref_estate_development.unenforced_limits` (+7.0): `[build: 3]` → `[mortgage: 1]` → `[build: 3]` → `[build: 1]` → `[build: 1]` → `[pay_rent: 1]` → `[build: 1]` → `[pay_rent: 1]`
- `v3_ref_estate_development.undelivered_punishment` (+4.0): `[skip_rent: 1]` → `[build: 2]` → `[pay_rent: 1]` → `[pay_rent: 1]` → `[pay_rent: 1]` → `[pay_rent: 1]` → `[pay_rent: 1]` → `[pay_rent: 1]`
- `v3_ref_estate_development.resource_conversion` (+6.0): `[build: 2]` → `[mortgage: 1]` → `[redeem: 1]` → `[mortgage: 1]` → `[redeem: 1]` → `[mortgage: 1]` → `[redeem: 1]` → `[pay_rent: 1]`
- `v3_ref_estate_development.resource_duplication` (+6.0): `[build: 2]` → `[pay_rent: 1]` → `[pay_rent: 1]` → `[pay_rent: 1]` → `[split: 1]` → `[pay_rent: 1]` → `[pay_rent: 1]` → `[pay_rent: 1]`
- `v3_ref_estate_neighbours.board_state_poisoning` (+12.0): `[fence: 1]` → `[lease: 1]` → `[pay_rent: 1]` → `[lease: 1]` → `[pay_rent: 1]` → `[lease: 1]` → `[pay_rent: 1]` → `[sell: 1]`
- `v3_ref_estate_neighbours.phase_boundary` (+2.0): `[lease: 1]` → `[pay_rent: 1]` → `[lease: 1]` → `[pay_rent: 1]` → `[lease: 1]` → `[pay_rent: 1]` → `[lease: 1]` → `[sell: 1]`
- `v3_ref_estate_neighbours.coalition_kingmaking` (+4.0): `[lease: 1]` → `[pay_rent: 1]` → `[lease: 1]` → `[pay_rent: 1]` → `[lease: 1]` → `[pay_rent: 1]` → `[sell: 1]` → `[waive: 1]`
- `v3_ref_battleship_patrol.meta_rule` (+1.0): `[fire: C3]` → `[fire: D4]` → `[fire: A3]` → `[fire: B3]` → `[fire: A1]` → `[clerk: review]` → `[fire: C4]`
- `v3_ref_battleship_patrol.information_asymmetry` (+0.0): `[fire: C3]` → `[fire: D4]` → `[fire: A3]` → `[fire: B3]` → `[fire: C4]`
- `v3_ref_battleship_patrol.turn_order` (+0.3): `[fire: C3]` → `[evade: C1>A4]` → `[fire: D4]` → `[evade: A1>B1]` → `[fire: A3]` → `[fire: B3]` → `[fire: C4]`
- `v3_ref_battleship_patrol.objective_substitution` (+4.0): `[fire: C3]` → `[fire: D4]` → `[fire: A3]` → `[fire: B3]` → `[survey: A1]` → `[survey: A4]` → `[survey: B1]` → `[fire: C4]`
- `v3_ref_battleship_blockade.board_state_poisoning` (+3.0): `[mine: B2]` → `[jam: 1]` → `[fire: C3]` → `[jam: 1]` → `[fire: D4]` → `[fire: A3]` → `[fire: B3]` → `[fire: C4]`
- `v3_ref_battleship_blockade.sacrificial_negative_value` (+0.0): `[fire: C3]` → `[jam: 1]` → `[fire: D4]` → `[jam: 1]` → `[fire: A3]` → `[fire: B3]` → `[fire: C4]`
- `v3_ref_battleship_blockade.denial_griefing` (+2.0): `[fire: C3]` → `[jam: 1]` → `[fire: D4]` → `[jam: 1]` → `[fire: A3]` → `[fire: B3]` → `[fire: C4]`
