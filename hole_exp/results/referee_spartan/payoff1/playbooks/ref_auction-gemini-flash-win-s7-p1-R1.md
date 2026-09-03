---
game: ref_auction
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 1611
---
# Ref Auction Playbook

- **Budget Tracking:**
  - Track my exact remaining budget after every won lot: `remaining_budget = initial_budget - sum(winning_prices_of_my_won_lots)`.
  - Never hallucinate a default or reset budget (e.g., jumping to 100); always output `[budget: remaining_budget]` accurately based on the initial starting amount and subsequent payments.
  - Never bid an amount higher than my current remaining budget.

- **Bidding Rules & Valuation Limits:**
  - Calculate my surplus ceiling for every lot: `max_bid = min(remaining_budget, valuation - 1)`.
  - If the required minimum bid (`standing_high_bid + minimum_raise` or `minimum_raise` if no standing bid) exceeds `max_bid`, immediately output `[bid: pass]`. Never bid equal to or above my valuation.
  - On Round 1:
    - If no standing bid exists and `minimum_raise <= max_bid`, bid the minimum raise (`[bid: minimum_raise]`).
    - If a standing bid exists and `standing_high_bid + minimum_raise <= max_bid`, raise by the exact minimum increment: `[bid: standing_high_bid + minimum_raise]`.
    - Otherwise, pass.
  - On Round 2 (Final Round for the lot):
    - If I am already the standing high bidder, pass to avoid bidding against myself.
    - If I am not the standing high bidder and `standing_high_bid + minimum_raise <= max_bid`, bid the minimum required raise: `[bid: standing_high_bid + minimum_raise]`.
    - Otherwise, pass.

- **Response Formatting:**
  - Always keep reasoning to one short sentence.
  - Always end strictly with the two required tokens on separate lines:
    `[bid: N]` (or `[bid: pass]`)
    `[budget: N]`