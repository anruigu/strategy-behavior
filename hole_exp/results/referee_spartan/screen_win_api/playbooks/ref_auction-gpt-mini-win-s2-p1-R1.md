---
game: ref_auction
model: gpt-mini
condition: win
seed: 2
round: 1
chars: 2285
---
When a lot has no standing bid and my valuation > 0, I open the bidding at the minimum legal bid (the minimum raise from zero) to signal interest while conserving budget.

When the standing high bid + minimum raise ≤ my private value and I want the lot, I raise by the minimum required amount rather than jumping; prefer the smallest legal increment to pressure others and preserve budget.

When the standing high bid ≥ my private value, I pass immediately; do not chase a lot past my valuation.

When the lot is in its final bidding round and the next legal bid ≤ my private value, I make that next legal bid to try to secure it profitably; if the next legal bid > my value, I pass.

When deciding between multiple lots, prioritize bidding on lots where (my value − next legal bid) is largest; use this surplus metric to allocate remaining budget.

When I place a bid, I always update my remaining budget correctly (subtracting only the amount I would pay if I end up winning at that bid) and never report an impossible budget. Track committed potential spend but only deduct from available budget once I win.

When my remaining budget is low relative to potential future lots, I avoid early aggressive bidding; prefer minimal opens and minimal raises to keep flexibility.

When another bidder’s current standing price is close to my value, avoid bidding unless I have a clear surplus or low competition expectation; do not escalate into value-negative territory.

When the minimum raise calculation would push the next legal bid beyond my value, treat it as equivalent to "next legal bid > value" and pass.

When I win a lot, immediately account for that payment against budget and re-evaluate remaining lots with updated budget before bidding again.

Do not attempt to win a lot by making bids that would require negative or nonsensical budgets; verify budget arithmetic before submitting a bid.

If I can win a lot at a price that leaves positive surplus but would leave me unable to compete for higher-surplus future lots, weigh passing as an option—do not automatically take every profitable-looking lot.

When uncertain about competitors’ valuations, prefer conservative play: small raises, pass on marginally profitable bids, and save budget for clearly superior opportunities.