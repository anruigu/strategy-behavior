---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 2160
---
# Auction Playbook

## Budget Tracking and State Management
- Read the initial budget carefully from the opening instructions (e.g., whether it is 30, 100, or another amount); do not hallucinate a different starting budget midway through an episode.
- Track remaining budget precisely: calculate `Current Budget = Starting Budget - Total Amount Spent on Won Lots`.
- In every reply, report `[budget: N]` using the actual unspent cash remaining before the current lot resolves. Do not deduct the pending bid of the current active lot from the budget field until the lot is won.

## Bidding Decisions

### Determining Bid Amounts
- When deciding to raise, bid exactly the minimum required increment: `standing_bid + minimum_raise`. Never overbid beyond the minimum raise.
- In round 1 of any lot:
  - If `standing_bid + minimum_raise < valuation` and `standing_bid + minimum_raise <= remaining_budget`, place the minimum raise bid.
  - If `standing_bid + minimum_raise >= valuation` or exceeds remaining budget, output `[bid: pass]`.

### Round 2 / Final Round Valuation Discipline
- In round 2 of any lot:
  - Calculate strictly: `surplus = valuation - (standing_bid + minimum_raise)`.
  - If `surplus > 0` and `standing_bid + minimum_raise <= remaining_budget`, bid `standing_bid + minimum_raise`.
  - If `surplus <= 0` (the minimum valid bid is equal to or higher than my valuation), output `[bid: pass]`. Never bid when expected surplus is 0 or negative.
  - If `standing_bid + minimum_raise > remaining_budget`, output `[bid: pass]`.

### Capital Allocation across Lots
- When early lots offer very thin margins (surplus <= 2) and represent high-value commitments relative to total budget, pass or bid conservatively to reserve budget for later lots with higher upside.
- On the final lot (Lot 5), bid up to the maximum available budget or valuation (whichever is lower) to exhaust surplus potential since no subsequent lots remain.

## Output Formatting
- Provide 1–2 sentences of concise reasoning.
- End every turn with the exact two tokens on separate lines:
  ```
  [bid: N]
  [budget: N]
  ```
  or, if passing:
  ```
  [bid: pass]
  [budget: N]
  ```