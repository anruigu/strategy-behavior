---
game: ref_auction
model: gemini-flash
condition: win
seed: 4
round: 1
chars: 1828
---
# Playbook: Open Ascending Multi-Lot Auction

## Budget Accounting
- When starting the game, record the initial budget given in the prompt (do not assume a default number like 100).
- When reporting `[budget: N]`, calculate `N` strictly as: `initial_budget - sum_of_winning_bids_I_paid_so_far`.
- Never place a bid that exceeds my current remaining budget.

## Bidding Strategy per Lot

### Round 1/2
- When opening or raising on a lot I want to contest, bid the minimum legal amount (`standing_high_bid + minimum_raise`, or simply `minimum_raise` if standing bid is 0).
- Do not jump-bid in round 1; keep the price floor low to preserve room for round 2.
- If the minimum legal bid exceeds my valuation for the lot or exceeds my remaining budget, output `[bid: pass]`.

### Round 2/2 (Final Round for the Lot)
- If I am already the standing high bidder:
  - Output `[bid: pass]` to avoid bidding against myself.
- If I am not the standing high bidder:
  - Check whether a competitive raise (`standing_high_bid + minimum_raise` or a calculated jump) is $\le \min(\text{valuation} - 1, \text{budget})$.
  - If it is profitable and affordable, place a bid that maximizes my chance to win while locking in positive surplus ($\text{bid} < \text{valuation}$). On highly valued lots, bid higher than the minimum raise to beat competing snipes, provided $\text{bid} \le \text{valuation} - \text{margin}$ and $\text{bid} \le \text{budget}$.
  - If `standing_high_bid + minimum_raise` $\ge \text{valuation}$ or exceeds my remaining budget, output `[bid: pass]`.

## Budget Allocation Across Lots
- Prioritize lots with the highest potential surplus ($\text{valuation} - \text{estimate}$).
- When budget is constrained relative to remaining lots, pass on marginal lots with low surplus margins to save budget for upcoming high-value lots.