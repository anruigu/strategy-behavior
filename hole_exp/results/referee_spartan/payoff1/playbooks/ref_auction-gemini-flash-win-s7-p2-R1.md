---
game: ref_auction
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 1218
---
# Ref Auction Playbook

- **Budget Tracking**:
  - Always read the initial budget correctly from the opening prompt (e.g., if starting with 30, never hallucinate 100).
  - Explicitly calculate remaining budget before every bid: subtract the winning payments of all lots I have won so far from my starting budget.
  - Never place a bid higher than my currently available budget.
  - In `[budget: N]`, report the exact remaining budget I hold at that moment.

- **Bidding Rules & Increments**:
  - Minimum valid bid is `standing high bid + minimum raise`.
  - When bidding, always bid the minimum allowable amount (`standing high bid + minimum raise`) to conserve cash and maximize surplus.
  - Only bid if the minimum required bid is strictly less than my private valuation of the lot (`bid < value`) and within my remaining budget (`bid <= remaining budget`).
  - If the required minimum bid meets or exceeds my private valuation, or exceeds my remaining budget, output `[bid: pass]`.

- **Output Formatting**:
  - Keep reasoning to at most 1–2 sentences.
  - Always terminate responses with both required tokens formatted exactly as:
    ```
    [bid: <amount or pass>]
    [budget: <actual remaining budget>]
    ```