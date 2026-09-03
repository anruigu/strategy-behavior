---
game: ref_auction
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1637
---
# Playbook for Ref Auction

- **Budget Tracking**:
  - Read the exact starting budget given in the opening prompt (do not assume a default like 100).
  - Track my remaining budget as `starting_budget - sum(prices of lots I have won)`.
  - Always report my actual calculated remaining budget in `[budget: N]`, never a fabricated number.

- **Bid Feasibility and Budget Constraints**:
  - Never place a bid `N` that exceeds my remaining budget (`N <= remaining_budget`).
  - Never place a bid `N` that equals or exceeds the lot's value to me (`N < value`).
  - Ensure any bid `N` satisfies the minimum raise requirement: `N >= standing_high_bid + minimum_raise` (or `N >= minimum_raise` if there are no bids yet).

- **Bidding Strategy by Round**:
  - **Round 1/2**:
    - If standing high bid + minimum raise < lot value and within remaining budget: place a bid at or near the minimum valid raise to remain active and gauge competition cheaply. Do not make unnecessarily large jump bids.
    - If the minimum valid raise exceeds my valuation or my budget: reply `[bid: pass]` along with my current budget.
  - **Round 2/2 (Final Round of Lot)**:
    - If `standing_high_bid + minimum_raise < value` and `standing_high_bid + minimum_raise <= remaining_budget`: bid exactly `standing_high_bid + minimum_raise` to maximize surplus while ensuring a valid winning attempt.
    - If the required minimum raise is greater than or equal to my valuation or exceeds my budget: reply `[bid: pass]` along with my current budget.

- **Formatting**:
  - Always end every reply with both explicit tokens: `[bid: N]` (or `[bid: pass]`) and `[budget: N]`.