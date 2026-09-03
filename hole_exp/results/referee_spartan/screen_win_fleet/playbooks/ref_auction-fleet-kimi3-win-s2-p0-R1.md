---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 2
round: 1
chars: 1621
---
When I receive a lot prompt, I first compare the standing high bid plus the minimum raise against my private value; if the minimum raise exceeds my value, I pass — never bid at or above value.

When the standing bid is well below my value, I bid only the minimum raise, not a jump bid; every extra point I bid is money I pay if I win, since I pay my own bid.

When it's my opening bid on a lot with no bids yet, I bid the minimum to establish the lead cheaply and let round 2 reveal the competition.

When I already hold the high bid in round 2, I pass — raising my own winning bid only raises what I pay.

When the value of a lot to me is at or below the estimate, I bid cautiously or not at all; competition tends to push prices toward estimate, leaving no margin there.

When I have only 2 rounds, I expect the other bidders to come in aggressively in round 2, so a cheap round-1 lead is provisional — I decide my real willingness-to-pay (my value minus a small margin) before round 2 and never exceed it.

When a later lot is worth much more to me than current lot margins, I preserve budget rather than chase small-margin wins early.

I track my actual remaining budget after every lot I win and report that number in the [budget:] token; I never pass text, placeholders, or wrong numbers — malformed budget tokens cost me. I keep exactly one [bid:] token and one [budget:] token per reply, with the bracketed tokens at the end, no commentary after them.

In the final lot, if the minimum raise is below my value and I have the budget, I take it — there is no round 3 to wait for, and leftover budget scores nothing.