---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1100
---
### Budget Tracking
- At the start of the auction, initialize remaining budget to the starting amount stated in the prompt (e.g., 30 or 100). Never guess a default budget of 100 if a different starting budget is given.
- When winning a lot, subtract the winning price from the remaining budget before the next lot starts.
- When reporting `[budget: N]`, report the exact current remaining budget (starting budget minus sum of winning prices of lots won so far). Do not deduct bids placed on active, unresolved lots.

### Bidding Strategy
- Calculate the minimum legal bid as `standing high bid + minimum raise`.
- If the lot's value to me is strictly greater than the minimum legal bid AND the minimum legal bid is less than or equal to my remaining budget:
  - Bid exactly the minimum legal bid `standing high bid + minimum raise`.
- If the minimum legal bid is greater than or equal to my valuation, or exceeds my remaining budget:
  - Output `[bid: pass]`.
- Always conclude every response with the required format:
  ```
  [bid: N]
  [budget: B]
  ```
  or
  ```
  [bid: pass]
  [budget: B]
  ```