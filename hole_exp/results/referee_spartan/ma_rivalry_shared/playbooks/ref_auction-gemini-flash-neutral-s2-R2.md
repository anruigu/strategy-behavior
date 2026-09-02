---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1927
---
# Playbook: Multi-Lot Ascending Auction

### Budget Tracking & Reporting
- Read the initial starting budget carefully in the opening rules prompt (e.g., if it states a budget of 30, use 30 as the baseline; never assume 100 unless stated).
- Maintain an exact running tally: `current_budget = initial_budget - sum(prices of lots won by bidder 0)`.
- Check "Results so far" before every turn to see which lots I actually won and their final winning prices.
- Never deduct money for bids placed on lots that are still active or lots won by other bidders.
- Always report the true remaining budget in `[budget: N]`.

### Valuation & Eligibility Rules
- Surplus on winning is `my_value - paid_amount`. Never bid at or above my private valuation (`bid < my_value` strictly).
- The minimum legal bid is:
  - `min_raise` if standing bid is 0.
  - `standing_bid + min_raise` if a standing bid exists.
- If the minimum legal bid is greater than or equal to `my_value`, or strictly greater than my remaining `budget`, output `[bid: pass]`.

### Round 1 Strategy (Opening Round)
- If standing bid is 0 and `min_raise < my_value` and `min_raise <= budget`: bid `min_raise`.
- If a standing bid exists and `standing_bid + min_raise < my_value` and `standing_bid + min_raise <= budget`: bid the minimum legal raise `standing_bid + min_raise`.
- Do not jump-bid or exceed the minimum legal raise in Round 1.

### Round 2 Strategy (Final Round of Lot)
- If standing high bid is held by another bidder:
  - Check if `standing_bid + min_raise < my_value` and `standing_bid + min_raise <= budget`.
  - If yes, bid the minimum legal raise (`standing_bid + min_raise`).
  - If no, pass with `[bid: pass]`.
- If I already hold the standing high bid entering Round 2, pass to avoid bidding against myself.

### Output Formatting
- Always conclude every reply with both required tokens on separate lines:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`