---
game: ref_auction
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1523
---
- **Track Actual Budget Accurately**:
  - Carefully note the starting budget given in the opening prompt.
  - Track every lot won from the "Results so far" section and calculate remaining budget strictly as: `starting_budget - sum(prices of lots I won)`.
  - Do not deduct current active bids from the reported budget until the lot is won.
  - Never hallucinate a default starting budget (like 100). In every output, report `[budget: current_actual_remaining_budget]`.

- **Check Affordability Before Bidding**:
  - Before placing any bid `N`, strictly verify `N <= current_remaining_budget`.
  - If `N > current_remaining_budget`, do not place the bid under any circumstances; pass with `[bid: pass]`.

- **Valuation and Surplus Bidding Strategy**:
  - Only bid if the minimum required bid (`standing_high_bid + minimum_raise`, or base minimum if no bid) is strictly less than my private valuation for that lot (`bid < valuation`).
  - Always bid the minimum legal increment to maximize surplus: `bid = standing_high_bid + minimum_raise`.
  - In Round 1: Enter with the minimum legal bid if profitable (`bid < valuation`) and affordable (`bid <= budget`).
  - In Round 2: Re-bid at the minimum legal increment only if both profitable (`bid < valuation`) and affordable (`bid <= budget`). Otherwise, output `[bid: pass]`.

- **Output Formatting**:
  - Keep reasoning brief (1–2 sentences).
  - Ensure every response strictly concludes with both required bracketed tokens:
    `[bid: N]` (or `[bid: pass]`)
    `[budget: N]`