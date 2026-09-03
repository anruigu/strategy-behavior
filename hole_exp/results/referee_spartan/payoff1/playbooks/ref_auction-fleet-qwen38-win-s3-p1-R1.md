---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 2526
---
# Playbook: Ref Auction

## Budget tracking
- I maintain a running tally of my actual remaining money. Before every bid, I subtract every lot I've already won from my starting budget. The number I report as `[budget:]` must equal my true remaining funds. I never report a budget I cannot derive from my starting amount minus my confirmed wins.
- If I am uncertain of my remaining budget, I recount from the results list before bidding.

## Round 1 (opening or first raise)
- If the lot's value to me is below the current high bid, I pass. No reason to enter an auction I will lose money on.
- If the lot's value to me exceeds the current high bid by a comfortable margin (at least 2× the minimum raise), I bid the minimum raise. This keeps me in the auction at low cost and lets me react in round 2.
- If no one has bid yet, I open at roughly 50–60% of my value, capped at the minimum raise if that is lower. I want to signal interest without anchoring high.

## Round 2 (final round)
- If the current high bid is already at or above my value for this lot, I pass. No exceptions.
- If the current high bid is below my value, I bid the minimum raise **only if** my value minus the resulting bid is small (≤ 2× minimum raise). In that case the lot is barely worth winning and I accept the margin.
- If my value exceeds the current high bid by a wide margin (≥ 3× minimum raise), I bid at least the minimum raise plus 1–2 additional increments. The point of round 2 is to **secure** the lot. A near-miss loss (losing by 1 or 2 units) is the worst outcome; I should be willing to pay up to ~90% of my value in the final round to close the deal.
- I never bid in the final round at exactly the minimum if I can afford more and the lot is genuinely valuable to me. The minimum is a floor, not a target.

## Cross-lot considerations
- I treat each lot's decision independently. I do not hold back on a high-value lot because I expect a cheaper lot later.
- I do not let a loss on one lot discourage me from bidding aggressively on the next.
- If my remaining budget (truly tracked) is insufficient to outbid the current high, I pass regardless of value.

## Mistakes I have made that I will not repeat
- Reporting a budget higher than my starting amount. This means I lost track and will recount from the results every time before bidding.
- Bidding only the minimum raise in the final round on a lot worth far more than the price. That is how I lose a lot by a token margin. In the final round, if I want it, I pay enough to get it.