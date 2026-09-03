---
game: ref_auction
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1505
---
# Auction Strategy & Playbook

- **Budget Tracking**:
  - Always track remaining budget accurately starting from the initial budget specified in the game setup (e.g., if starting with 30, never jump to 100).
  - Explicitly calculate `remaining_budget = initial_budget - sum(prices paid for lots won so far)`.
  - When reporting `[budget: N]`, output the current `remaining_budget` at the moment of the bid (do not deduct the current bid before winning the lot; only deduct completed wins).
  - Ensure any active bid `B` strictly satisfies `B <= remaining_budget`.

- **Bidding Decision Rules**:
  - Compute the minimum valid bid: `min_bid = standing_high_bid + minimum_raise` (or the minimum opening bid if no standing bid).
  - If `min_bid > lot_value` or `min_bid > remaining_budget`:
    - Output `[bid: pass]`.
  - If `min_bid <= lot_value` and `min_bid <= remaining_budget`:
    - In Round 1/2: Bid exactly `min_bid` to stay in contention cheaply.
    - In Round 2/2: Bid exactly `min_bid` if `min_bid < lot_value` to secure positive surplus (`surplus = lot_value - min_bid`). If `min_bid == lot_value` (zero surplus), pass to conserve budget for future positive-surplus lots unless it is the final lot.

- **Response Formatting**:
  - Keep reasoning strictly to 1–2 brief sentences verifying arithmetic (budget, minimum raise, valuation).
  - Always terminate responses with the exact bracketed tags on their own lines:
    ```
    [bid: N]
    [budget: N]
    ```
    (or `[bid: pass]` if passing).