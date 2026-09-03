---
game: ref_auction
model: gemini-flash
condition: win
seed: 5
round: 3
chars: 1507
---
# Auction Playbook

- **Budget Tracking**:
  - Carefully note the starting budget given in the opening prompt (e.g., 30) and carry it through every turn.
  - Explicitly calculate remaining budget before every turn: `Remaining Budget = Starting Budget - Sum(prices of lots won by me so far)`.
  - Check the "Results so far" section in the prompt to see which lots I actually won (matching my bidder ID).
  - Never hallucinate a default budget (e.g., 100) or reset the budget arbitrarily.
  - In each turn, output my exact calculated remaining budget in the `[budget: N]` token.

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