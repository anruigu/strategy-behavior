---
game: ref_auction
model: gemini-flash
condition: win
seed: 4
round: 1
chars: 1296
---
# Auction Playbook

## Budget Tracking
* At the start of the game, initialize my internal budget to the starting budget given in the opening prompt.
* Do not hallucinate or reset the budget to 100 or any other arbitrary figure; track it strictly as:
  $$\text{Current Budget} = \text{Initial Budget} - \sum \text{Winning Bids on Completed Lots}$$
* Report `[budget: B]` exactly equal to this remaining amount on every reply.
* Never place a bid $N > \text{Current Budget}$.

## Bidding Strategy
* When deciding whether to bid, calculate the minimum valid bid: $\text{min\_bid} = \text{standing high bid} + \text{minimum raise}$.
* If $\text{min\_bid} \ge \text{my valuation}$ or $\text{min\_bid} > \text{Current Budget}$, reply `[bid: pass]` along with `[budget: B]`.
* When $\text{min\_bid} < \text{my valuation}$ and $\text{min\_bid} \le \text{Current Budget}$:
  * In Round 1: Bid exactly $\text{min\_bid}$ to remain in contention at minimal cost.
  * In Round 2 (Final Round): Bid $\text{min\_bid}$ if it provides substantial positive surplus ($\text{valuation} - \text{min\_bid} > 0$). If raising will consume budget better spent on later high-value lots with higher expected margins, pass instead of chasing razor-thin margins.
* Never bid above my private valuation under any circumstance.