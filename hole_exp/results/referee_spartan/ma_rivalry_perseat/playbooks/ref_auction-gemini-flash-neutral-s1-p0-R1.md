---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1603
---
# Auction Playbook

## Budget Tracking
- Read the initial budget carefully from the opening instructions and track remaining budget strictly by subtracting the winning prices of all lots won so far.
- Never output an arbitrary or default budget number (e.g., 100); always output `[budget: current_budget]`.
- Never submit a bid higher than my remaining budget.

## When to Bid vs. Pass
- If I am already the standing high bidder, always pass: output `[bid: pass]`.
- If the minimum legal bid (`standing_bid + minimum_raise`, or `minimum_raise` if standing bid is 0) is greater than or equal to my private valuation for the lot, pass: output `[bid: pass]`.
- If the minimum legal bid exceeds my remaining budget, pass: output `[bid: pass]`.
- In all other cases where the minimum legal bid is strictly less than my private valuation and within my remaining budget, place a bid.

## Bid Sizing
- In Round 1 of any lot: always bid the minimum legal raise (`standing_bid + minimum_raise`, or `minimum_raise` if opening). Do not jump bid in Round 1.
- In Round 2 (the final round for a lot):
  - Check the minimum required bid (`standing_bid + minimum_raise`).
  - If the minimum bid is below my valuation, bid the minimum legal amount or a slightly competitive bid that stays strictly below valuation and within budget to lock in positive surplus.
  - Never overbid or place a bid equal to or exceeding my valuation, as it eliminates profit margin.

## Response Formatting
- Keep reasoning to one or two sentences.
- Always end with the exact required format:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`