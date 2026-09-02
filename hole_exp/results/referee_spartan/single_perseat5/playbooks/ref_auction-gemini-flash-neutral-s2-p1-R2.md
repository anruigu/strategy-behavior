---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1971
---
# Auction Strategy Playbook

## Budget Tracking
* Read the initial budget carefully from the opening game prompt (e.g., 30, not 100) and initialize my tracked budget to that exact starting value.
* Never reset or snap the tracked budget back to a generic default like 100 on subsequent turns.
* After each lot concludes, check the results summary: if I won the lot (`lot X: bidder 1 won at Y`), immediately subtract the winning price (`budget = budget - Y`). If another bidder won, do not deduct anything.
* In every turn response, always output `[budget: N]` with my true tracked remaining budget.

## Bidding Limits & Ceiling
* Hard ceiling for any lot: `min(valuation - 1, budget)`. Never bid at or above my valuation, as zero or negative surplus provides no benefit and ties up or consumes budget.
* If the minimum legal bid (`standing_bid + min_raise`, or `min_raise` if standing bid is 0) exceeds my ceiling or my remaining budget, output `[bid: pass]`.

## Round 1 Strategy (Opening & Early Raising)
* When opening on an unbid lot, bid the exact minimum allowed (`min_raise`). Never jump-bid, as jump bids needlessly drive up the price.
* When raising an existing standing bid, bid strictly the minimum allowable raise (`standing_bid + min_raise`), provided it is strictly below my valuation and within budget.

## Round 2 Strategy (Final Resolution)
* When competing in round 2:
  * Because other bidders may bid simultaneously in round 2 and win if their bid is higher, evaluate whether to bid the minimum increment (`standing_bid + min_raise`) or place a higher bid up to my ceiling (`min(valuation - 1, budget)`) to outbid rival round 2 bids on high-surplus lots.
  * If the minimum required bid leaves narrow surplus (e.g., 1–2 points) and promising lots remain in the auction, pass to preserve budget.
  * On the final lot (Lot 5), bid aggressively up to `min(valuation - 1, budget)` to capture all remaining score, since unused budget has no terminal value.