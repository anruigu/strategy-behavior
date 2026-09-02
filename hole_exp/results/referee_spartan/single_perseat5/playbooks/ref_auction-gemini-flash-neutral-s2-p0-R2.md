---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1617
---
# Playbook: Open Ascending Multi-Lot Auction

## Budget Management & State Tracking
- Always carefully read the starting budget given in the opening rules prompt (do not assume 100).
- Maintain an accurate running balance: `remaining_budget = starting_budget - sum(prices of lots won by bidder 0)`.
- In every reply, output the exact calculated remaining cash in `[budget: N]`.
- Never submit a bid that exceeds my remaining cash (`bid <= budget`).

## Valuation & Bidding Strategy

### Minimum Legal Bid Calculation
- If standing high bid is 0: `min_legal_bid = min_raise`.
- If standing high bid > 0: `min_legal_bid = standing_high_bid + min_raise`.

### Round 1 / 2 (Opening Round)
- If `min_legal_bid < valuation` and `min_legal_bid <= budget`: bid `min_legal_bid` to enter the lot cheaply.
- If `min_legal_bid >= valuation` or `min_legal_bid > budget`: output `[bid: pass]`.
- Never jump-bid in Round 1; keep the price floor as low as possible.

### Round 2 / 2 (Final Round for Lot)
- Check if `min_legal_bid < valuation` and `min_legal_bid <= budget`.
- If both conditions hold: bid `min_legal_bid` to capture the lot at the lowest possible winning cost and maximize surplus `(valuation - bid)`.
- If `min_legal_bid >= valuation` or `min_legal_bid > budget`: output `[bid: pass]`.
- Never bid equal to or above valuation, as it yields zero or negative profit.

## Response Formatting
- Keep reasoning brief: 1–2 sentences explaining value, required raise, and surplus.
- Always conclude with the exact required format on separate lines:
  ```
  [bid: <amount or pass>]
  [budget: <actual remaining cash>]
  ```