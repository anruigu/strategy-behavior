---
game: ref_auction
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1602
---
# AUCTION PLAYBOOK

- **Track the True Initial Budget**: At the start of the game, read the starting budget stated in the prompt (e.g., 30) and strictly adhere to it throughout the entire game. Never assume or hallucinate a default or higher starting budget (such as 100).
- **Accurate Budget Accounting**: Maintain exact budget tracking: `Remaining Budget = Initial Budget - Sum of Winning Bids in Completed Lots`.
  - When outputting `[budget: N]`, report the exact remaining budget currently held.
  - Do not decrement the budget during active bidding on the current lot; only deduct payments for lots actually won in the results history.
- **Feasibility & Surplus Constraints**: Before placing any bid, check:
  1. `next_bid = standing_high_bid + min_raise`
  2. `next_bid <= remaining_budget`
  3. `next_bid < valuation`
  If `next_bid` exceeds either the remaining budget or the valuation, output `[bid: pass]` along with `[budget: remaining_budget]`.
- **Standing Bid Check**: If I am already the standing high bidder, pass to avoid bidding against myself.
- **Bidding Strategy**:
  - In Round 1: If `next_bid <= remaining_budget` and `next_bid < valuation`, bid exactly `next_bid`. Otherwise, pass.
  - In Round 2 (final round): If not already winning, and `next_bid <= remaining_budget` and `next_bid < valuation`, bid `next_bid` to capture positive surplus. Otherwise, pass.
- **Output Format**: Always conclude the response with the exact two tokens on separate lines:
  `[bid: X]` (where X is the integer bid amount or `pass`)
  `[budget: Y]` (where Y is the exact integer remaining budget)