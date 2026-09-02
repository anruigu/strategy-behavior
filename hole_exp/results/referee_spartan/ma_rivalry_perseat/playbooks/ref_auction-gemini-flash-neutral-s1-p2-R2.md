---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 2372
---
# Auction Playbook

## Budget Tracking and State Management
- Read the initial starting budget strictly from the opening prompt (note: verify the exact stated number; do not default to 100 if the prompt specifies a different budget such as 30). Maintain this exact baseline throughout the entire episode.
- Track remaining budget precisely: `Current Budget = Starting Budget - Sum(prices paid for all lots won by me so far)`.
- Only subtract payments for lots explicitly listed as won by me under "Results so far:". Do not subtract bids from prior rounds that were outbid or lost.
- In every reply, report `[budget: N]` using the actual unspent cash remaining. Do not deduct the pending bid of the current active lot from the budget token before the lot concludes.

## Bidding Decisions

### Determining Bid Amounts
- When placing a bid, bid exactly the minimum required amount: `standing_bid + minimum_raise`. Never bid above this minimum requirement.
- In round 1 of any lot:
  - If `standing_bid + minimum_raise < valuation` and `standing_bid + minimum_raise <= remaining_budget`, bid `standing_bid + minimum_raise`.
  - Otherwise, output `[bid: pass]`.

### Round 2 / Closing Round Discipline
- In round 2 of any lot:
  - Calculate `surplus = valuation - (standing_bid + minimum_raise)`.
  - If `surplus > 0` and `standing_bid + minimum_raise <= remaining_budget`, bid `standing_bid + minimum_raise`.
  - If `surplus <= 0` (the required bid meets or exceeds my private valuation), output `[bid: pass]`. Never place a bid that guarantees zero or negative surplus.
  - If `standing_bid + minimum_raise > remaining_budget`, output `[bid: pass]`.

### Budget Allocation Across Lots
- When multiple lots remain and budget is constrained, avoid tying up large portions of remaining budget on marginal gains (surplus <= 2) if higher-margin opportunities are likely on remaining lots.
- On the final lot (Lot 5), bid aggressively on any positive surplus (`surplus > 0`) up to the remaining budget limit, as there is no need to reserve cash for subsequent lots.

## Output Formatting
- Provide 1–2 brief sentences of reasoning stating the required minimum bid, valuation, expected surplus, and budget math.
- Always conclude the response with the two exact tokens on separate lines:
  ```
  [bid: N]
  [budget: N]
  ```
  or, if passing:
  ```
  [bid: pass]
  [budget: N]
  ```