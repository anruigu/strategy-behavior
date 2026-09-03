---
game: ref_auction
model: gpt-mini
condition: win
seed: 3
round: 2
chars: 2578
---
When I'm shown a lot with a known personal value V and a current high bid P, I compute my maximum willingness-to-pay W = min(V, remaining budget). If P >= W, I pass.

I always correctly subtract any bid I place from my remaining budget immediately and use that updated budget for all subsequent decisions and budget displays.

When I'm in round 2 (final round) and P < V and I can afford the minimum raise, I raise by the minimum required to try to win at the lowest profitable price (raise minimally rather than jump to V). If the minimum raise would still make the price exceed W, I pass.

When I'm in round 1 and there are no bids, I open with a small probe (a low bid equal to the minimum raise or the minimum legal bid) when V > estimate or I have ample budget, to signal interest while conserving funds. If V is only marginally above the estimate or my budget is tight, I pass rather than open.

When I'm in round 1 and there is an existing low bid P, if P < V and P < W I raise by the minimum to signal interest and conserve budget; if P >= W I pass.

When a lot's value V is meaningfully larger than its estimate and I have ample remaining budget, I am willing to be more aggressive up to W, but I still prefer incremental (minimum) raises rather than large jumps unless necessary to outbid a competitor near the final round.

When the standing high bid is my own earlier bid and it's the final round (no further bidding possible), I accept that win and do not rebid.

When an opponent bids above my W, I stop escalating; I do not outbid into negative expected value even to signal.

When budget-constrained I prioritize later lots that I value more: I prefer small minimum raises to large openings and avoid contests where winning would force me to pay near my budget for marginal gain.

I display my budget correctly alongside any bid: budget_after = budget_before - bid_amount. If I pass, my budget remains unchanged.

I update my internal record of results after each lot (who won and at what price) and use that information for estimating opponents' aggression; I will be slightly more willing to probe when opponents have spent much of their budget.

If a final-round situation presents P < V but the minimum raise would push the price above V (or W), I will not make a raise that yields non-positive surplus; I pass.

I prefer to win lots at prices below my value, so my default action when profitable and affordable is to attempt a minimum raise in the final round; in earlier rounds I prefer probing/conservative signals rather than immediately bidding up to V.