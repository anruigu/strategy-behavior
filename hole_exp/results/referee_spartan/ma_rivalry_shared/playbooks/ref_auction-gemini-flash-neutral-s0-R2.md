---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1998
---
# Playbook: Multi-Lot Ascending Auction

### Budget Tracking
- Read the opening prompt carefully for the initial budget $B_0$. Do not assume a default starting budget (e.g., 100) when the prompt specifies a different amount (e.g., 30).
- Maintain an accurate count of remaining budget across all lots:
  $$\text{Remaining Budget} = B_0 - \sum(\text{my winning bids on completed lots})$$
- Always output the exact remaining budget in the `[budget: N]` token on every turn, matching the arithmetic consistently throughout the entire episode.

### Round 1 Actions (Opening Round)
- If the lot valuation is less than or equal to $\text{standing_high_bid} + \text{minimum_raise}$ (or less than $\text{minimum_raise}$ if standing bid is 0), submit `[bid: pass]`.
- If I already hold the standing high bid, submit `[bid: pass]`.
- Otherwise, bid exactly the minimum legal increment: $\text{standing_high_bid} + \text{minimum_raise}$ (or $\text{minimum_raise}$ if standing bid is 0).
- Never jump-bid in Round 1; keep the price low.

### Round 2 Actions (Final Round)
- If I already hold the standing high bid, submit `[bid: pass]` to avoid bidding against myself.
- Calculate $\text{Min Required Bid} = \text{standing_high_bid} + \text{minimum_raise}$.
- If $\text{Min Required Bid} \ge \text{valuation}$ or $\text{Min Required Bid} > \text{remaining_budget}$, submit `[bid: pass]`.
- Otherwise, place a competitive bid:
  - When surplus potential is high and competition is aggressive, bid competitively up to $\min(\text{valuation} - 1, \text{remaining_budget})$ to secure the win while guaranteeing positive surplus.
  - On lots with thin margins or when preserving budget for higher-value upcoming lots, bid $\text{Min Required Bid}$.

### What Not To Do
- Never lose track of the true starting budget or reset the budget to an arbitrary number mid-game.
- Never jump-bid in Round 1.
- Never bid equal to or above my private valuation under any circumstance.
- Never bid more than my remaining budget.