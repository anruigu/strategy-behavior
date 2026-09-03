---
game: ref_auction
model: gemini-flash
condition: win
seed: 6
round: 1
chars: 1747
---
# Playbook: Open Ascending Multi-Lot Auction

- **Budget Tracking**: 
  - Start with the exact starting budget given in the game introduction.
  - In every reply, explicitly calculate and report `[budget: current_balance]`.
  - When I win a lot, subtract the winning price from my budget balance before making any subsequent bids. Never hallucinate or reset the budget to an arbitrary number.

- **Bid Limits & Constraints**:
  - Never place a bid that exceeds my private valuation for the current lot.
  - Never place a bid that exceeds my remaining available budget balance.
  - If the required minimum bid (`standing high bid + minimum raise`) is greater than either my valuation or my remaining budget, output `[bid: pass]`.

- **Round 1 Strategy (Opening/Contention)**:
  - If the standing high bid is 0, bid the minimum opening amount (`minimum raise`), provided it is strictly below my valuation and within budget.
  - If another bidder holds the standing high bid and it is below my valuation, raise by the minimum raise increment to stay in contention cheaply.

- **Round 2 Strategy (Final Round of a Lot)**:
  - Calculate my ceiling: `limit = min(valuation - 1, current_budget)`.
  - If the minimum required raise (`standing high bid + minimum raise`) exceeds `limit`, output `[bid: pass]`.
  - If the minimum required raise is less than or equal to `limit`, bid competitively up toward my limit—especially on valuable lots or later rounds—rather than just making the minimal raise, to prevent opponents from outbidding me with small increments while still locking in positive surplus.

- **Formatting**:
  - Always end every prompt response with exactly two tokens on their own lines:
    `[bid: N]` (or `[bid: pass]`)
    `[budget: N]`