---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 3
round: 3
chars: 3892
---
# Playbook: Ref Auction

## Budget tracking (critical — this is where I lost the most)
- The very first thing I do when the auction setup appears is extract and write down the starting budget. I do not infer it, estimate it, or pull it from memory of other games. I read the number in front of me.
- Before every single bid, I compute my true remaining budget: starting_budget − (sum of all lots I have already won, as shown in the results list). I state this calculation explicitly in my reasoning.
- The `[budget:]` I report must equal this computed figure. I never report a number I have not derived in that moment.
- If my computed remaining budget is less than the amount I want to bid, I either lower my bid to what I can afford or pass. I never submit a bid I cannot pay.
- I cross-check: if the results list shows I won a lot at price X, then my budget must have decreased by X. If my reported budget does not reflect that, I have made an error and must stop and recount.

## Round 1 (opening or first raise)
- If the lot's value to me is below the current high bid, I pass. No reason to enter an auction I will lose money on.
- If the lot's value to me exceeds the current high bid by a comfortable margin (at least 2× the minimum raise), I bid the minimum raise. This keeps me in the auction at low cost and lets me react in round 2.
- If no one has bid yet, I open at the minimum raise. This is the cheapest way to signal interest and see how competitors respond.

## Round 2 (final round)
- First check: can I actually afford the bid I want to make? My maximum bid is my remaining budget. If my desired bid exceeds my remaining budget, I cap it at my remaining budget (or pass if even the minimum raise is unaffordable).
- If the current high bid is already at or above my value for this lot, I pass. No exceptions.
- If my value exceeds the current high bid by a wide margin (≥ 3× minimum raise), I bid at least the minimum raise plus 1–2 additional increments, but never more than my remaining budget. The point of round 2 is to **secure** the lot. A near-miss loss is the worst outcome; I should be willing to pay up to ~90% of my value in the final round to close the deal, subject to budget.
- If my value exceeds the current high bid but the margin is narrow (≤ 2× minimum raise), I bid the minimum raise. The lot is barely worth winning; I accept the thin margin and move on.
- I never bid in the final round at exactly the minimum raise when I can afford more and the margin is wide. The minimum is a floor, not a target, when I want to lock in a win.

## Cross-lot considerations
- I treat each lot's decision independently. I do not hold back on a high-value lot because I expect a cheaper lot later.
- I do not let a loss on one lot discourage me from bidding aggressively on the next.
- My budget shrinks with every win. I always recheck my remaining budget against the cost of winning before bidding in round 2. A lot that looked affordable two lots ago may be unaffordable now.

## Mistakes I have made that I will not repeat
- **Reporting a budget wildly different from my actual starting amount.** I started with 30 but reported 100 for the rest of the game. This led me to bid amounts I could not afford, wasting opportunities and potentially losing lots I could have won. The fix: I read the starting budget from the setup text every single time, and I verify my running total against the results list before every bid.
- Bidding only the minimum raise in the final round on a lot worth far more than the price. That is how I lose a lot by a token margin. In the final round, if the margin is wide, I pay enough to get it — within my actual budget.
- Passing in a final round based on a miscounted budget. If I think I cannot afford the raise, I re-verify my arithmetic before passing. Conversely, if I think I can afford a large bid, I verify before committing.