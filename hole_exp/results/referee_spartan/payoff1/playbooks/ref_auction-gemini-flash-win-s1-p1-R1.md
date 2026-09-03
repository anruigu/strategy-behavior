---
game: ref_auction
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1763
---
# Playbook for ref_auction

- **Budget Tracking**:
  - Read the exact starting budget stated in the initial prompt and do not assume a default value (like 100).
  - Track my remaining budget strictly: `current_budget = initial_budget - sum(winning_bids_won_so_far)`.
  - Always report this exact calculated remaining budget in the `[budget: N]` token on every turn, regardless of whether my bid succeeds or I pass.
  - Never bid an amount greater than my remaining budget.

- **Valuation and Profit Ceiling**:
  - Never bid at or above my private valuation for a lot.
  - Always calculate maximum allowable bid as `min(budget_left, private_value - 1)`.

- **Bidding in Round 1/2**:
  - If standing high bid is 0 and minimum raise is strictly less than my private value, bid the minimum raise (`[bid: min_raise]`).
  - If standing high bid > 0 and `standing_bid + min_raise < private_value`, bid `standing_bid + min_raise`.
  - If `standing_bid + min_raise >= private_value` or exceeds remaining budget, pass (`[bid: pass]`).

- **Bidding in Round 2/2 (Final Round)**:
  - Check the standing high bid. If I am already the standing high bidder, pass (`[bid: pass]`) to avoid bidding against myself.
  - If another bidder leads, calculate required minimum raise: `required_bid = standing_bid + min_raise`.
  - If `required_bid < private_value` and `required_bid <= budget_left`, bid `required_bid` (or a slightly higher jump bid if surplus is very high and budget allows, but keep `bid < private_value`).
  - If `required_bid >= private_value` or `required_bid > budget_left`, pass (`[bid: pass]`).

- **Formatting**:
  - Ensure every response strictly concludes with both `[bid: N]` (or `[bid: pass]`) and `[budget: N]` using the actual calculated remaining budget.