---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1538
---
### Budget Management & Token Tracking
- Read the initial budget carefully from the opening instructions and track it strictly. Do not hallucinate a default budget (e.g., 100) on later rounds.
- Track remaining budget precisely: `current_budget = initial_budget - sum(prices of lots won by bidder 0)`.
- On every turn, report the exact remaining budget in the token `[budget: current_budget]`.
- Never place a bid that exceeds `current_budget`.

### Bidding Rules & Limits
- Calculate the minimum allowable bid:
  - If `standing_bid == 0`: `minimum_raise`.
  - If `standing_bid > 0`: `standing_bid + minimum_raise`.
- Determine the maximum allowable bid: `max_bid = min(valuation - 1, current_budget)`.
- If `minimum_allowable_bid > max_bid`, output `[bid: pass]` along with `[budget: current_budget]`.

### Round-by-Round Strategy
- **Round 1 / 2:**
  - If `minimum_allowable_bid <= max_bid`, bid exactly `minimum_allowable_bid`.
  - Never jump-bid in Round 1; keep prices as low as possible going into the final round.
- **Round 2 / 2 (Final round for lot):**
  - If already holding the standing high bid and nobody raised, pass to avoid bidding against myself.
  - If raising or placing a new bid: bid `max_bid = min(valuation - 1, current_budget)` provided `max_bid >= minimum_allowable_bid`, to maximize win probability and lock in positive surplus.
  - If `max_bid < minimum_allowable_bid`, pass.

### Formatting
- Always end responses with both exact bracketed tokens:
  - `[bid: N]` or `[bid: pass]`
  - `[budget: current_budget]`