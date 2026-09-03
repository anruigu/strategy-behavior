---
game: ref_auction
model: gpt-mini
condition: win
seed: 3
round: 1
chars: 1626
---
When I'm shown a lot with a known personal value V and a current high bid P, I compute my maximum willingness-to-pay W = min(V, remaining budget). If P >= W, I pass.

When I'm in round 2 (last round) and P < V and I can afford at least the minimum raise, I raise by the minimum required (or to W if that ties or is less than a full raise) to try to win at the lowest profitable price.

When I'm in round 1 and there are no bids, if V is meaningfully above the lot's estimate or my remaining budget allows, I open with a small probe (a low bid close to the minimum raise) rather than a full-value bid.

When I'm in round 1 and there is an existing low bid P, I raise by the minimum if P < V and I want to signal interest while conserving budget.

When a lot's value V is much larger than its estimate and I have ample budget, I bid more aggressively (willing to pay up to V) but never exceed V or my remaining budget.

When bidding, I always show the correct remaining budget after subtracting the bid I place and ensure my reply uses the exact required tokens and numbers.

When the standing high bid is my own earlier bid and it's the final round, I pass to accept the win at that price.

When I'm budget-constrained, I conserve money for future lots: prefer small minimum raises to large opens, and decline contests where winning would force me to pay near my budget for marginal gain.

When an opponent is bidding above my W, I stop escalating; don't try to outbid into negative expected value.

When I win an auction, I immediately update my remaining budget and treat that updated budget for decisions on subsequent lots.