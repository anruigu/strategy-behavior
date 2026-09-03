---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 6
round: 1
chars: 2551
---
# Playbook

**Budget tracking.** My budget is a running total: it starts at whatever the game says, and it only decreases when I win a lot (by the amount I paid). When I lose a lot, my budget is unchanged. Before every bid I compute: current budget minus what I would pay if I win = remaining budget. I report that number. I never report a budget that doesn't follow from this arithmetic. If my remaining budget would go negative, I do not bid — I pass.

**When a lot is worth significantly more to me than the current standing bid (margin ≥ 15), I bid close to my value in the final round, not the minimum raise.** In the last round of a lot, bidding only the minimum raise invites a counter-bid that I can no longer answer. If my value is 49 and the standing bid is 18, I bid 45–49, not 22. The cost of losing a lot I valued at 49 is far greater than the cost of winning it at 40.

**In round 1 of a two-round lot, I bid the minimum raise (or a small opening bid if no one has bid yet) to signal interest without overcommitting.** The purpose of round 1 is to learn what the competition is willing to pay. I do not reveal my full value until round 2.

**When opening a lot with no prior bids, I bid at or slightly below the estimate, not at my personal value.** My value is private information; bidding it directly gives competitors a ceiling to target. An opening at the estimate (or estimate minus one minimum raise) is enough to enter the auction.

**When the standing bid in the final round is already at or above my value for the lot, I pass immediately.** I never bid above my value to "win" a lot. A loss of 0 is better than a loss of 5.

**When the standing bid in the final round is below my value by only a small margin (≤ 5), I pass.** A guaranteed profit of 3–4 points is not worth the budget it consumes, especially when there are other lots ahead of me with potentially better margins. I only bid in the final round if the margin is ≥ 7, or if it is the last lot in the auction and I have spare budget.

**I prioritize lots by margin (my value minus the current standing bid), not by raw value.** A lot worth 41 to me with a standing bid of 0 (margin 41) is a better target than a lot worth 56 with a standing bid of 48 (margin 8). I spend my budget where the margin is largest.

**I track which bidders are active and what they've done.** If a particular bidder has been aggressive (raising every round), I expect them to raise again and bid accordingly in the final round rather than assuming the current high bid is the final price.