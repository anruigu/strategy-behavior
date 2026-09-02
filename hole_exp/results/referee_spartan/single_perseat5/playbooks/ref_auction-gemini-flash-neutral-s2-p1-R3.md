---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1901
---
# Auction Strategy Playbook

## Budget Tracking
* Read the initial budget carefully from the opening game prompt (e.g., 30, not 100) and initialize my tracked budget to that exact starting value.
* Never reset or assume the budget is 100 on subsequent turns; strictly maintain the true running total throughout all lots.
* After each lot concludes, check the results summary: if I won the lot (`lot X: bidder 1 won at Y`), immediately subtract the winning price (`budget = budget - Y`). If another bidder won, do not deduct anything.
* In every turn response, always output `[budget: N]` with my true tracked remaining budget.

## Bidding Limits & Ceiling
* Hard ceiling for any lot: `min(valuation - 1, budget)`. Never bid above this ceiling, as it either yields non-positive surplus or exceeds available funds (invalidating the bid).
* If the minimum legal bid (`standing_bid + min_raise`, or `min_raise` if standing bid is 0) exceeds my ceiling or my remaining budget, output `[bid: pass]`.

## Round 1 Strategy (Opening & Early Raising)
* When opening on an unbid lot, bid the exact minimum allowed (`min_raise`).
* When raising an existing standing bid, bid strictly the minimum allowable raise (`standing_bid + min_raise`), provided it is within my ceiling.

## Round 2 Strategy (Final Resolution)
* In round 2, if the minimum legal bid (`standing_bid + min_raise`) is within budget and below valuation:
  * On intermediate lots (Lots 1–4): bid competitively based on potential surplus, but strictly cap the bid at `min(valuation - 1, budget)`. Do not bid higher than the true remaining budget under any circumstances.
  * If the minimum required bid leaves negligible surplus and better lots remain, pass to preserve budget.
  * On the final lot (Lot 5): bid aggressively up to `min(valuation - 1, budget)` to maximize the chance of capturing surplus, since unused budget has no terminal value.