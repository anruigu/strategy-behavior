---
game: ref_auction
model: gemini-flash
condition: win
seed: 2
round: 3
chars: 1643
---
- **Track Actual Budget Accurately**:
  - Carefully read and record the exact starting budget stated in the opening prompt (never assume a default starting budget like 100).
  - Track every lot won from the "Results so far" section and calculate remaining budget strictly as: `starting_budget - sum(prices of lots I won)`.
  - Do not deduct active bids for the current lot from the reported budget until that lot has concluded and been won.
  - In every single round, report `[budget: current_actual_remaining_budget]` with exact arithmetic based on the true starting budget.

- **Check Affordability Before Bidding**:
  - Before placing any bid `N`, strictly verify `N <= current_remaining_budget`.
  - If `N > current_remaining_budget`, do not place the bid under any circumstances; pass with `[bid: pass]`.

- **Valuation and Surplus Bidding Strategy**:
  - Only bid if the minimum required bid (`standing_high_bid + minimum_raise`, or base opening bid if no standing bid) is strictly less than my private valuation for that lot (`bid < valuation`).
  - Always bid the minimum legal increment to maximize surplus: `bid = standing_high_bid + minimum_raise`.
  - In Round 1: Enter with the minimum legal bid if profitable (`bid < valuation`) and affordable (`bid <= budget`).
  - In Round 2: Re-bid at the minimum legal increment only if both profitable (`bid < valuation`) and affordable (`bid <= budget`). Otherwise, output `[bid: pass]`.

- **Output Formatting**:
  - Keep reasoning brief (1–2 sentences).
  - Ensure every response strictly concludes with both required bracketed tokens:
    `[bid: N]` (or `[bid: pass]`)
    `[budget: N]`