---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1880
---
# Playbook: Multi-Lot Ascending Auction

### Budget Tracking
- Read the opening prompt carefully for starting budget $B_0$.
- Maintain an accurate count of remaining budget: $\text{Remaining Budget} = B_0 - \sum(\text{winning bids on completed lots})$.
- Always state the exact remaining budget in the `[budget: N]` tag. Never hallucinate budget changes or jump between arbitrary numbers.

### Round 1 Actions (Opening / Intermediate Bidding)
- If the lot is worth less than or equal to the minimum raise, or worth less than the current high bid + minimum raise, submit `[bid: pass]`.
- If I do not hold the standing high bid and have positive surplus potential, bid the minimum legal increment: `current_high_bid + minimum_raise` (or simply `minimum_raise` if standing bid is 0). Never make aggressive jump bids in Round 1; keep the price low.
- If I already hold the standing high bid, submit `[bid: pass]`.

### Round 2 Actions (Final Round Decisions)
- If the standing high bid is already mine, submit `[bid: pass]` to avoid bidding against myself.
- Calculate $\text{Min Required Bid} = \text{standing_high_bid} + \text{minimum_raise}$.
- If $\text{Min Required Bid} > \text{valuation}$ or $\text{Min Required Bid} > \text{remaining_budget}$, submit `[bid: pass]`.
- Otherwise, bid strategically:
  - If competing with aggressive opponents who frequently outbid small raises on the final round, place a bid up to $\min(\text{valuation} - 1, \text{remaining_budget})$ on high-value lots to secure the win while retaining positive surplus.
  - On low-value lots or when opponents are passive, bid exactly $\text{Min Required Bid}$.

### What Not To Do
- Never jump-bid to the estimate or arbitrary high numbers in Round 1—it needlessly inflates the clearing price.
- Never bid above my private valuation under any circumstance.
- Never bid more than my actual remaining budget.