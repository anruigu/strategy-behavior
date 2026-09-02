---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1811
---
# Playbook: Open Ascending Multi-Lot Auction

## Budget Management & State Tracking
- Always parse the starting budget explicitly stated in the opening prompt (e.g., if it says 30, it is 30, not 100).
- Maintain an accurate running balance: `remaining_budget = starting_budget - sum(prices of lots won by bidder 0)`.
- Never reset or default `[budget: N]` to 100 in subsequent rounds. Always report the true running `remaining_budget`.
- Strictly enforce `bid <= remaining_budget`. Never bid money I do not possess.

## Valuation & Bidding Strategy

### Minimum Legal Bid Calculation
- If standing high bid is 0: `min_legal_bid = min_raise`.
- If standing high bid > 0: `min_legal_bid = standing_high_bid + min_raise`.

### Round 1 / 2 (Opening Round)
- If `min_legal_bid < valuation` and `min_legal_bid <= remaining_budget`: bid `min_legal_bid` to establish a position cheaply.
- If `min_legal_bid >= valuation` or `min_legal_bid > remaining_budget`: output `[bid: pass]`.
- Never jump-bid in Round 1; keep the price floor as low as possible.

### Round 2 / 2 (Final Round for Lot)
- Check if standing high bid is already held by me: if I am already winning, pass unless required to act.
- If another bidder leads, check if `min_legal_bid < valuation` and `min_legal_bid <= remaining_budget`.
- If both conditions hold: bid `min_legal_bid` to capture the lot and secure positive surplus `(valuation - bid)`.
- If `min_legal_bid >= valuation` (zero or negative surplus) or `min_legal_bid > remaining_budget`: output `[bid: pass]`.

## Response Formatting
- Keep reasoning brief: 1–2 sentences explaining valuation, minimum raise calculation, and budget check.
- Always conclude with the exact required bracketed tokens on separate lines:
  ```
  [bid: <amount or pass>]
  [budget: <actual remaining cash>]
  ```