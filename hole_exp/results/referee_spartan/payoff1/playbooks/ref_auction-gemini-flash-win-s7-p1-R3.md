---
game: ref_auction
model: gemini-flash
condition: win
seed: 7
round: 3
chars: 1592
---
# Ref Auction Playbook

- **Budget Tracking:**
  - Read the exact starting budget stated in the opening prompt (e.g. 30, not an assumed 100).
  - Explicitly calculate and maintain my remaining budget across every round: `remaining_budget = starting_budget - sum(prices_of_lots_won_by_me)`.
  - Always output my accurate `[budget: remaining_budget]` in every single response. Never report a hallucinated or unadjusted budget like 100.
  - Never place a bid higher than my current `remaining_budget`.

- **Valuation & Bid Calculation:**
  - Calculate my maximum permissible bid for any lot: `max_bid = min(remaining_budget, valuation - 1)`.
  - Determine the required minimum legal bid:
    - If `standing_high_bid == 0`: required bid is `minimum_raise`.
    - If `standing_high_bid > 0`: required bid is `standing_high_bid + minimum_raise`.
  - If the required minimum bid exceeds `max_bid`, output `[bid: pass]`. Never bid equal to or above my valuation.

- **Round Execution:**
  - Round 1/2:
    - If required bid `<= max_bid`, bid the required minimum increment: `[bid: required_bid]`.
    - Otherwise, pass.
  - Round 2/2:
    - If I am already the standing high bidder, pass (`[bid: pass]`) to avoid driving up the price or outbidding myself.
    - If another bidder holds the standing high bid and required bid `<= max_bid`, bid the minimum increment: `[bid: required_bid]`.
    - Otherwise, pass.

- **Response Formatting:**
  - Keep reasoning brief (one sentence).
  - Always conclude with the two required tokens on separate lines:
    `[bid: N]` (or `[bid: pass]`)
    `[budget: N]`