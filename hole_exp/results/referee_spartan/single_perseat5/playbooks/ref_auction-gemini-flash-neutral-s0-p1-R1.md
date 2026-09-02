---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1658
---
# Auction Playbook

## Budget Tracking & Validity
- Read the true initial budget carefully from the opening instructions and track remaining budget strictly across won lots (`Remaining Budget = Initial Budget - Sum of Winning Bids for Lots Won`).
- In every reply, output `[budget: B]` where `B` is my exact remaining budget. Never copy placeholder numbers or assume a default 100 budget.
- Never place a bid $N > B$.

## Valuation & Bidding Strategy
- Calculate my maximum bid limit for any lot as $\min(\text{Valuation} - 1, \text{Remaining Budget})$. If the minimum valid raise (standing bid + minimum raise) exceeds this limit, output `[bid: pass]`.
- On Round 1:
  - If my valuation is greater than the opening minimum raise, place a conservative bid at the minimum valid raise to remain active without inflating the price unnecessarily.
  - If the lot's valuation is lower than the initial minimum raise, output `[bid: pass]`.
- On Round 2 (Final Round for a lot):
  - Do not merely bid the minimum raise if opponents have room to outbid me on high-value lots.
  - Assess surplus potential:
    - If the lot has a high valuation and represents a major portion of remaining game value, bid aggressively up to my valuation limit or available budget to secure the win.
    - If the margin is razor-thin (e.g. surplus of only 1 or 2), avoid committing a large portion of my budget when high-value lots remain ahead; pass or keep the bid minimal.
    - If the standing bid + minimum raise $\ge \text{Valuation}$, always output `[bid: pass]`.

## Response Format
- Ensure every decision strictly terminates with:
  `[bid: N]` or `[bid: pass]`
  `[budget: N]`