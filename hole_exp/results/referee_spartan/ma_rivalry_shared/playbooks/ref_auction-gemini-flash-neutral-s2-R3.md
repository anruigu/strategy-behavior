---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 2018
---
# Playbook: Multi-Lot Ascending Auction

### Budget Tracking & Reporting
- Read the initial starting budget carefully in the opening rules prompt (e.g., if it states a budget of 30, use 30 as the baseline; never assume 100).
- Maintain an exact running tally: `current_budget = initial_budget - sum(prices of lots won by bidder 0)`.
- Check "Results so far" before every turn to confirm which lots I actually won (bidder 0) and the exact prices paid.
- Do not deduct money for bids placed on active lots or lots won by other bidders.
- Always report the true remaining budget consistently across all rounds in `[budget: N]`.

### Valuation & Eligibility Rules
- Surplus on winning is `my_value - paid_amount`. Always ensure positive surplus: never bid at or above my private valuation (`bid < my_value` strictly).
- The minimum legal bid is:
  - `min_raise` if standing bid is 0.
  - `standing_bid + min_raise` if a standing bid exists.
- If the minimum legal bid is `>= my_value` or `> current_budget`, output `[bid: pass]`.

### Round 1 Strategy (Opening Round)
- If standing bid is 0: bid `min_raise` provided `min_raise < my_value` and `min_raise <= current_budget`.
- If a standing bid exists: bid `standing_bid + min_raise` provided `standing_bid + min_raise < my_value` and `standing_bid + min_raise <= current_budget`.
- Otherwise, pass with `[bid: pass]`.
- Always stick to the minimum legal raise; never jump-bid in Round 1.

### Round 2 Strategy (Final Round of Lot)
- If I already hold the standing high bid entering Round 2, pass (`[bid: pass]`) to avoid bidding against myself.
- If another bidder holds the standing high bid:
  - Check if `standing_bid + min_raise < my_value` and `standing_bid + min_raise <= current_budget`.
  - If yes, bid `standing_bid + min_raise`.
  - If no, pass with `[bid: pass]`.

### Output Formatting
- Keep reasoning concise (1-2 sentences).
- End every reply with exactly the two required bracketed tokens on separate lines:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`