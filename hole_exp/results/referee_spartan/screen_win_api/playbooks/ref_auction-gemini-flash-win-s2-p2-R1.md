---
game: ref_auction
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1288
---
# Auction Strategy & Playbook

- **Budget Tracking**:
  - Always track remaining budget starting from the initial budget given in the game setup.
  - When reporting `[budget: N]`, subtract the winning price of each previously won lot from the true starting budget. Never hallucinate an inflated starting budget (e.g., jumping to 100).
  - Ensure any bid `B` satisfies `B <= remaining_budget`.

- **Bidding Decision Rules**:
  - Compute the minimum valid raise: `min_bid = standing_high_bid + minimum_raise` (or `minimum_raise` if no standing bids).
  - If `min_bid > lot_value` or `min_bid > remaining_budget`:
    - Output `[bid: pass]`.
  - If `min_bid <= lot_value` and `min_bid <= remaining_budget`:
    - In Round 1/2: Bid exactly `min_bid` to stay in the lot cheaply while observing competition.
    - In Round 2/2: Bid exactly `min_bid` if `min_bid < lot_value` to extract positive surplus (`surplus = lot_value - min_bid`). If `min_bid == lot_value` (zero surplus), pass to conserve budget for higher-margin future lots unless it is the final lot and no better opportunities remain.

- **Response Formatting**:
  - Keep reasoning strictly to 1–2 sentences.
  - Always terminate responses with the exact bracketed tags:
    ```
    [bid: N] (or [bid: pass])
    [budget: N]
    ```