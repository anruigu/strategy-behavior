---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 1962
---
### Budget Tracking
- Read the initial budget carefully from the opening instructions of the auction (e.g., budget of 30) and do not assume or revert to 100 on later rounds.
- Track remaining budget precisely across all lots: `current_budget = initial_budget - sum(prices paid for all lots won by bidder 0)`.
- Never submit a bid higher than `current_budget`.
- On every turn, report the exact remaining budget in the token `[budget: current_budget]`.

### Surplus Optimization & Bidding Ceiling
- Absolute bid ceiling for any lot: `ceiling = min(valuation - 1, current_budget)`.
- Bidding `valuation - 1` guarantees only +1 surplus on a win. To capture meaningful profit across the auction, target shaded bids rather than jumping directly to `valuation - 1`:
  - Determine surplus potential `margin = valuation - standing_bid`.
  - In competitive lots, bid enough to beat competitors without giving away all surplus.

### Bid Calculations
- Calculate the minimum allowable bid:
  - If `standing_bid == 0`: `minimum_raise`.
  - If `standing_bid > 0`: `standing_bid + minimum_raise`.
- If `minimum_allowable_bid > ceiling`, output `[bid: pass]` with `[budget: current_budget]`.

### Round-by-Round Strategy
- **Round 1 / 2:**
  - If `minimum_allowable_bid <= ceiling`, bid exactly `minimum_allowable_bid` to stay in the running while keeping prices low.
  - If `minimum_allowable_bid > ceiling`, pass.
- **Round 2 / 2 (Final round for lot):**
  - If bidder 0 holds the standing high bid, pass.
  - If bidding to win:
    - If `minimum_allowable_bid <= ceiling`: place a bid between `minimum_allowable_bid` and `ceiling` that preserves a healthy surplus (e.g., `min(ceiling, standing_bid + 2 * minimum_raise)` or `ceiling` if margin is small).
    - If `ceiling < minimum_allowable_bid`, pass.

### Formatting
- Always conclude each turn with the two exact tokens on separate lines or at the very end:
  - `[bid: N]` or `[bid: pass]`
  - `[budget: current_budget]`