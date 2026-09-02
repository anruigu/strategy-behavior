---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 4
round: 1
chars: 1548
---
# Playbook for Ref Auction

### Budget Tracking & Reporting
- Read the starting budget explicitly from the game prompt (e.g., 30 or 100) and track it locally.
- In every reply, calculate `remaining_budget = starting_budget - total_spent_on_won_lots`. Never hallucinate or reset the budget to an arbitrary baseline between rounds.
- Always output `[budget: remaining_budget]` using the exact tracked remainder.

### Bidding Strategy & Thresholds
- On Round 1:
  - If the lot is worth significantly more than the minimum bid, make the minimum valid opening raise (`standing_high_bid + minimum_raise`, or simply `minimum_raise` if no standing bid).
  - Do not place large jump bids in Round 1; keep the price low to leave room for profit.
- On Round 2 (Final Round):
  - Calculate `next_min_bid = standing_high_bid + minimum_raise`.
  - If `next_min_bid <= value` and `next_min_bid <= remaining_budget`: bid exactly `next_min_bid` to maximize surplus.
  - Do not place aggressive, unnecessary jump bids far above the minimum required raise in Round 2; it only reduces surplus without adding strategic value.
  - If `next_min_bid > value` or `next_min_bid > remaining_budget`: output `[bid: pass]`. Never bid equal to or above valuation when it yields zero or negative profit.

### Budget Preservation Across Lots
- Prioritize high-margin lots (large positive gap between value and estimate/standing bid).
- If remaining budget is limited, pass on marginal lots (surplus < 3) to preserve capital for potentially higher-value lots later in the sequence.