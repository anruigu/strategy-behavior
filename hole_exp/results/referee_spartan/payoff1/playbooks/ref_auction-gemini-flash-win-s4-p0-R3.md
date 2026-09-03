---
game: ref_auction
model: gemini-flash
condition: win
seed: 4
round: 3
chars: 2279
---
# Playbook: Open Ascending Multi-Lot Auction

## Budget Accounting
- Read and strictly record the initial budget explicitly stated in the game setup prompt on turn 1 (e.g., if prompt states budget is 30, do not assume 100).
- When reporting `[budget: N]`, calculate `N` strictly as: `initial_budget - sum_of_winning_bids_I_paid_so_far`.
- Track won lots exclusively from the `Results so far:` block (where `bidder 0 won at X`).
- Never place a bid that exceeds my current remaining budget (`bid <= remaining_budget`).
- Ensure `[budget: N]` in the output tag accurately matches this calculation on every single turn.

## Valuation & Surplus Discipline
- My score is `total_valuation_won - total_paid`.
- Always maintain positive surplus: never bid equal to or greater than my private valuation (`bid < valuation`).
- Maximum allowable bid on any lot is $\min(\text{valuation} - 1, \text{remaining\_budget})$.

## Bidding Strategy per Lot

### Round 1/2
- If the minimum legal bid (`standing_high_bid + minimum_raise`, or `minimum_raise` if standing bid is 0) is $\le \min(\text{valuation} - 1, \text{remaining\_budget})$:
  - Place the minimum legal bid to enter the auction while keeping prices low.
- If the minimum legal bid exceeds my valuation or remaining budget:
  - Output `[bid: pass]`.

### Round 2/2 (Final Round for the Lot)
- If I am already the standing high bidder:
  - Output `[bid: pass]` to avoid bidding against myself.
- If I am not the standing high bidder:
  - Determine the minimum legal raise: `min_legal = standing_high_bid + minimum_raise`.
  - If `min_legal > valuation - 1` or `min_legal > remaining_budget`:
    - Output `[bid: pass]`.
  - Otherwise, choose a winning bid $B$ such that $\text{min\_legal} \le B \le \min(\text{valuation} - 1, \text{remaining\_budget})$.
    - For lots with high potential surplus, place a decisive bid above the minimum raise to fend off competitor counter-bids, while ensuring a healthy profit margin is preserved.

## Budget Allocation Across Lots
- Monitor total remaining lots and prioritize preserving budget for lots with high absolute potential surplus ($\text{valuation} - \text{estimate}$).
- Pass on low-margin or unfavorable lots if spending would starve bidding power for later high-surplus opportunities.