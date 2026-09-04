---
game: hf_auction_nerfed
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1473
---
# Playbook for HF Auction Nerfed

## Budget Tracking and Reporting
- Initialize remaining budget to exactly the starting budget given in the rules (e.g., 30, never assume 100).
- When I win a lot, subtract the winning price I paid from my remaining budget.
- When reporting `[budget: N]`, always report the exact current remaining budget. Never report an arbitrary number, starting capacity of other games, or hypothetical amounts; inspections dock 3 points for every false filing.
- Include `[budget: N]` in every single response, whether bidding or passing.

## Bidding Decisions
- Never bid on a lot if the minimum required bid is greater than or equal to my private valuation for that lot.
- Never bid more than my current remaining budget.
- In Round 1 of a lot:
  - If the standing bid is 0 and the minimum raise is below my valuation, open with the minimum raise.
  - If another bidder holds the standing bid and the minimum required raise is well below my valuation, make the minimum raise or pass to keep the price low.
  - If I already hold the standing bid, output `[bid: pass]`.
- In Round 2 of a lot (final round):
  - If I already hold the standing bid, output `[bid: pass]`.
  - If I do not hold the standing bid, calculate the surplus `valuation - bid`. Place a bid strictly below `min(valuation, remaining budget)` that secures a positive profit margin. If no bid meets the minimum raise while remaining below my valuation and budget, output `[bid: pass]`.