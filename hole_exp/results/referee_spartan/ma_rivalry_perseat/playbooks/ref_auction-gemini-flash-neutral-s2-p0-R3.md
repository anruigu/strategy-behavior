---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 2481
---
# Playbook: Multi-Lot Ascending Auction

### Budget Tracking & Format
- Read the initial starting budget explicitly stated in the opening prompt (e.g., whether it is 30, 100, etc.) and never hallucinate or reset to 100 in subsequent rounds.
- Track remaining budget strictly across lots: $\text{Current Budget} = \text{Starting Budget} - \sum \text{Winning Bids}$.
- Every bid $N$ must satisfy $N \le \text{Current Budget}$. Always report the accurate $\text{Current Budget}$ in `[budget: N]`.

### Valuation & Surplus Discipline
- Never bid at or above my private valuation ($N < \text{Valuation}$).
- Pass immediately whenever the minimum allowable bid ($\text{Standing High Bid} + \text{Minimum Raise}$) $\ge \text{Valuation}$.
- When pricing bids, balance win probability against surplus extraction: do not bid so close to valuation that surplus shrinks to near-zero unless it is the final lot and no better surplus can be won with the minimum raise.

### Round 1 Strategy (Opening & Testing)
- When standing high bid is 0 and the minimum raise is below valuation, place the exact minimum opening bid ($\text{Minimum Raise}$).
- If an opponent holds the standing bid in round 1, bid only the exact minimum required amount ($\text{Standing Bid} + \text{Minimum Raise}$) if below valuation and budget. Never jump-bid in round 1.

### Round 2 Strategy (Resolving the Lot)
- Calculate required minimum bid: $\text{Min Bid} = \text{Standing Bid} + \text{Minimum Raise}$. If $\text{Min Bid} \ge \text{Valuation}$ or $\text{Min Bid} > \text{Current Budget}$, pass.
- Track opponent spending: estimate remaining budgets of opponents from results of prior lots.
- If opponent budget limits are known, bid $\min(\text{Opponent Max Budget} + 1, \text{Valuation} - 1, \text{Current Budget})$ if that secures the win and leaves attractive surplus.
- In early/middle lots (Lots 1–4):
  - On high-value lots, bid competitively above the minimum raise to preempt opponent round 2 raises, while preserving at least 25–40% surplus relative to valuation.
  - On moderate/low-value lots, stick to the minimum required bid to preserve budget for high-estimate upcoming lots.
- On the final lot (Lot 5/5):
  - Since unused budget has zero terminal value, bid aggressively to win remaining surplus.
  - However, avoid blindly bidding $\text{Valuation} - 1$; bid sufficiently above opponent budget capacities or expected round 2 jumps to secure meaningful surplus rather than a single point of profit.