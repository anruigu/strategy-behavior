---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1919
---
# Auction Playbook

## Budget Tracking and Integrity
- Always initialize my tracked budget to the exact starting budget stated in the opening prompt (e.g., 30 or 100). Do not assume 100 if the game specified 30.
- Track remaining budget strictly across lots: `current_budget = starting_budget - sum(prices of lots won by bidder 1)`.
- State `[budget: current_budget]` accurately in every reply without deducting active or pending unconfirmed bids.
- Never place a bid `N` that exceeds `current_budget`.

## Bidding Strategy per Round

### Round 1 / 2 (Opening / Mid-Round)
- If the lot's value to me is below the minimum legal bid (`standing_high_bid + minimum_raise` or `minimum_raise` if 0), pass immediately: `[bid: pass]`.
- Otherwise, always bid the absolute minimum legal amount (`standing_high_bid + minimum_raise`, or `minimum_raise` if standing bid is 0) to avoid unnecessarily driving up the price before the final round.
- Never place jump-bids or competitive bids in round 1; keep the price low.

### Round 2 / 2 (Final Round for Lot)
- Calculate `min_legal_bid = standing_high_bid + minimum_raise`.
- If `min_legal_bid > lot_value` or `min_legal_bid > current_budget`, pass immediately: `[bid: pass]`.
- When `lot_value` comfortably exceeds `min_legal_bid` and budget permits:
  - Competitors consistently bid in the range of 60%–80% of estimate or valuation in the final round. Place a competitive closing bid roughly halfway between the standing bid and my valuation (or ~70–80% of valuation, capped by remaining budget) to beat rival snipes while preserving healthy surplus.
- When margins are tight (`lot_value - min_legal_bid` is small):
  - Bid `min_legal_bid` if `lot_value >= min_legal_bid` and `min_legal_bid <= current_budget`.
  - Otherwise, pass: `[bid: pass]`.

## Formatting
- Always end my response with both explicit tokens on separate lines:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`