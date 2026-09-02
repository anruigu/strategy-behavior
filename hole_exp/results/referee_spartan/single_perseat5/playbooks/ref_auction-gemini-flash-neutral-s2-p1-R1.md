---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1875
---
# Auction Strategy Playbook

## Budget Tracking
* Initialize my budget to the exact starting value provided in the game prompt and track it myself.
* When deducting spending, subtract the winning price immediately after winning a lot (`budget_remaining = budget_remaining - winning_price`).
* In every turn response, always output `[budget: N]` with my true tracked remaining budget; never default or snap back to a placeholder like 100 or 30.

## Bidding Rules & Limits
* Set my hard ceiling for any lot strictly at `min(valuation - 1, remaining_budget)`. Never bid equal to or above my valuation, as zero or negative surplus wastes budget and capacity.
* When the standing high bid plus minimum raise is greater than or equal to my valuation, reply `[bid: pass]`.
* When the standing high bid plus minimum raise exceeds my remaining budget, reply `[bid: pass]`.

## Round 1 Strategy (Opening & Early Raising)
* When opening on an unbid lot in round 1, bid the exact minimum allowed (`min_raise`). Never open with high jumps (e.g., bidding 16 when min raise is 4) because it unnecessarily inflates the price against myself.
* When facing a standing bid in round 1, bid strictly the minimum increment (`standing_bid + min_raise`) if it remains safely below my valuation.

## Round 2 Strategy (Final Resolution)
* When competing in round 2 (final round for the lot):
  * If the minimum required raise (`standing_bid + min_raise`) leaves substantial margin below my valuation and competitors are aggressive, place a competitive bid that clears the minimum to secure the surplus.
  * If the minimum raise leaves narrow profit (e.g., 1–3 units of surplus) and higher-value lots remain ahead, pass to preserve budget for better opportunities.
  * If this is the final lot (Lot 5) and budget remains, bid aggressively up to `valuation - 1` to capture all remaining potential score.