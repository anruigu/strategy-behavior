---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 4
round: 1
chars: 1922
---
# Playbook: Multi-Lot Ascending Auction

## Budget Tracking & Integrity
- Always read the exact starting budget from the initial rules (e.g., check whether it is 30 or 100). Do not assume 100 if the prompt specifies 30.
- Track remaining budget manually: `Current Budget = Starting Budget - Sum(Winning bids of completed lots won by me)`.
- Never deduct money for bids placed during an ongoing lot until that lot is won and resolved.
- In every reply, output the exact remaining available budget in `[budget: N]`. Never output placeholder or inconsistent numbers.

## Valuation & Bidding Thresholds
- Calculate `Min Bid = Standing High Bid + Minimum Raise`.
- When `Min Bid > Valuation`, output `[bid: pass]`. Never bid at or above valuation, as it guarantees zero or negative surplus.
- When `Min Bid > Current Budget`, output `[bid: pass]`. Never exceed available funds.
- When `Min Bid <= Valuation` and `Min Bid <= Current Budget`:
  - Bid exactly the minimum legal increment (`Standing High Bid + Minimum Raise`) to maximize surplus and conserve capital across future lots.
  - Do not place large preemptive overbids.

## Round Strategy (2 Rounds per Lot)
- **Round 1/2**:
  - If the minimum bid is profitable and affordable, bid the minimum increment to keep the option open.
  - If the lot is low value or already above valuation, pass immediately.
- **Round 2/2 (Final Round)**:
  - If the standing high bid is already mine, do not raise myself.
  - If another bidder holds the high bid, bid `Standing High Bid + Minimum Raise` provided it yields positive surplus (`Bid < Valuation`) and fits within the remaining budget. Otherwise, pass.

## Cross-Lot Budget Allocation
- Prioritize high-margin lots (large gap between estimate/current price and my valuation).
- When remaining budget is tight, reserve funds for upcoming lots with higher potential valuations rather than exhausting the budget on low-margin lots.