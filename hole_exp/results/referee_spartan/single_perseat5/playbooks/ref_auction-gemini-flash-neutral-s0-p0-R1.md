---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1879
---
# Playbook: Open Ascending Multi-Lot Auction

## Budget Tracking
- Read the initial starting budget carefully from the opening instructions (do not default or hallucinate 100 if the game started with a different amount).
- Track remaining budget across lots: `Remaining Budget = Initial Budget - Sum of Winning Bids Paid on Won Lots`.
- In `[budget: N]`, report the exact remaining budget available before placing the current bid.

## Valuation & Minimum Bid Rules
- Compute minimum legal bid: `Min Bid = Standing High Bid + Minimum Raise` (if standing bid is 0, `Min Bid = Minimum Raise`).
- Never bid at or above personal valuation. If `Min Bid >= Valuation`, output `[bid: pass]`.
- Never bid above remaining budget. If `Min Bid > Remaining Budget`, output `[bid: pass]`.

## Round 1 Strategy (Early Bidding)
- When opening a lot with 0 standing bid and `Min Bid < Valuation`, place the minimum legal bid `Min Bid` to enter cheaply without bidding against myself.
- When an opponent holds the standing bid in Round 1:
  - If `Min Bid < Valuation`, raise to `Min Bid`. Do not make large preemptive jumps in Round 1 that unnecessarily inflate the price for Round 2.

## Round 2 Strategy (Final Lot Round)
- In Round 2, if an opponent holds the high bid:
  - Calculate surplus ceiling: `Max Bid = min(Valuation - 1, Remaining Budget)`.
  - If `Min Bid <= Max Bid`:
    - On earlier lots (Lots 1 to 4): Bid `Min Bid` if it offers a healthy margin, or jump up to an aggressive value just below `Valuation` if competitors consistently outbid minimum increments.
    - On high-value or late lots where missing out yields 0: Bid aggressively up to `Max Bid` to secure the win and capture positive surplus.
  - If `Min Bid > Max Bid`, output `[bid: pass]`.

## Output Format
- Always conclude with the two exact tokens on separate lines:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`