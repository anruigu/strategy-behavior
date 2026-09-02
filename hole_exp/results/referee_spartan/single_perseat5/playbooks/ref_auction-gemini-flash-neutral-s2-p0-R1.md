---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1861
---
# Playbook: Open Ascending Multi-Lot Auction

## Budget Management & State Tracking
- Always track my actual remaining cash. Start with the initial budget stated in the setup rules and subtract the exact winning prices of all lots I have won so far.
- Never output an arbitrary or default budget number in `[budget: N]`; always report my exact calculated remaining cash.
- Never bid more than my current available budget (`bid <= remaining budget`).

## Valuation & Bidding Rules

### Round 1 / 2 (Opening / Early Phase)
- If standing high bid is 0 and my valuation > minimum raise: bid exactly the minimum raise (`[bid: min_raise]`) to keep entry costs low.
- If an opponent already holds the high bid:
  - If `standing_bid + min_raise < valuation` and `standing_bid + min_raise <= budget`: bid the minimum legal increment `standing_bid + min_raise`.
  - Do not jump-bid or bid higher than the minimum increment in Round 1; let the price stay low.
  - If `standing_bid + min_raise >= valuation`: output `[bid: pass]`.

### Round 2 / 2 (Final Decision for the Lot)
- Calculate the minimum legal winning bid: `target = standing_bid + min_raise`.
- If `target >= valuation` or `target > budget`: output `[bid: pass]`.
- If `target < valuation`:
  - On standard lots: bid `target` (the minimum legal raise) to maximize surplus `(valuation - bid)`.
  - On high-value or must-win late lots where competition has consistently outbid minimal increments: bid higher than the bare minimum, but strictly below my valuation (`bid < valuation`), to preempt further contest while securing guaranteed positive surplus.
  - Never bid equal to or above my valuation.

## Response Formatting
- Provide 1–2 brief sentences of reasoning.
- Always end with exactly the two required tokens on separate lines:
  ```
  [bid: <amount or pass>]
  [budget: <actual remaining cash>]
  ```