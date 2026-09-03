---
game: ref_auction
model: gemini-flash
condition: win
seed: 6
round: 3
chars: 1721
---
# Playbook: Open Ascending Multi-Lot Auction

- **Budget Tracking**:
  - Read the exact starting budget stated in the opening prompt (e.g., 30) and strictly track it across every round. Never reset or default to any arbitrary number (e.g., 100).
  - Explicitly calculate `current_budget = starting_budget - total_spent_on_won_lots` before generating any reply.
  - If `current_budget <= 0`, I cannot place any positive bids and must pass for all remaining lots.
  - In every reply, output the exact balance: `[budget: current_budget]`.

- **Bid Limits & Constraints**:
  - Absolute cap for any bid on a lot: `cap = min(valuation - 1, current_budget)`.
  - Never place a bid that exceeds `cap` or `current_budget` under any circumstance.
  - Minimum required bid to enter or raise:
    - If standing high bid is 0: `min_bid = minimum_raise`.
    - If standing high bid > 0: `min_bid = standing_high_bid + minimum_raise`.
  - If `min_bid > cap`, output `[bid: pass]`.

- **Round 1 Strategy (Opening / Early Round)**:
  - If I am already the standing high bidder, pass.
  - If `min_bid <= cap`, bid exactly `min_bid`.
  - Otherwise, pass.

- **Round 2 Strategy (Final Round of a Lot)**:
  - If I am already the standing high bidder:
    - Pass if my current bid is safe, or consider standing pat to avoid overpaying.
  - If I am not the standing high bidder:
    - If `min_bid > cap`, output `[bid: pass]`.
    - If `min_bid <= cap`, place a strong bid at `cap` (or up to `cap`) to maximize win probability while guaranteeing surplus $\ge 1$ and staying within budget.

- **Formatting**:
  - Always conclude every prompt response with exactly two tokens on separate lines:
    `[bid: N]` (or `[bid: pass]`)
    `[budget: N]`