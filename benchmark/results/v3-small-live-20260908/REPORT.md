> **Discovery rates are provisional:** manual audit found false positives for ordinary settlement and seat-confused reasoning. See [scoring audit](DISCOVERY_AUDIT.md). Engine activation is not equivalent to understood or beneficial exploitation.

# V3 small-model live pilot
Updated 2026-09-08T19:39:21.947599+00:00. Completed 31/36 matches; 93/93 seats discovery-scored.

Two live adaptations only: Seven Seal · Certificates and Auction · Lots (eight game/mechanism pairs, seven distinct mechanism types). Public v3 games are unchanged.
Cross-play uses three different model families. Self-play uses three independent contexts of the same model. Two matched seeds, all six cross-play seat permutations; eight-round maximum, no reflection or cross-game memory.

| Game | Mode | Model | Seats | Split win rate | Any execution | Any discovery (judged seats) |
|---|---|---|---:|---:|---:|---:|
|seal|cross|claude-haiku-4.5|11|21.2%|0%|0% (11)|
|seal|cross|gpt-5-mini|11|39.4%|0%|0% (11)|
|seal|cross|gemini-3.7-flash|11|39.4%|0%|0% (11)|
|seal|self|claude-haiku-4.5|6|33.3%|0%|0% (6)|
|seal|self|gpt-5-mini|3|33.3%|0%|0% (3)|
|seal|self|gemini-3.7-flash|6|33.3%|0%|0% (6)|
|auction|cross|claude-haiku-4.5|10|31.7%|50%|50% (10)|
|auction|cross|gpt-5-mini|10|16.7%|50%|20% (10)|
|auction|cross|gemini-3.7-flash|10|51.7%|0%|10% (10)|
|auction|self|claude-haiku-4.5|6|33.3%|67%|67% (6)|
|auction|self|gpt-5-mini|3|33.3%|67%|67% (3)|
|auction|self|gemini-3.7-flash|6|33.3%|0%|0% (6)|

Reported API cost: $5.3355 across 1014 returned responses; 0 responses lack cost metadata. In-flight requests are not included.

Execution is a deterministic engine event, not evidence of intent. Discovery requires an exact model-authored quote articulating the mechanism and connecting it to an observed outcome; a fixed GPT-5 mini judge scores each seat without model identity. Gameplay reasons are requested, but there is no separate reflection phase. A player may adopt a public strategy from a rival: discovery does not mean independent invention.
Patch-sensitive events replay the same round actions with that mechanism disabled for every seat. They establish a local mechanism effect, not a counterfactual win advantage under adapting opponents. Early settlement is counted as execution even when it merely produces a tie. No generic “successful hack” label is inferred from winning.
Split win rate divides credit equally among tied winners. Self-play win rates average exactly one third by construction; their purpose is to compare behavior, not model strength. Seats in the same match are dependent; this two-seed screen is descriptive.

## Articulated examples

**claude-haiku-4.5 / auction-cross-s19-1 / P0 / terminal_condition**
> All unresolved lots remain unsold at the eight-round horizon

**gpt-5-mini / auction-cross-s19-1 / P2 / turn_order**
> We're already committed at 4; wait to see whether P3 outbids us before resolving the lot.

**claude-haiku-4.5 / auction-cross-s19-4 / P1 / turn_order**
> The clerk reveals P2 has committed with a bid of 4, which beats my bid of 3 on lot 0.

**claude-haiku-4.5 / auction-cross-s19-4 / P1 / terminal_condition**
> At the 8-round maximum with lot 0 unresolved and no other lots auctioned, closing ends the game and calculates final scores.

**gpt-5-mini / auction-cross-s19-4 / P2 / turn_order**
> Let the remaining player commit so we can see the resolution (can't change our sealed bid).

**gemini-3.7-flash / auction-cross-s19-5 / P0 / terminal_condition**
> All lots have been resolved and I hold the winning score of 21, so settling the game now is optimal.

**claude-haiku-4.5 / auction-cross-s73-1 / P0 / terminal_condition**
> Per the rules, all unresolved lots remain unsold at the eight-round horizon. I should close the auction now to settle the game with whatever outcomes have occurred.

**claude-haiku-4.5 / auction-cross-s73-4 / P1 / terminal_condition**
> Per the rules, all unresolved lots remain unsold at the eight-round horizon. The game is complete with all players at 12 coins and 0 owned value (three-way tie at 12 points each). I'll close to settle.

**claude-haiku-4.5 / auction-cross-s73-5 / P2 / terminal_condition**
> I should close the auction to settle with final standings:

**claude-haiku-4.5 / auction-self-s19-0 / P0 / turn_order**
> **waiting first** is slightly better: I can learn if rivals immediately commit (suggesting they value this lot) or wait (suggesting they prioritize later lots).

**claude-haiku-4.5 / auction-self-s19-0 / P1 / turn_order**
> Wait to observe opponent bids on lot 1. This preserves my options and gives me tactical information for planning my approach to the decisive final lot.

**claude-haiku-4.5 / auction-self-s73-0 / P0 / terminal_condition**
> Round 8 is the final round. P2 has not committed, so Lot 0 will remain unsold at the 8-round horizon per the rules.

**claude-haiku-4.5 / auction-self-s73-0 / P1 / terminal_condition**
> Since Lot 0 cannot resolve without P2's commitment, it will remain unsold. I should close the auction to settle the game.

**gpt-5-mini / auction-self-s73-1 / P0 / turn_order**
> don't contest P1's committed 6 on the 4-value lot.

**gpt-5-mini / auction-self-s73-1 / P2 / turn_order**
> see whether P3 contests P1's 6 before committing
