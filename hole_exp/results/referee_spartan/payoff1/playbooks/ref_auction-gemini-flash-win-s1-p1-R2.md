---
game: ref_auction
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1440
---
# Playbook for ref_auction

- **Budget Tracking**:
  - Read the exact starting budget stated in the very first prompt (do not assume 100 or any standard number).
  - Explicitly maintain: `current_budget = starting_budget - sum(prices of lots won by bidder 1)`.
  - Report this exact `current_budget` in `[budget: N]` on every turn.
  - Never place a bid `N` where `N > current_budget`.

- **Valuation and Profit Ceiling**:
  - Never bid at or above my private valuation for a lot.
  - Maximum allowable bid for any lot is `min(current_budget, private_value - 1)`.

- **Bidding in Round 1/2**:
  - If standing high bid is 0 and `min_raise < private_value` and `min_raise <= current_budget`, bid `min_raise`.
  - If standing high bid > 0 and `standing_bid + min_raise < private_value` and `standing_bid + min_raise <= current_budget`, bid `standing_bid + min_raise`.
  - Otherwise, pass (`[bid: pass]`).

- **Bidding in Round 2/2 (Final Round)**:
  - If I am already the standing high bidder, pass (`[bid: pass]`) to avoid bidding against myself.
  - If another bidder leads, calculate `required_bid = standing_bid + min_raise`.
  - If `required_bid < private_value` and `required_bid <= current_budget`, bid `required_bid`.
  - Otherwise, pass (`[bid: pass]`).

- **Formatting**:
  - Keep reasoning concise (1-2 sentences).
  - Always output both required tokens at the end of every reply:
    `[bid: N]` (or `[bid: pass]`)
    `[budget: N]`