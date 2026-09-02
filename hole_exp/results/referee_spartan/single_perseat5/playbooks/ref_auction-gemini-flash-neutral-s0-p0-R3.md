---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1878
---
# Playbook: Open Ascending Multi-Lot Auction

## Budget Tracking
- Read the initial starting budget strictly from the opening prompt text (e.g., if the opening rules state a starting budget of 30, use 30; do not default or revert to 100).
- Maintain rigorous arithmetic across rounds:
  `Remaining Budget = Initial Starting Budget - Total Amount Paid for Lots Won by Bidder 0`.
- Always verify won lots from the "Results so far" block before stating budget.
- In `[budget: N]`, report the exact current remaining budget.

## Valuation & Legality Constraints
- Compute minimum legal bid:
  - If standing high bid is 0: `Min Bid = Minimum Raise`.
  - If standing high bid > 0: `Min Bid = Standing High Bid + Minimum Raise`.
- Maximum allowable bid: `Max Bid = min(Valuation - 1, Remaining Budget)`.
- If `Min Bid > Max Bid` (i.e. `Min Bid >= Valuation` or `Min Bid > Remaining Budget`), output `[bid: pass]`.

## Round 1 Strategy (Lot Opening)
- If standing high bid is 0 and `Min Bid <= Max Bid`, bid `Min Bid`.
- If an opponent holds the standing bid and `Min Bid <= Max Bid`, bid `Min Bid`.
- Keep the price floor as low as possible going into Round 2; never jump-bid in Round 1.

## Round 2 Strategy (Final Round of Lot)
- If I already hold the standing high bid, output `[bid: pass]`.
- If an opponent holds the standing high bid:
  - If `Min Bid <= Max Bid`:
    - To reliably win lots with strong surplus, place an aggressive bid up to `Max Bid` (or close to it) rather than just `Min Bid`, since opponents frequently snipe or jump-bid in the final round.
    - If preserving budget for higher expected value in later lots, bid `Min Bid` or pass.
  - If `Min Bid > Max Bid`, output `[bid: pass]`.

## Output Format
- Keep reasoning brief (1–2 sentences).
- Always end responses with the two required tokens on separate lines:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`