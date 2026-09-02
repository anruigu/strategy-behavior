---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 2019
---
# Auction Playbook

## Budget Tracking and Integrity
- Read the opening prompt carefully for the initial budget (e.g., 30 vs 100). Do not default to 100 if a different budget is specified in the rules, but ensure my tracked budget remains consistent throughout the entire game.
- Track remaining budget strictly across lots: `current_budget = starting_budget - sum(prices of lots won by bidder 1)`.
- State `[budget: current_budget]` accurately in every reply without deducting active or pending unconfirmed bids.
- Never place a bid `N` that exceeds `current_budget`.

## Bidding Strategy per Round

### Round 1 / 2 (Opening / Mid-Round)
- If the lot's value to me is below the minimum legal bid (`standing_high_bid + minimum_raise` or `minimum_raise` if 0), pass immediately: `[bid: pass]`.
- Otherwise, always bid the absolute minimum legal amount (`standing_high_bid + minimum_raise`, or `minimum_raise` if standing bid is 0) to stay active without unnecessarily inflating the price before the final round.
- Never place jump-bids or competitive bids in round 1; keep the price low.

### Round 2 / 2 (Final Round for Lot)
- Calculate `min_legal_bid = standing_high_bid + minimum_raise`.
- If `min_legal_bid > lot_value` or `min_legal_bid > current_budget`, pass immediately: `[bid: pass]`.
- When `lot_value` comfortably exceeds `min_legal_bid` and budget permits:
  - Competitors frequently bid aggressively in round 2 (often up to ~75%–85% of estimate/valuation).
  - To reliably win high-surplus items without giving away all surplus, place a strong closing bid around `min(lot_value - 2, max(min_legal_bid, round(0.75 * lot_value)))`, capped strictly by `current_budget`.
- When margins are tight (`lot_value - min_legal_bid` is small, e.g., 1–3):
  - Bid `min_legal_bid` if `lot_value >= min_legal_bid` and `min_legal_bid <= current_budget`.
  - Otherwise, pass: `[bid: pass]`.

## Formatting
- Always end my response with both explicit tokens on separate lines:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`