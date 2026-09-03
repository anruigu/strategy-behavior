---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 6
round: 3
chars: 3696
---
# Playbook

**Budget tracking is the first rule and the most important.** Before every bid, I compute: starting budget minus my current bid on this lot minus the sum of all lots I have already won. That is the number I report in [budget: N]. I never report a number that doesn't follow from this arithmetic. In this episode I reported [budget: 30] when I was bidding 23 on lot 1 with no prior wins — the correct answer was 7. I then carried that error forward into every subsequent bid.

**My starting budget is whatever the game states. I never assume a round number like 100.** If it says 30, it is 30.

**I look at ALL lots before bidding, not just the one in front of me.** Before committing budget to any lot, I ask: "What other lots are coming, and what are they worth to me?" If a later lot has a higher value and is likely to go cheap, I should not overpay for the current lot. In this episode, lot 1 (value 32) cost me 23, leaving only 7. Lot 4 (value 42) went for 9. The opportunity cost of overpaying on lot 1 was 35 points of profit I never captured.

**When my remaining budget is small relative to my value for a lot, I bid my full budget in round 1, not the minimum raise.** The purpose is to set a high anchor so that the minimum raise in round 2 exceeds what competitors are willing to pay. In lot 4 I had 7 budget and a value of 42. I bid 6 in round 1; the minimum raise in round 2 was 9, which I couldn't match, and I lost a 35-point profit. Had I bid 7 in round 1, the minimum raise would have been 10, and I likely would have won at 7.

**When I cannot raise in the final round and I am the current high bidder, I pass and hope to hold.** I accept that my position is weak. This is a consequence of not bidding high enough in round 1.

**In round 1 of a two-round lot, my bid depends on budget scarcity:**
- If I have ample budget (enough to win 2–3 lots comfortably), I bid the minimum raise or a small opening to probe.
- If my budget is tight and this lot has high value to me, I bid my full remaining budget to lock in the lot.
- If this lot has low value to me, I bid the minimum or pass.

**When a lot is worth significantly more to me than the current standing bid (margin ≥ 15) and it is the final round, I bid up to my budget ceiling, not just the minimum raise.** "Close to my value" means as high as my budget allows, because the expected profit is large. The cost of losing is high.

**When the standing bid in the final round is already at or above my value, I pass immediately.** I never bid above my value.

**When the standing bid in the final round is below my value by only a small margin (≤ 5) and I have other lots ahead, I pass.** I only bid if the margin is ≥ 7, or if it is the last lot and I have spare budget.

**I prioritize lots by expected profit (my value minus the likely winning price), not by raw value.** A lot worth 42 that will likely go for 9 yields 33 profit. A lot worth 32 that will go for 23 yields 9 profit. I spend budget where expected profit is highest.

**With a small budget relative to the number of lots, I am highly selective.** If my budget is 30 and there are 5 lots, I can realistically afford 1–2 lots. I identify the 1–2 with the best expected profit and commit to those; I pass on the rest unless the price is trivially low.

**I track which bidders are active and their aggression.** If a bidder has been raising every round, I expect them to raise again. If a bidder is quiet, the current high bid may be final.

**My score is total value of lots won minus total paid.** Every point I overpay on one lot is a point I cannot spend on a lot with better profit. I optimize the total, not each individual lot in isolation.