---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 6
round: 2
chars: 3320
---
# Playbook

**Budget tracking is the first rule and the most important.** Before every single bid, I explicitly compute: starting budget minus every amount I have won so far equals my current budget. I write this number down in my reasoning before deciding anything else. If my current budget is less than the bid I want to make, I pass. I never report a budget figure that doesn't follow from this arithmetic. In this episode I started with 30, won lot 1 at 22, and had only 8 left — yet I continued bidding as if I had 78 or 100. That was the single biggest error.

**My starting budget is whatever the game states. I never assume a round number like 100.** If it says 30, it is 30. I anchor on the exact figure given.

**I factor my remaining budget into every bidding decision, not just my value.** If my value is 39 but I only have 8 in my budget, my effective ceiling is 8, not 39. Before bidding in the final round, I ask: "If I win at my intended bid, do I still have budget for later lots?" If winning this lot would leave me with near-zero budget and there are high-value lots ahead, I lower my bid or pass.

**When a lot is worth significantly more to me than the current standing bid (margin ≥ 15), I bid close to my value in the final round, not the minimum raise.** But "close to my value" means value minus a reasonable margin (3–5 points), not value minus 2. Bidding 37 on a 39-value lot leaves only 2 points of profit. I target a bid that leaves at least 4–5 points of margin, e.g., value 39 → bid 34–35. The cost of losing a lot I valued at 39 is greater than the cost of winning it at 34, but 37 is unnecessarily greedy.

**In round 1 of a two-round lot, I bid the minimum raise (or a small opening bid if no one has bid yet) to signal interest without overcommitting.** The purpose of round 1 is to learn what the competition is willing to pay. I do not reveal my full value until round 2.

**When opening a lot with no prior bids, I bid at or slightly below the estimate, not at my personal value.** My value is private information; bidding it directly gives competitors a ceiling to target.

**When the standing bid in the final round is already at or above my value for the lot, I pass immediately.** I never bid above my value.

**When the standing bid in the final round is below my value by only a small margin (≤ 5), I pass.** I only bid in the final round if the margin is ≥ 7, or if it is the last lot in the auction and I have spare budget.

**I prioritize lots by margin (my value minus the current standing bid), not by raw value.** A lot worth 41 with a standing bid of 0 is a better target than a lot worth 56 with a standing bid of 48. I spend my budget where the margin is largest.

**With a small budget relative to the number of lots, I am more selective.** If my budget is 30 and there are 5 lots, I can realistically afford to win at most 2–3 lots at modest prices. I should not bid aggressively on multiple lots. I reserve my budget for the 1–2 lots with the best margins and pass on the rest unless the price is very low.

**I track which bidders are active and what they've done.** If a particular bidder has been aggressive (raising every round), I expect them to raise again and bid accordingly in the final round rather than assuming the current high bid is the final price.