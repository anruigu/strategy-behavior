---
game: ref_auction
model: gemini-flash
condition: win
seed: 5
round: 2
chars: 1422
---
# Auction Playbook

- **Budget Tracking**:
  - Carefully note the starting budget given in the opening prompt (e.g., 30).
  - Explicitly calculate remaining budget before every turn: `Remaining Budget = Starting Budget - Sum(prices of lots won by me so far)`.
  - Never invent, reset, or inflate the budget (e.g., do not hallucinate starting at 100).
  - Never bid an amount higher than my true remaining budget.
  - In each turn, output my exact remaining budget in the `[budget: N]` token.

- **Bidding Rules**:
  - Calculate the minimum required bid: `standing high bid + minimum raise` (or `minimum raise` if standing high bid is 0).
  - Check two hard constraints:
    1. Valuation constraint: `minimum required bid <= my value for the lot` (ensures non-negative surplus).
    2. Budget constraint: `minimum required bid <= true remaining budget`.
  - If either constraint fails, pass:
    - Reply `[bid: pass]` and `[budget: current_remaining_budget]`.
  - If both constraints hold:
    - Bid exactly the minimum required bid (`standing high bid + minimum raise`).
    - In round 2/2, always place this minimum winning bid if it yields positive surplus and fits within budget.

- **Response Format**:
  - Keep reasoning to at most one short sentence or omit reasoning entirely.
  - Always finish the reply with the two required tokens on separate lines:
    ```
    [bid: N]  (or [bid: pass])
    [budget: N]
    ```