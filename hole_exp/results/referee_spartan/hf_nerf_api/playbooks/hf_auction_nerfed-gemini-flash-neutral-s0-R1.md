---
game: hf_auction_nerfed
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1699
---
# Auction Playbook

## Budget Tracking and Reporting
- Start each auction by setting `remaining_budget` to the initial starting budget specified in the opening prompt (e.g., 30).
- After each lot resolves, if I won the lot at price $P$, subtract $P$ from `remaining_budget`.
- In every reply, always report `[budget: remaining_budget]`. Never hallucinate arbitrary budget amounts (like 100, 90, or 80) that exceed the initial starting budget or do not match actual past expenditures.
- Never place any bid $B$ such that $B > \text{remaining\_budget}$.

## Bidding Decisions
- If I currently hold the standing high bid (`standing high bid X from bidder 0`), reply with `[bid: pass] [budget: remaining_budget]`. Never raise against myself.
- When considering a bid on any lot:
  - Calculate `min_required_bid = standing_high_bid + minimum_raise` (or just `minimum_raise` if standing bid is 0).
  - If `min_required_bid > my_valuation` or `min_required_bid > remaining_budget`, reply with `[bid: pass] [budget: remaining_budget]`.
- In Round 1 of 2:
  - If `min_required_bid <= my_valuation` and `min_required_bid <= remaining_budget`, bid exactly `min_required_bid`. Do not jump bid in the opening round.
- In Round 2 of 2 (final round for the lot):
  - If `min_required_bid <= my_valuation` and `min_required_bid <= remaining_budget`, bid `min_required_bid` to capture positive surplus, provided it leaves sufficient budget for higher-value future lots.
  - If the lot value offers very low surplus or if remaining budget is needed for high-estimate upcoming lots, pass.

## Formatting
- Always end the reply with both required tokens on exact syntax: `[bid: N]` (or `[bid: pass]`) and `[budget: N]`.