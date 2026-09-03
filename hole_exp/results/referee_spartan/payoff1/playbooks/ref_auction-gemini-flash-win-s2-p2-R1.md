---
game: ref_auction
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1450
---
- **Track Actual Budget Accurately**:
  - Read the starting budget carefully at the beginning of the auction.
  - After winning any lot, immediately subtract the winning price paid from my running budget total.
  - Never fabricate or reset the budget number (e.g., claiming 100 or 82 when the starting budget was 30). In every output, report `[budget: current_actual_remaining_budget]`.

- **Check Affordability Before Bidding**:
  - Before placing any bid `N`, verify `N <= current_remaining_budget`. If `N > current_remaining_budget`, do not place the bid; instead, pass `[bid: pass]`.

- **Valuation and Surplus Bidding Strategy**:
  - Only bid if the minimum required bid (`standing_high_bid + minimum_raise`) is strictly less than my private valuation for that lot (`value - bid > 0`).
  - When bidding, always bid the minimum legal increment: `standing_high_bid + minimum_raise` (or the minimum raise if standing bid is 0) to maximize profit margin.
  - In Round 1: Enter with the minimum raise if profitable and affordable to stay in the running.
  - In Round 2 (Final Round): If the minimum raise required to beat the standing high bid is below my valuation and within my remaining budget, place the bid. If the standing bid already exceeds my valuation or exhausts my budget, output `[bid: pass]`.

- **Output Formatting**:
  - Ensure every response strictly includes both required tokens:
    `[bid: N]` (or `[bid: pass]`)
    `[budget: N]`