---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1851
---
# Auction Playbook

## Budget Tracking
- Read the initial budget carefully from the opening instructions (e.g., if the opening prompt states "You start with a budget of 30", initial budget is 30; if it states 100, initial budget is 100).
- Maintain an accurate running budget throughout the episode: start from the initial budget and strictly subtract the winning price of each lot won by me (bidder 0).
- Never hallucinate or switch budget defaults mid-game (e.g., jumping from 30 to 100 or vice versa); verify remaining budget consistently as `initial_budget - sum(prices of lots won by me)`.
- Output the true remaining budget token `[budget: current_budget]` in every reply.
- Never submit a bid higher than my remaining budget.

## When to Bid vs. Pass
- If I am already the standing high bidder, pass: output `[bid: pass]`.
- If the minimum legal bid (`standing_bid + minimum_raise`, or `minimum_raise` if opening with standing bid 0) is greater than or equal to my private valuation for the lot, pass: output `[bid: pass]`.
- If the minimum legal bid strictly exceeds my remaining budget, pass: output `[bid: pass]`.
- If the minimum legal bid is strictly less than my private valuation and within my remaining budget, place a bid.

## Bid Sizing
- In Round 1 of any lot: bid the minimum legal raise (`standing_bid + minimum_raise`, or `minimum_raise` if opening).
- In Round 2 (the final round for a lot):
  - Bid the minimum required bid (`standing_bid + minimum_raise`) as long as it is strictly below my valuation and within my remaining budget.
  - Never place a bid equal to or exceeding my valuation, as it guarantees non-positive surplus.

## Response Formatting
- Keep reasoning strictly to one or two sentences.
- Always conclude replies with the two mandatory tokens on separate lines:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`