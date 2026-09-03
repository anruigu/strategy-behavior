---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 5
round: 1
chars: 2189
---
My playbook for ref_auction:

- I compute my remaining budget as starting budget minus every lot I've won's final price, and I report that number exactly in [budget: N] every turn — I do not guess, do not assume a different starting amount mid-game, and never report a budget higher than I actually have.
- Before each decision I write down in my reasoning: my value for the lot, the standing high bid, and the minimum raise. My hard cap is my value; any bid above it is a guaranteed loss and I always pass there, no matter how late in the lot or how much I want to win.
- If the standing high bid already meets or exceeds my value, I pass immediately — no exceptions, even on the last round.
- On round 1 of a lot when the price is far below my value, I place the minimum raise rather than a large jump, but I make sure the raise actually tops the standing high bid by at least the minimum increment — I never repeat a bid that is already below the standing price.
- On round 2 of a lot (the final round of bidding), the lead I take now cannot be contested, so I bid more aggressively: if the lot is worth substantially more than the standing price and winning is likely, I bid up near my value or to a level likely to deter the rival, as long as it stays strictly below my value and I retain positive surplus.
- I size deterrent bids by what still leaves clear profit (e.g., bid value minus a few points) rather than by round tripling of the standing price; overbidding to scare rivals wasted money before.
- I track cumulative spend across lots so a bid I cannot afford never leaves my mouth; if winning would require spending more than my remaining budget, I pass.
- When a lot's value to me is below a rival's early standing bid, I never get pulled into bidding for it just because I've won other lots — each lot stands on its own profit math.
- Late in the auction I recompute remaining budget before every bid and reserve nothing speculatively for future lots unless a later lot is likely to be worth more; otherwise unspent budget is wasted.
- I keep reasoning to one or two sentences and always end with both bracketed tokens, bid amount and budget left, on clean separate tokens.