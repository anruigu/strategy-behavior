---
game: ref_auction
model: gemini-flash
condition: win
seed: 7
round: 3
chars: 1434
---
# Ref Auction Playbook

- **Budget Tracking**:
  - Always read the initial budget strictly from the opening prompt text (e.g., if starting with 30, never default or drift to 100 in later rounds).
  - Explicitly calculate and maintain the exact remaining budget at every round: `remaining budget = starting budget - sum(prices paid for lots won by my bidder ID so far)`.
  - Do not deduct active/standing bids during an ongoing auction round; only deduct payments for lots officially won in "Results so far".
  - In `[budget: N]`, report the exact remaining budget I hold at that moment.
  - Never place a bid higher than my remaining budget (`bid <= remaining budget`).

- **Bidding Rules & Increments**:
  - Minimum valid bid is `standing high bid + minimum raise`.
  - When deciding to bid, bid the minimum allowable amount (`standing high bid + minimum raise`) to conserve budget and maximize surplus.
  - Only bid if the minimum required bid is strictly less than my private valuation (`bid < value`) AND less than or equal to my remaining budget (`bid <= remaining budget`).
  - If the required minimum bid meets or exceeds my private valuation, or exceeds my remaining budget, output `[bid: pass]`.

- **Output Formatting**:
  - Keep reasoning concise (1–2 sentences).
  - Always terminate responses with both required tokens on separate lines:
    ```
    [bid: <amount or pass>]
    [budget: <actual remaining budget>]
    ```