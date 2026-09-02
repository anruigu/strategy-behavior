---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1702
---
# Auction Playbook

## Budget Tracking and Integrity
- Always initialize my tracked budget to the exact starting budget stated in the initial prompt (e.g., 30 or 100), and never hardcode 100 unless that is what the game explicitly started with.
- Track my remaining budget across lots strictly: `current_budget = starting_budget - sum(prices of lots won by bidder 1)`.
- State `[budget: current_budget]` accurately in every reply without deducting unconfirmed bids or pending offers from the active round.

## Bidding Strategy per Round

### Round 1 / 2 (Opening / Mid-Round)
- If the lot's value to me is below the minimum opening/raise requirement, pass immediately: `[bid: pass]`.
- Otherwise, always bid the absolute minimum legal amount (`standing_high_bid + minimum_raise`, or simply `minimum_raise` if standing bid is 0) to avoid unnecessarily inflating the price for round 2.
- Never place high opening jump-bids in round 1; keep the price low.

### Round 2 / 2 (Final Round for Lot)
- Calculate `min_legal_bid = standing_high_bid + minimum_raise`.
- If `min_legal_bid > lot_value` or `min_legal_bid > current_budget`, pass immediately: `[bid: pass]`.
- On high-value lots where valuation substantially exceeds the standing bid, do not merely raise by the minimum increment if competitors frequently snipe by small margins; place a competitive bid that captures substantial surplus while staying safely within `current_budget` and strictly below `lot_value`.
- On low-margin lots, bid exactly `min_legal_bid` if `lot_value - min_legal_bid >= 1`, otherwise pass.

## Formatting
- Always end my response with both explicit tokens on separate lines:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`