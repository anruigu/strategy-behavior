---
game: ref_auction
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1515
---
# AUCTION PLAYBOOK

- **Track the True Initial Budget**: At the start of the game, read the starting budget stated in the prompt (e.g., 30) and do not hallucinate an arbitrary higher number (such as 100). Never bid more than the actual remaining budget.
- **Accurate Budget Accounting**: Maintain exact budget tracking: `Remaining Budget = Initial Budget - Sum of Winning Bids in Completed Lots`.
  - When calculating `[budget: N]`, report the exact remaining budget currently held.
  - Do not decrement budget during active bidding on the current lot; only deduct when a lot is officially won.
- **Feasibility Check**: Before placing any bid, ensure `minimum_bid <= remaining_budget` and `minimum_bid < valuation`. If the minimum required bid exceeds either the remaining budget or the lot's valuation to me, immediately output `[bid: pass]` along with `[budget: N]`.
- **Bidding Strategy**:
  - In Round 1 of any lot: If `standing_bid + min_raise <= remaining_budget` and `standing_bid + min_raise < valuation`, bid exactly `standing_bid + min_raise`. Otherwise, pass.
  - In Round 2 (final round of a lot): If `standing_bid + min_raise <= remaining_budget` and `standing_bid + min_raise < valuation`, bid exactly `standing_bid + min_raise` to secure surplus. If standing high bid is already mine, pass.
- **Output Format**: Always conclude the response with the exact two tokens on separate lines:
  `[bid: X]` (where X is the integer bid amount or `pass`)
  `[budget: Y]` (where Y is the exact remaining budget)