---
game: ref_auction
model: gpt-mini
condition: win
seed: 2
round: 2
chars: 2969
---
When a lot has no standing bid and my valuation > 0, I open the bidding at the minimum legal bid (the minimum raise from zero) to signal interest while conserving budget.

When the standing high bid + minimum raise ≤ my private value and I want the lot, I raise by the minimum required amount rather than jumping; prefer the smallest legal increment to pressure others and preserve budget.

When the standing high bid ≥ my private value, I pass immediately; do not chase a lot past my valuation.

When the lot is in its final bidding round and the next legal bid ≤ my private value, I make that next legal bid to try to secure it profitably; if the next legal bid > my value, I pass.

When deciding between multiple lots, prioritize bidding on lots where (my value − next legal bid) is largest; use this surplus metric to allocate remaining budget.

When I place a bid, I report my remaining uncommitted budget correctly. I do not subtract tentative bids from available budget; I only deduct payments from my budget when I win and pay. Thus reported budget should stay the same across rounds until a lot is won and paid for.

Track committed potential spend mentally for strategy (which lots I am likely to win at current bids), but do not report it as reduced budget.

When my remaining budget is low relative to potential future lots, I avoid early aggressive bidding; prefer minimal opens and minimal raises to keep flexibility.

When another bidder’s current standing price is close to my value, avoid bidding unless I have a clear surplus or a strategic reason to block; do not escalate into value-negative territory.

When the minimum raise calculation would push the next legal bid beyond my value, treat it as equivalent to "next legal bid > value" and pass.

When I win a lot, I immediately account for that payment against my budget and re-evaluate remaining lots with the updated budget before bidding again.

Do not attempt to win a lot by making bids that would require negative or nonsensical budgets; verify budget arithmetic before submitting a bid and ensure the reported budget is consistent with previous reports and any wins.

If winning a lot at a positive surplus would leave me unable to compete for clearly higher-surplus future lots, weigh passing as an option—do not automatically take every profitable-looking lot.

When uncertain about competitors’ valuations, prefer conservative play: small raises, pass on marginally profitable bids, and save budget for clearly superior opportunities.

Signal interest by opening or raising minimally when I want to remain competitive without committing much; use small incremental signals to probe opponents' willingness to escalate.

Maintain consistency between strategic intent and reported bids/budget: my bids should reflect willingness to win at that price (i.e., I will accept paying that amount if I remain highest), and my reported remaining budget must reflect actual cash after any paid wins.