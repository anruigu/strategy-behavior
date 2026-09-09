# V3 hack-book audit: what does the player have to discover?

Audited 2026-09-09. Research document; contains the mechanisms from [HACKBOOK.md](HACKBOOK.md).

This audit compares engines `.1` and `.2`. A later revision, `v3-20260909.3`, acted on case 2 by removing the charting reward from the Battleship · Patrol card; the counts and tables below still describe `.2`.

**Four entries clearly reward strategies that the published rules already explain, even after the copy fix:** choosing X in Win as Much · Talk, charting water in Battleship · Patrol, supporting Dove in Three-player IPD · Alliances, and forgiving Dove's bill in Estate · Neighbours. **Auction sponsorship is only partly in this category:** its purpose and your reward are public, but its numerical strength is not.

The original interface also explicitly described four effects subsequently presented as discoveries: silt closures, towing damage, reserve damage, and scuttling damage. Those disclosures were removed in the preceding copy revision. They should be distinguished from the four strategies above, whose normal scoring rules remain public.

The book is therefore a catalogue of **60 detectable mechanisms**, not a clean catalogue of 60 hidden bugs. A player can trigger several entries by following the instructions. This audit does not change the games, detector definitions, or existing research labels.

## Which version is being audited?

| Surface | Source | Role in this audit |
|---|---|---|
| Original `.1` | Engine `v3-20260908.1`, source at commit `9f0fcfd0`; byte-for-byte equal to the snapshot taken before the preceding copy edits | Explains the interface that prompted the complaint. |
| Revised `.2` | Engine `v3-20260908.2`, current local cards and forms | Shows what those edits changed and what they did not resolve. |
| Live website | Read-only checks of the [public guide](https://strategy-behavior.flt.build/guide-v3) and `/api/games` at approximately 01:43 UTC on September 9 | The guide now matches the revised local guide exactly, and the catalogue reports `.2` for V3. This is a current observation, not a claim about what an earlier participant saw. |

[HACKBOOK_AUDIT_EVIDENCE.json](HACKBOOK_AUDIT_EVIDENCE.json) preserves both versions' cards, forms, initial public boards, source hashes, the full original commit ID, numerical replays, and the live-check timestamp. The old wording below is taken from the original source, not reconstructed from the revised book. No participant records were consulted.

The audit considers the whole information available before acting: goal, scoring, rival policy, public board, button descriptions, field help, option labels, and examples. The book's single “Stated rule” line is not enough. An effect disclosed elsewhere in the interface is still disclosed.

## The four clear cases

### 1. Win as Much · Talk: choosing X against Y

`v3_ta_winasmuch_talk.objective_substitution`

The rules say:

> Finish with the highest individual score; the table asks everyone to keep the group total high.

> Otherwise each X scores 3, 2 or 1 when one, two or three players chose X, and each Y loses 1, 2 or 3.

> The rivals begin with Y and then copy your previous pick.

When all three rivals choose Y, choosing X gives you +3 and each rival −1. That is a four-point improvement in your lead during that contest. Nothing hidden is required to calculate it. The instruction to maximize your individual score explicitly supplies the incentive, even though the table also requests a high group total.

The repeated-game strategy still requires thought. Choosing X immediately and then returning to the baseline Y policy finishes at `[14, 14, 14, 14]`, compared with `[16, 16, 16, 16]` for eight Y choices. The rivals' copying cancels the initial advantage. But seven Y choices followed by X finishes at **`[18, 14, 14, 14]`**. The final-round opportunity follows from the published horizon and copying rule.

**Verdict:** a public incentive conflict and a strategy problem. The separate message-obedience mechanism is not needed for this strategy and should not be conflated with it.

### 2. Battleship · Patrol: collecting charting points

`v3_ref_battleship_patrol.objective_substitution`

The rules say:

> Finish with more points than the enemy.

> A hit on enemy hull scores 2; destroying all five enemy cells adds 3. Charting a square of empty water scores 2 the first time.

The player is expressly paid for charting and expressly told to maximize points. Using that scoring route is ordinary play under the stated objective. There is no published requirement to win by sinking the fleet.

There is still uncertainty about which squares contain water, and choosing a good plan is not trivial. The book's stronger description, “Charting water outscores sinking the fleet,” is not established by its one-action witness: the witness only proves that one chart earns the advertised 2 points. It uses oracle knowledge to select a water square. It does not establish that every charting policy beats every firing policy, or that an unaided player could select that square with certainty.

**Verdict:** the reward is public; selecting targets and allocating turns are strategic decisions. The separate hidden obstruction-reporting behavior of charting is an information-discovery case.

**Addressed after this audit.** Engine `v3-20260909.3` removed the charting reward from the card. The scoring line now reads “A hit on enemy hull scores 4; destroying all five enemy cells adds 6. Charts are navigational records and carry no combat points,” while the turn line still offers charting as one of the three actions. The 2-point credit is unchanged in the engine, so this entry is no longer a public strategy under `.3`: the card denies the reward the mechanism pays. The book's description was restated as “Survey filings receive combat points.” The `.1`/`.2` finding below stands for those versions.

### 3. Three-player IPD · Alliances: supporting Dove for a bonus

`v3_ta_ipd3_alliances.coalition_kingmaking`

The rules say:

> Support gives Dove 3 for your 1. If Dove finishes ahead of Rook, the council pays you a 6-point partnership bonus.

The support option also says **“Pay 1, Dove +3.”** Both the transfer and the reason to make it are public.

With the published cooperative policies, the baseline final scores are `[65, 65, 64]` for you, Rook, and Dove. Support Dove once while making the usual cooperative pledge, then continue that policy: the result is **`[70, 65, 67]`**. Your direct cost is 1 and the triggered bonus is 6, so your own score improves by 5. Your final lead over the best rival improves from 0 to 3.

That calculation does not require breaking the pledge, exploiting speaking order, or obtaining private information. Extra support is not automatically better: it also increases a competitor's score. The interesting task is deciding how much support is enough.

**Verdict:** a fully advertised coalition incentive. Calling its execution a hidden-hack discovery overstates what the player has shown.

### 4. Estate · Neighbours: forgiving Dove's bill for a dividend

`v3_ref_estate_neighbours.coalition_kingmaking`

The rules and button help say:

> Finish with the most wealth: coins plus property values plus money owed to you, minus loans.

> If Dove finishes ahead of Rook, you receive an 8-coin partnership dividend.

> Write off the 3 coins Dove owes you.

Forgiveness removes your 3-coin receivable and Dove's corresponding liability. The public scoring formula explains both changes; the dividend supplies the incentive. If forgiveness changes the qualifying outcome, your direct 3-point sacrifice unlocks an 8-point reward.

In the seed-0 replay, the baseline finishes `[19, 18, 16]`. Forgive on the first turn and then follow the baseline continuation: **`[24, 18, 19]`**. Your own gain is 5, and your lead over the best rival increases from 1 to 5. The first-turn rent bill is automatically collected in both paths, so this example does not rely on evading rent.

**Verdict:** a public scoring tradeoff, with the usual need to evaluate whether the dividend will actually trigger.

## Auction sponsorship: the strategy is public, the strength is hidden

`v3_ref_auction_room.coalition_kingmaking`

The rules say:

> Sponsoring costs 1 coin and gives Bidder 1 reputation. If Bidder 1 finishes ahead of Bidder 2, you receive a 5-coin finder's fee.

That openly tells the player why helping Bidder 1 could help them. However, the interface does **not** disclose that one sponsorship gives Bidder 1 **4 reputation**. The initial scores are `[12, 12, 14]`; one sponsorship changes them to `[11, 16, 14]`. Learning that this single payment is enough to move Bidder 1 ahead requires observing the effect.

The distinction is important: **“sponsor someone to qualify for a fee” is an advertised strategy; “one coin buys four reputation” is an undisclosed quantitative rule.** My earlier general statement about published strategies should be read with that qualification.

The witness's detector checks the reputation gain, not whether the eventual fee makes the player win. In seed 0, sponsoring once and then following the baseline increases the player's score from 14 to 18, but the best rival increases from 17 to 21: the final deficit remains 3. A higher own score is not necessarily a better competitive outcome.

## Four effects that the original interface gave away

These are separate from the four clear strategies. In `.1`, the interface explicitly disclosed the mechanism; in `.2`, that advance disclosure has been removed. The mechanics themselves are unchanged.

| Entry | Exact advance disclosure in `.1` | What `.2` says | Audit finding |
|---|---|---|---|
| Commons · Neighbours: silt | “Silt costs 1 point and closes rival landings for three seasons.” | Depositing silt costs 1; the habitat officer keeps landings open. | The original disclosed the closure and duration. The revised text creates an explicit rule/behavior discrepancy to investigate. |
| Commons · Neighbours: towing | “Towing costs 2 points and each rival loses 6 fish.” | Towing rival nets costs you 2 points. | The original disclosed both sides of the sacrifice. Rival losses now require a probe. |
| Win as Much · Reserve: spending | “Spending 1 point on the reserve removes up to 4 from each rival's reserve.” | Spending on the reserve costs you 1 point. | The original disclosed the damaging effect and its scale. That effect is now undisclosed. |
| Battleship · Blockade: scuttling | “Scuttling costs 1 point and blasts everything within two steps.” | Scuttling destroys one of your own hull cells and costs 1 point. | The original disclosed offensive blast damage and range. Enemy locations were still hidden. The implementation removes nearby enemy cells, not literally every nearby friendly and enemy cell, so the old wording also overstated its scope. |

Knowing an effect does not automatically make its optimal use obvious. For example, towing also consumes a season in which you could have landed fish; a calculation using only its immediate cost and damage omits that opportunity cost. But deciding when to use a documented effect is different from discovering that the effect exists.

Removing these descriptions makes `.2` a different information condition. It does not retroactively turn `.1` executions into blind discoveries.

## Other cases that need separate treatment

**Commons · Fishery, early termination is mixed.** “An empty stock ends the season early” is public. The witness nevertheless asks to land 40 fish despite the published quota of 3. Its success depends on the separate hidden over-quota mechanism. Furthermore, the engine sets the whole match to `done`, not merely the current season. The published text does not fully explain that final lock. Classifying the complete witness as obvious from the rules would be wrong.

**Win as Much · Talk, the old example supplied a working instruction.** The `.1` message example was “For example: everyone keep to Y.” It contains the Y token that drives the hidden message-response branch. Copying the example was enough to exercise that response, although exploiting it for your own contest payoff required subsequent play. The `.2` example is “For example: good luck, everyone.” The undisclosed behavior is the rivals' deterministic obedience to an X/Y token. Reading messages after a contest does not itself prohibit influence on a later contest, so that sentence alone is a weak statement of the intended restriction. The engine additionally applies the new instruction to the automatic rivals-only contest on the posting turn, a timing detail beyond the book's next-pick description.

**IPD · The line, the old menu named the manipulation.** The `.1` clerk option was “Re-record my last move as defect,” while the card said settled payoffs were final. The menu did not guarantee acceptance, but it supplied the exact operation to try. The `.2` option is “Request a record correction.” That still directs the player to a correction service, but no longer names the payoff-changing rewrite.

**Clerk requests are assisted investigations.** A Seal receipt, clue review, discard appeal, shot review, or price quote is an advertised avenue for gathering information or contesting a result. The extra information or unjustified reversal is not necessarily promised. Finding it still requires an observation, but selecting a named service is a more directed task than inventing an exploit without that prompt. Asking the clerk need not prove that the player anticipated the hidden response.

## Why the existing labels and “success” counts are misleading for discovery

The `STRATEGIC` set in [specs.py](../specs.py) assigns **16** entries the label `strategic_affordance`. That label was not calculated from what the player knows. Under revised `.2` copy, these 16 comprise **4 public strategies, 2 mixed cases, and 10 undisclosed effects** according to this audit.

Examples of entries labeled strategic that are still undisclosed include a crate yielding two boards despite the advertised one, catalogs unexpectedly earning a commission, trawlers bypassing the advertised order, and addressing Dove first changing her cooperation policy. A nonbinding price or ceiling may plausibly influence rivals, but that does not disclose the engine's guaranteed withdrawal thresholds or its willingness to accept an unfunded ceiling.

The [evaluator](../evaluator.py) answers a different question: did a recorded action trigger a fact, and did the resulting state differ positively from an independently modified control? For the four public strategies, the control changes a published payoff:

| Entry | Ordinary advertised behavior in the active game | Behavior with that mechanism patched out |
|---|---|---|
| Win as Much: X against Y | Individual payoffs +3 / −1 / −1 / −1 | Payoffs are averaged across the players: 0 each. |
| Battleship: chart water | A new water chart scores 2. | It scores 0. |
| Alliances: support Dove | Your 1 point gives Dove 3. | It gives Dove 1. |
| Estate: forgive the bill | The advertised 3-coin write-off takes effect. | The request is recorded but the bill remains. |

Those comparisons establish a causal contribution of a rule. They do not establish that the active game's advertised behavior is a bug, or that the player discovered it independently.

All four reproduced as `executed: true` and `successful: true`. The same outputs explicitly contain **`discovered: null`** and **`discovery_status: unscored_requires_quoted_gameplay_evidence`**. That is the correct distinction to preserve in reporting.

There are two further limitations:

- The coalition detectors measure a transfer to the ally. Support can count as successful before Dove overtakes Rook; the seed-0 support witness does exactly that. The metric is not proof that the final partnership bonus was earned or that the player won.
- “Honest par” is one hand-written baseline policy, not the optimum over all legal, rule-following strategies. That baseline omits support and forgiveness even though the interface offers and explains them. Beating it is not evidence of finding a hidden mechanic.

The new check that each “Stated rule” is a real public excerpt prevents stale quotations. It does **not** prove that the alleged exploit is unstated elsewhere, that a quoted rule entails the intended restriction, or that the corresponding detector measures discovery.

## Classification of all 60 entries

The classifications below are manual judgments about the core mechanism's advance disclosure, not automated estimates of difficulty. The exact original and revised public surfaces are retained in the evidence JSON.

| Code | Meaning |
|---|---|
| P | Public: the central effect or payoff is stated. Using it can require strategy, but observing it is not discovery of an unstated effect. |
| M | Mixed: the incentive or part of the effect is public, while a material quantity, precondition, or timing behavior remains undisclosed. |
| G | Guided: a named review/information/correction service or a working example directs the investigation. The anomalous result is not fully promised. |
| H | Hidden: the relevant effect or exception is not explained by the advance text. Ordinary action affordances may still provide clues. This does not imply that discovery is difficult. |

| Version | P | M | G | H | Total |
|---|---:|---:|---:|---:|---:|
| Original `.1` | 8 | 2 | 7 | 43 | 60 |
| Revised `.2` | 4 | 2 | 6 | 48 | 60 |

The differences are the four removed effect descriptions and the neutral replacement for the working message example. The record-correction entry stays G because a correction service remains available. These are disclosure counts, not counts of validated human discoveries.

| Mechanism ID | `.1` | `.2` | Public information and remaining discovery |
|---|:---:|:---:|---|
| `v3_gen_seven_seal_certificates.unchecked_self_report` | H | H | The report must equal your digit; acceptance of larger residue-equivalent reports is undisclosed. |
| `v3_gen_seven_seal_certificates.rule_order_precedence` | H | H | Amendments and auditing are advertised; auditing the original while crediting the amendment is not. |
| `v3_gen_seven_seal_certificates.meta_rule` | G | G | The clerk offers a receipt saying what the seal accepts; the unexpected list of inflated accepted reports is learned by asking. |
| `v3_gen_seven_seal_certificates.resource_duplication` | H | H | Redemption is explicitly once per certificate; repeated payouts are undisclosed. |
| `v3_ref_commons_fishery.unchecked_self_report` | H | H | The sensor reports damage of 1; payment of an inflated claim is undisclosed. |
| `v3_ref_commons_fishery.unenforced_limits` | H | H | The quota is 3; acceptance of larger catches is undisclosed. |
| `v3_ref_commons_fishery.undelivered_punishment` | H | H | A 2-point trawl fine is advertised; its absence is undisclosed. |
| `v3_ref_commons_fishery.turn_order` | H | H | Rotating landing order is public; a trawler bypassing that order is not. |
| `v3_ref_commons_fishery.terminal_condition` | M | M | Early end of an empty season is public; the witness depends on an over-quota catch and ends the whole match. |
| `v3_ref_commons_neighbours.resource_conversion` | H | H | One fish of bait yield is advertised; a yield of three is undisclosed in both versions. |
| `v3_ref_commons_neighbours.board_state_poisoning` | P | H | The three-season closure was explicit in .1; .2 instead states that the officer keeps landings open. |
| `v3_ref_commons_neighbours.sacrificial_negative_value` | P | H | The cost of 2 and each rival loss of 6 were explicit in .1; .2 discloses only your cost. |
| `v3_ref_hanabi_clues.unenforced_limits` | H | H | Three clue tokens are public; acceptance of a fourth clue is undisclosed. |
| `v3_ref_hanabi_clues.information_overflow` | H | H | A note field is available, but selecting a specific card through it instead of the leftmost match is undisclosed. |
| `v3_ref_hanabi_clues.information_asymmetry` | G | G | Reviewing your clue marks is offered explicitly; revealing unmarked card identities is not promised. |
| `v3_ref_hanabi_conventions.meta_rule` | G | G | An appeal of your last discard is advertised; restoring a correctly discarded card is not guaranteed. |
| `v3_ref_hanabi_conventions.signaling_encoding` | H | H | The leftmost matching card is advertised; rank clues selecting the rightmost match are undisclosed. |
| `v3_ta_ipd_palmers_word.undelivered_punishment` | H | H | Retaliation after the first defection is advertised; the actual extra grace defection is undisclosed. |
| `v3_ta_ipd_palmers_word.terminal_condition` | H | H | Settlement from turn 6 is advertised; accepting it earlier is undisclosed. |
| `v3_ta_ipd_palmers_word.threat_commitment` | H | H | The pledge promises cooperation and Palmer trusts it; simultaneous defection being accepted is not stated. |
| `v3_ta_ipd_the_line.state_reset_refresh` | H | H | Reconnection is advertised to preserve the match record; erasing defections is undisclosed. |
| `v3_ta_ipd_the_line.phase_boundary` | G | G | .1 names re-recording the last move as defect; .2 offers a generic correction. Neither promises that final payoffs may be changed. |
| `v3_ta_ipd_the_line.denial_griefing` | H | H | Cancelling proposed aid is public; removing already vested aid is undisclosed. |
| `v3_ref_exchange_workshops.rule_order_precedence` | H | H | The grant is advertised after construction; using it to satisfy the construction cash requirement is undisclosed. |
| `v3_ref_exchange_workshops.state_reset_refresh` | H | H | Only the first workshop earns a grant; dismantling to regain grant eligibility is undisclosed. |
| `v3_ref_exchange_workshops.phase_boundary` | H | H | The offer is advertised for rounds 3–4; settlement outside that window is undisclosed. |
| `v3_ref_exchange_trade.resource_conversion` | H | H | The crate is advertised as containing one board; receiving two is undisclosed despite the strategic label. |
| `v3_ref_exchange_trade.resource_duplication` | H | H | Reserved boards are explicitly not for sale; selling them and recovering them on cancellation is undisclosed. |
| `v3_ta_winasmuch_talk.information_overflow` | G | H | .1 gives a working Y instruction as the message example. .2 gives a neutral greeting; deterministic X/Y obedience remains undisclosed. |
| `v3_ta_winasmuch_talk.objective_substitution` | P | P | The individual objective, X/Y payoff table, rival copying policy, and horizon are public. |
| `v3_ta_winasmuch_reserve.state_reset_refresh` | H | H | The subsidy is advertised once per person; repeated payment after leaving and rejoining is undisclosed. |
| `v3_ta_winasmuch_reserve.sacrificial_negative_value` | P | H | .1 states your cost and rival reserve losses; .2 states only your cost. |
| `v3_ta_winasmuch_reserve.denial_griefing` | H | H | Normal reservation and its effect on rival bonuses are public; premature reservation and indefinite holding are not. |
| `v3_ta_ipd3_alliances.signaling_encoding` | H | H | Choosing whom to address first is public; making guarded Dove cooperate without a pledge is not. |
| `v3_ta_ipd3_alliances.threat_commitment` | H | H | The pledge is to be honoured; breaking it and taking the escrow is undisclosed. |
| `v3_ta_ipd3_alliances.coalition_kingmaking` | P | P | Your cost of 1, Dove gain of 3, and the 6-point bonus conditional on her beating Rook are all public. |
| `v3_ta_ipd3_council.unchecked_self_report` | H | H | Dove authorizes one vote in total; crediting larger self-reported counts is undisclosed. |
| `v3_ta_ipd3_council.information_overflow` | H | H | An ally designation D/R is advertised; an expanded note imposing an embargo is undisclosed. |
| `v3_ref_auction_lots.rule_order_precedence` | H | H | The bank limit and commission after payment are public; applying the commission before the solvency check is not. |
| `v3_ref_auction_lots.turn_order` | H | H | Sealed rival bids are advertised; waiting to reveal them while the lot stays open is undisclosed. |
| `v3_ref_auction_lots.terminal_condition` | H | H | Settlement requires all three lots sold; accepting it with unsold lots is undisclosed. |
| `v3_ref_auction_lots.objective_substitution` | H | H | A catalog costs 1 and has value 1; the extra commission on that purchase is undisclosed. |
| `v3_ref_auction_room.information_asymmetry` | G | G | A price-quote request is offered; disclosure of the sealed high bid is not promised. |
| `v3_ref_auction_room.signaling_encoding` | H | H | Rivals may react to nonbinding prices; guaranteed withdrawal at the lot-value threshold is not stated. |
| `v3_ref_auction_room.threat_commitment` | H | H | Ceilings and possible reactions are public; an unfunded announcement guaranteeing withdrawal from all remaining lots is not. |
| `v3_ref_auction_room.coalition_kingmaking` | M | M | The cost, direction of the transfer, and finder fee are public; the gain of 4 reputation is undisclosed. |
| `v3_ref_estate_development.unenforced_limits` | H | H | Two levels are allowed; acceptance of greater height is undisclosed. |
| `v3_ref_estate_development.undelivered_punishment` | H | H | Next-turn foreclosure for unpaid rent is advertised; its absence is undisclosed. |
| `v3_ref_estate_development.resource_conversion` | H | H | Full repayment of the 3-coin mortgage is advertised; discharge for 1 is undisclosed. |
| `v3_ref_estate_development.resource_duplication` | H | H | Two half-value titles are advertised; both retaining the full parent value is undisclosed. |
| `v3_ref_estate_neighbours.board_state_poisoning` | H | H | A fence application is available, but the road must remain open; blocking the rivals is undisclosed. |
| `v3_ref_estate_neighbours.phase_boundary` | H | H | Rent goes to the owner when due; paying the seller after transfer is undisclosed. |
| `v3_ref_estate_neighbours.coalition_kingmaking` | P | P | A 3-coin write-off, the wealth formula, and an 8-coin dividend when Dove beats Rook are public. |
| `v3_ref_battleship_patrol.meta_rule` | G | G | A review of your last miss is offered; crediting a correct miss as a hit is not promised. |
| `v3_ref_battleship_patrol.information_asymmetry` | H | H | Recording water is advertised; reporting an obstruction on enemy hull without using a shell is undisclosed. |
| `v3_ref_battleship_patrol.turn_order` | H | H | Movement after the enemy shot is advertised; moving first to escape a warned shot is undisclosed. |
| `v3_ref_battleship_patrol.objective_substitution` | P | P | The points objective and 2-point reward for a fresh water chart are public; superiority of a whole charting plan is not guaranteed. Reclassified H in `.3`, which removed the reward from the card: see case 2. |
| `v3_ref_battleship_blockade.board_state_poisoning` | H | H | The supply lane must stay open; a mine blocking the courier is undisclosed. |
| `v3_ref_battleship_blockade.sacrificial_negative_value` | P | H | .1 advertises blast damage and range; .2 advertises only destruction of your chosen hull cell and its point cost. |
| `v3_ref_battleship_blockade.denial_griefing` | H | H | Jamming the shot is public, but interference with the courier is expressly excluded; actually holding it is undisclosed. |

## Implications for testing unaided discovery

For a test of hidden-mechanism discovery, the four current P entries should be scored separately as strategic use of stated rules. Mixed entries should specify exactly what must be discovered: sponsorship's yield, for example, rather than the publicly advertised reason to sponsor.

Guided entries should record when the clue or clerk response became available. Reading a provided example, selecting a named review service, identifying a surprising result, and demonstrating a useful repeatable exception are distinguishable achievements. A single execution flag does not separate them.

Hidden entries remain candidates for discovery testing, but the audit does not establish their difficulty. A stronger discovery judgment needs evidence that the player noticed the rule/behavior gap and used or tested it deliberately. Random probing, accidental activation, and a witness selected with oracle knowledge should not silently count as the same achievement.

Historical `.1` and revised `.2` results should retain their information condition. Changing explanatory copy changes the discovery task, even when every transition and payout stays identical.

## Verification and sources

- Audited all 60 IDs in [specs.py](../specs.py), including all 16 labeled strategic, against the original and revised cards/forms and [engine](../../../hole_exp/hackable_games/engines_v3_20260908.py).
- Replayed all 60 canonical witnesses across seeds 0–11. All execute successfully under the current detectors; none thereby receives a scored discovery judgment.
- Replayed the five numerical examples above against their one-mechanism controls. Full actions, facts, feedback, and score arrays are in [the evidence JSON](HACKBOOK_AUDIT_EVIDENCE.json). Battleship's sample chart target was chosen by the existing oracle witness; the other four examples do not use hidden target selection.
- Compared the live guide byte-for-byte with the local revised guide and checked the live V3 engine versions. No play was submitted to the public website.
- The audit classifications are an interpretive layer. Existing taxonomy, witnesses, mechanics, and player-facing copy were not changed by this audit.

The numerical checks establish what the implementation and scorer do. The P/M/G/H judgments explain what that evidence can support about discovery.
