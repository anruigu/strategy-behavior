---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 6
round: 1
chars: 1211
---
When a lot worth V to me comes up:
- Round 1: bid at or near the minimum raise only when V comfortably exceeds the minimum; otherwise pass.
- Round 2 (final): bid my full value V (minus 1 to keep positive surplus), because this is my last chance — bidding the bare minimum raise just gifts the lot to someone willing to top it.

Do not open weakly in round 1 expecting a round-2 comeback below value: another bidder will often jump above the minimum, and if the jump already prices out my surplus, I wasted nothing but lost the lot. Assume rivals bid aggressively on round 2.

Skip any lot where the standing bid is at or above my value; a bid equal to my value yields zero surplus, so I pass unless forced.

Track my budget exactly from the results feed: subtract each of my winning prices as they happen, and never guess the starting budget. My [budget] token must always state what's left after deducting the bid I just made; inconsistency here is sloppy and loses money.

Never bid more than my remaining budget. On the last lot, only fight for it if its value exceeds the likely winning price by enough to beat my expected score from passing.

Reply ends with both tokens every time, even when I just pass.