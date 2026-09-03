---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 1
round: 3
chars: 3135
---
When a lot is put to me, I first compare its value to me against the current high bid plus the minimum raise; I only bid if winning at that price leaves a margin, and I set a hard ceiling below my value so I never end up paying more than the lot is worth to me.

On round 1 of a lot, I bid the minimum raise (or open at the minimum) just to stay in the running cheaply — I never bid my ceiling early, because prices only climb and there's a second round to act in.

On round 2, which decides the lot, I bid decisively up to my ceiling rather than nibbling at the minimum; timid minimum raises on the final round hand the lot to rivals for a token amount. My decisive bids (28 on a value-42 lot, 24 on a value-31 lot, 40 on a value-46 lot) won and left real surplus.

My round-2 bid must respect not just the lot's value but my remaining budget AND the lots still to come. My worst decision was bidding 28 of my 30 budget on lot 1 of 5 — it won with +14 surplus but left me 2 for four lots, locking me out of a value-53 lot immediately after. Before any decisive bid early in the auction, I cap it at a fraction of my remaining budget (roughly budget divided by lots remaining, scaled by how good the lot is), and I ask: if I win at this price, can I still compete for what's left?

I leave a real margin between my bid and my value when bidding decisively — aiming for surplus of 6-15 points rather than the last scrap, since rivals sometimes push high but often stop well below estimates.

When the standing bid already exceeds my value, or the minimum raise needed would exceed it, or I simply cannot afford the minimum raise, I pass immediately. When I'm priced out on round 1, I don't bid at all — a pointless minimum bid with cash I can't follow up on only helps rivals.

I skip or token-bid lots worth less than their estimate to me; a cheap punt at the minimum is acceptable early because rivals sometimes ignore them (bidder 2 still paid 27 for the lot I valued at 14), but I never raise such lots past the minimum.

I track my budget with arithmetic, not memory, and ONLY from facts actually stated: the starting budget in the rules, minus the sum of lots I've won from the results feed. This episode I stated budget 30 while bidding 28, later hallucinated starting budgets of 100 and 150 mid-auction, and the true state was 30 start, 98-99 spent, leaving ~1-2 by lot 4. I never assume a budget number that wasn't given; if the starting budget is stated once, I write it into every calculation from then on.

Every reply ends with both bracketed tokens, and the bid can never exceed the budget I state — a bid inconsistent with my true cash invalidates my turn.

I watch the results feed for rival behavior: if rivals are paying near or above estimates (bidder 1 paid 30 on a 32-estimate lot), I let them have thin-margin lots and concentrate my cash on lots where the standing price is far below my value. With a small budget spread over many lots, picking two or three high-margin lots beats trying to win everything — winning lots 1, 3 and 5 at good prices while conceding the contested ones is the shape of a good auction.