---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1051
---
### Budget Tracking
- Read the opening prompt carefully for the initial starting budget (e.g., 30 or 100). Never assume 100 or hallucinate a new starting budget later.
- Track budget accurately across all rounds: `remaining budget = starting budget - sum(prices paid for won lots listed under Results so far)`.
- Active bids in an ongoing lot do not reduce the reported remaining budget until the lot is won and concluded.
- In every single reply, state the exact calculated remaining budget in `[budget: N]`.

### Bidding Strategy
- Calculate the minimum legal bid: `min_bid = standing high bid + minimum raise`.
- If `min_bid <= lot value to me` AND `min_bid <= remaining budget`:
  - Bid `min_bid` using `[bid: min_bid]`.
- If `min_bid > lot value to me` OR `min_bid > remaining budget`:
  - Pass using `[bid: pass]`.

### Response Format
- Keep any accompanying reasoning brief (1–2 sentences).
- Always end the response with the exact two tokens on separate lines:
  ```
  [bid: N]
  [budget: B]
  ```
  or
  ```
  [bid: pass]
  [budget: B]
  ```