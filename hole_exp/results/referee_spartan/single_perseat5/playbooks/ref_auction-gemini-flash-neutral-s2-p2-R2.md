---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 976
---
### Budget Tracking
- Read the opening prompt carefully for the initial starting budget (e.g., 30). Do not assume 100 or any default value.
- Maintain an exact running total of remaining budget: `remaining budget = starting budget - sum(prices paid for won lots)`.
- Do not deduct active bids from the remaining budget during an ongoing lot; only deduct settled winning bids from completed lots.
- In every round, report the exact remaining budget in `[budget: N]`, even in round 2 of lot 1 or subsequent lots.

### Bidding Strategy
- Calculate the minimum legal bid: `min_bid = standing high bid + minimum raise`.
- If `min_bid <= lot value` AND `min_bid <= remaining budget`:
  - Place a bid equal to `min_bid`.
- If `min_bid > lot value` OR `min_bid > remaining budget`:
  - Output `[bid: pass]`.

### Response Format
- Always finish the response with the exact two tokens on separate lines:
  ```
  [bid: N]
  [budget: B]
  ```
  or
  ```
  [bid: pass]
  [budget: B]
  ```