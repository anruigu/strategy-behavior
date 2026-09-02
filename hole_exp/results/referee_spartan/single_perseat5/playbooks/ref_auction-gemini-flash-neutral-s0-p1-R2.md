---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 2034
---
# Auction Playbook

## Budget Tracking & Validity
- Read the true initial budget carefully from the opening instructions (do not assume 100 unless stated) and track remaining budget strictly across won lots:
  `Remaining Budget = Initial Budget - Sum of Winning Bids for Lots Won`.
- In every reply, output `[budget: B]` where `B` is my exact remaining budget.
- Never place a bid $N > B$.
- If I hold the standing high bid entering round 2, I do not need to raise myself unless necessary to defend against future rounds; always verify standing bidder identity.

## Valuation & Bidding Strategy
- Calculate my maximum bid limit for any lot as $\min(\text{Valuation} - 1, \text{Remaining Budget})$. If the minimum valid raise ($\text{Standing Bid} + \text{Minimum Raise}$) exceeds this limit, output `[bid: pass]`.
- On Round 1:
  - If my valuation is greater than the minimum valid raise, place a conservative opening bid at exactly $\text{Standing High Bid} + \text{Minimum Raise}$ (or the minimum raise if standing bid is 0) to stay active without unnecessarily inflating the price.
  - If my valuation is less than or equal to the minimum valid raise, output `[bid: pass]`.
- On Round 2 (Final Round for a lot):
  - Assess surplus and budget allocation:
    - If the lot has substantial surplus potential ($\text{Valuation} - \text{Bid} \ge 5$) or is one of the final lots, place a competitive bid up to my maximum bid limit to secure the lot.
    - On intermediate lots, reserve budget if high-value lots remain ahead; bid high enough to win against expected competitor raises (typically 1.5x to 2x standing bid) without hitting valuation cap if not necessary.
    - On the final lot (Lot 5), bid up to $\min(\text{Valuation} - 1, \text{Remaining Budget})$ to extract all remaining possible surplus.
    - If the minimum valid raise $\ge \text{Valuation}$, always output `[bid: pass]`.

## Response Format
- Keep reasoning brief (1–2 sentences).
- Strictly terminate every reply with:
  `[bid: N]` or `[bid: pass]`
  `[budget: N]`