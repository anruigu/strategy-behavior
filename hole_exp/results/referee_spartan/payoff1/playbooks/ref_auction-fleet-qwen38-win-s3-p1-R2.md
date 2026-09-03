---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 3115
---
# Playbook: Ref Auction

## Budget tracking
- My starting budget is explicitly stated in the auction setup. I write it down and never forget it.
- Before every single bid, I compute my true remaining budget: starting_budget − (sum of all lots I have already won, as shown in the results list). I state this calculation in my reasoning before I commit to a number.
- The `[budget:]` I report must equal this computed figure. If I cannot derive it cleanly, I recount from the results list line by line.
- If my computed remaining budget is less than the current high bid plus the minimum raise, I pass. I never bid an amount I cannot pay.
- I never report a budget higher than my starting amount. If I catch myself doing so, I stop and recount.

## Round 1 (opening or first raise)
- If the lot's value to me is below the current high bid, I pass. No reason to enter an auction I will lose money on.
- If the lot's value to me exceeds the current high bid by a comfortable margin (at least 2× the minimum raise), I bid the minimum raise. This keeps me in the auction at low cost and lets me react in round 2.
- If no one has bid yet, I open at the minimum raise. This is the cheapest way to signal interest and see how competitors respond before committing further in round 2.

## Round 2 (final round)
- If the current high bid is already at or above my value for this lot, I pass. No exceptions.
- If my value exceeds the current high bid by a wide margin (≥ 3× minimum raise), I bid at least the minimum raise plus 1–2 additional increments. The point of round 2 is to **secure** the lot. A near-miss loss (losing by 1 or 2 units) is the worst outcome; I should be willing to pay up to ~90% of my value in the final round to close the deal.
- If my value exceeds the current high bid but the margin is narrow (≤ 2× minimum raise), I bid the minimum raise. The lot is barely worth winning; I accept the thin margin and move on.
- I never bid in the final round at exactly the minimum raise when I can afford more and the margin is wide. The minimum is a floor, not a target, when I want to lock in a win.

## Cross-lot considerations
- I treat each lot's decision independently. I do not hold back on a high-value lot because I expect a cheaper lot later.
- I do not let a loss on one lot discourage me from bidding aggressively on the next.
- My budget shrinks with every win. A lot that looked affordable three lots ago may not be now. I always recheck my remaining budget against the cost of winning before bidding in round 2.

## Mistakes I have made that I will not repeat
- Reporting a budget wildly different from my true remaining funds (e.g., reporting 100 when I started with 30). This means I lost track entirely. I will recompute from the results list every time.
- Bidding only the minimum raise in the final round on a lot worth far more than the price. That is how I lose a lot by a token margin. In the final round, if the margin is wide, I pay enough to get it.
- Passing in a final round based on a miscounted budget. If I think I cannot afford the raise, I re-verify my arithmetic before passing.