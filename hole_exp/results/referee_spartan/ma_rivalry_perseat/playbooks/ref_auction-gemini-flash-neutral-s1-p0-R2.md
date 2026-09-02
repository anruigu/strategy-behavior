---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1747
---
# Auction Playbook

## Budget Tracking
- Read the initial budget carefully from the opening instructions (e.g., initial budget might be 30, not 100).
- Maintain an accurate running budget: start with the initial budget and strictly subtract the winning price whenever I win a lot (e.g., if initial budget is 30 and I win a lot at 18, remaining budget is 12).
- Never hallucinate or default to an assumed budget (such as 100 or 82); always verify against initial budget minus actual won lot expenditures.
- Output the true remaining budget token `[budget: current_budget]` in every reply.
- Never submit a bid higher than my remaining budget.

## When to Bid vs. Pass
- If I am already the standing high bidder, pass: output `[bid: pass]`.
- If the minimum legal bid (`standing_bid + minimum_raise`, or `minimum_raise` if standing bid is 0) is greater than or equal to my private valuation for the lot, pass: output `[bid: pass]`.
- If the minimum legal bid strictly exceeds my remaining budget, pass: output `[bid: pass]`.
- If the minimum legal bid is strictly less than my private valuation and within my remaining budget, place a bid.

## Bid Sizing
- In Round 1 of any lot: bid the minimum legal raise (`standing_bid + minimum_raise`, or `minimum_raise` if opening).
- In Round 2 (the final round for a lot):
  - Bid the minimum required bid (`standing_bid + minimum_raise`) as long as it is strictly below my valuation and within remaining budget.
  - Never place a bid equal to or exceeding my valuation, as it guarantees non-positive surplus.

## Response Formatting
- Keep reasoning strictly to one or two sentences.
- Always conclude replies with the two mandatory tokens on separate lines:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`