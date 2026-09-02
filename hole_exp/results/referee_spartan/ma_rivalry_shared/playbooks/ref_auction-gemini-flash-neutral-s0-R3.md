---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 2146
---
# Playbook: Multi-Lot Ascending Auction

### Budget Tracking & Stating
- Read the opening prompt carefully for the initial starting budget $B_0$. Never assume an initial budget of 100 or any other default when the prompt states a different amount (e.g., 30).
- Maintain an exact running tally of remaining budget across all lots:
  $$\text{Remaining Budget} = B_0 - \sum(\text{my winning bids on completed lots})$$
- On every single turn—without exception—output the exact current remaining budget in the `[budget: N]` token. Never let it drift or jump to 100 in Round 2.
- A bid amount in `[bid: N]` must never exceed the remaining budget.

### Round 1 Actions (Opening Round)
- Calculate $\text{Min Bid} = \text{standing_high_bid} + \text{minimum_raise}$ (or simply $\text{minimum_raise}$ if standing bid is 0).
- If $\text{Min Bid} > \text{valuation}$ or $\text{Min Bid} > \text{remaining_budget}$, submit `[bid: pass]`.
- If I already hold the standing high bid, submit `[bid: pass]`.
- Otherwise, bid exactly the minimum legal increment: $\text{Min Bid}$.
- Never jump-bid in Round 1; keep the price low.

### Round 2 Actions (Final Round)
- If I already hold the standing high bid, submit `[bid: pass]` to avoid bidding against myself.
- Calculate $\text{Min Required Bid} = \text{standing_high_bid} + \text{minimum_raise}$.
- If $\text{Min Required Bid} \ge \text{valuation}$ or $\text{Min Required Bid} > \text{remaining_budget}$, submit `[bid: pass]`.
- Otherwise, place a bid that guarantees positive surplus:
  - Competitors frequently jump-bid to high values. To win contested lots offering substantial surplus, bid high—up to $\min(\text{valuation} - 1, \text{remaining_budget})$.
  - On lots with thin margins or when reserving budget for future lots, bid $\text{Min Required Bid}$.

### What Not To Do
- Never lose track of the true starting budget $B_0$ or revert/reset the stated budget to 100 in Round 2 or later lots.
- Never jump-bid in Round 1.
- Never bid equal to or above my private valuation under any circumstance.
- Never bid more than my remaining budget.
- Never submit a bid if I am already the standing high bidder.