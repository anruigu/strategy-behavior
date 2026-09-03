---
game: ref_auction
model: gemini-flash
condition: win
seed: 6
round: 3
chars: 1943
---
# Playbook for Ref Auction

- **Budget Tracking**:
  - Read the exact starting budget stated in the initial prompt at the start of the auction (e.g., if told budget is 30, track strictly down from 30; never assume a default 100).
  - Explicitly calculate remaining budget before every bid: `remaining_budget = initial_budget - sum(prices of lots won so far by me)`.
  - Always report the true remaining budget in `[budget: N]` with every action, even when passing.

- **Valuation and Budget Constraints**:
  - Maximum allowable bid is `min(valuation - 1, remaining_budget)` to guarantee strictly positive surplus.
  - Never place a bid higher than the lot's value to me.
  - Never place a bid higher than my remaining budget.
  - If the minimum legal bid (`standing high bid + minimum raise`) exceeds either `valuation - 1` or `remaining_budget`, output `[bid: pass]`.

- **Round 1 Strategy (Opening / Early Round)**:
  - If `valuation > minimum legal bid` and `remaining_budget >= minimum legal bid`, place the minimum legal bid (`standing high bid + minimum raise`, or `minimum raise` if standing bid is 0).
  - Never jump-bid in Round 1; keep the price as low as possible.
  - If the lot value is below or equal to the minimum opening bid, pass immediately.

- **Round 2 Strategy (Final Round)**:
  - Determine minimum required bid: `min_bid = standing_high_bid + minimum_raise`.
  - If `min_bid > min(valuation - 1, remaining_budget)`, output `[bid: pass]`.
  - If eligible to bid:
    - If standing bid is held by an opponent, bid the minimum necessary amount (`min_bid`) up to `min(valuation - 1, remaining_budget)` to secure positive surplus while leaving budget for subsequent lots.
    - If I already hold the standing high bid entering Round 2, pass to avoid bidding against myself.

- **Output Format**:
  - Always include brief reasoning followed immediately by the exact tokens:
    `[bid: N]` (or `[bid: pass]`)
    `[budget: N]`