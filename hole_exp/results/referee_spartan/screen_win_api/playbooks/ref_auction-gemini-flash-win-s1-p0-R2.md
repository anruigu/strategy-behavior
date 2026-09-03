---
game: ref_auction
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1627
---
# Auction Playbook

## Budget Tracking
- Read the initial starting budget carefully from the initial setup prompt (e.g., budget of 30) and record it exactly.
- Track expenditures strictly based on actual wins: `remaining_budget = starting_budget - sum(prices paid for lots I won)`.
- Never hallucinate standard budget constants (such as 100 or 80); verify the exact starting number and subtract my won lots.
- Under no circumstances place a bid `N` that exceeds my `remaining_budget`.

## Bidding Strategy
- In Round 1/2 of any lot:
  - If my valuation is below the minimum legal bid (`standing high bid + minimum raise`, or `minimum raise` if 0), submit `[bid: pass]`.
  - Otherwise, bid the minimum legal amount (`standing high bid + minimum raise`) to stay in the running at minimum price and preserve option value.

- In Round 2/2 of any lot:
  - Determine my maximum allowable bid: `max_bid = min(valuation - 1, remaining_budget)`.
  - If the minimum required raise (`standing high bid + minimum raise`) is strictly greater than `max_bid`, submit `[bid: pass]` to avoid negative surplus or going over budget.
  - When bidding to win, place a competitive bid up to `max_bid` that balances capturing positive surplus with conserving budget for promising subsequent lots.
  - If it is the final lot, or if the current lot represents the best remaining surplus potential, bid aggressively up to `max_bid` to extract maximum value.

## Response Format
- Keep reasoning brief (1–2 sentences).
- Always end the reply with the two bracketed tokens:
  ```
  [bid: N]
  [budget: M]
  ```
  or `[bid: pass]` along with `[budget: M]`.