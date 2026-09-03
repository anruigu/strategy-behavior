---
game: ref_auction
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1453
---
# Auction Playbook

## Budget Tracking
- Read the initial starting budget from the setup message and track it accurately across all rounds.
- When reporting `[budget: N]`, calculate `N` strictly as `starting_budget - total_spent_on_won_lots`. Never hallucinate or default to arbitrary numbers like 100.
- Never place a bid `B` greater than my currently remaining budget `N`.

## Bidding Strategy
- In Round 1/2 of any lot:
  - If my valuation is below the minimum opening bid, submit `[bid: pass]`.
  - Otherwise, bid the minimum legal amount (`standing high bid + minimum raise`, or `minimum raise` if no bids exist) to remain active at minimal cost.

- In Round 2/2 of any lot:
  - Calculate my surplus ceiling: `max_bid = min(valuation - 1, remaining_budget)`.
  - If `standing high bid + minimum raise > max_bid`, submit `[bid: pass]` rather than overpaying or exceeding budget.
  - If there is room for positive surplus, bid aggressively enough to win the lot rather than just placing the minimum increment, provided the bid does not exceed `max_bid` and leaves sufficient budget for higher-value future lots.
  - On the final lot or high-margin opportunities where no better lots remain, bid up to `max_bid` to capture all remaining positive surplus.

## Response Format
- Keep reasoning brief (1–2 sentences).
- Always end with exactly the two required tokens on separate lines:
  ```
  [bid: N]
  [budget: M]
  ```
  or `[bid: pass]` if passing.