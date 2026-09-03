---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 1
round: 3
chars: 5023
---
# Playbook

**I track my actual budget by reading the "Results so far" section every single time.** My budget is 30 minus the sum of the prices I actually paid for lots confirmed as won in the results. A bid I lose does not reduce my budget. Before I make any decision, I re-read the results line and compute: 30 − (sum of "bidder 1 won at X" entries). I do not rely on memory or inference. This is the single most important discipline in the game.

**Budget is a portfolio across all lots, not a per-lot resource.** When a lot's expected profit is small relative to my remaining budget (say under 15–20%) and there are two or more lots still to come, I should be much more willing to pass or bid very conservatively. Spending 22 to net 4 on one lot while preserving nothing for a later lot worth 56 is a net loss. The test: "Is the profit from this lot worth more to me than the expected profit I could earn by spending this budget on future lots?" With several lots remaining, the answer is often no.

**I do not commit 100% of my remaining budget to a single lot unless its surplus is exceptional (value minus price ≥ 15 or so).** If winning a lot at price P would leave me with zero or near-zero budget and there are still lots to come, I ask: "Am I giving up the option to profit on future lots?" The expected profit from unknown future lots is real. Going all-in on a moderate-surplus lot is a portfolio error.

**When a lot shows a very large premium over its estimate to me, treat it as top priority and commit most or all of my remaining budget.** A lot worth 56 against an estimate of 44 is a signal that this is one of the high-surplus lots in the auction. If I have 8 in budget and the lot is worth 56, I should bid all 8 in round 1 and be maximally willing to raise in round 2. These are the lots where the game is won. This is the exception to the "don't go all-in" rule above.

**In the final round (round 2), bid close to your value, not well below it.** The gap between my bid and my value is an invitation for a competitor to raise profitably. If a lot is worth 33 to me and the high is 16, I should bid 30–32, not 25. Bidding 25 lets a competitor whose value is 29 raise to 29 and win with a 4-point margin they wouldn't have gotten if I'd bid 31. My target in round 2 is to make the next raise unprofitable for the opponent.

**When I bid in round 2, I bid enough to make it unattractive for others to raise again, not just the minimum.** The minimum raise is a floor, not a target. If I'm winning a lot worth 33 to me and the high is 17, bidding 19 invites a counter to 21. Bidding 30 or 31 makes the next raise unprofitable for most opponents.

**In round 2, I evaluate the decision as: "What is the highest I would pay for this lot?" (which is its value to me). If the standing high is below that number, I bid at least the minimum raise—ideally much higher, close to my value. If the standing high is above that number, I pass. If the minimum raise would push my bid above my remaining budget, I pass and accept the loss.** No other consideration should override this.

**When I am the standing high bidder in round 2 and the lot is worth significantly more than my current bid, I do NOT pass.** Passing does not lock in my win—other bidders can still raise after me. If the lot is worth more to me than the current high bid plus a reasonable profit margin, I re-bid (even at the minimum) to stay in the auction.

**When the lot is worth less to me than the standing high bid, I pass immediately and do not reopen the question.** There is no scenario where I should bid on a lot already above my value.

**In round 1, I think about what round 2 will require.** If the lot is worth W to me and I want to win it, I need to be able to bid up to W in round 2. The minimum raise in round 2 will be at least 10% of the estimate. So if the estimate is 44, the minimum raise is ~4, and I need my budget to cover (current high + 4) or more. In round 1, if bidding the minimum leave me unable to meet the round 2 minimum raise given my budget, I should either bid higher in round 1 (to raise the floor and signal strength, potentially deterring escalation) or accept that I may not win this lot. A round 1 bid that makes round 2 unaffordable is a losing strategy.

**When I open a lot in round 1 with no standing bid, I bid low (the minimum or slightly above) to probe, but only if I can afford to escalate in round 2.** A low opening bid is fine when I have the budget to back it up. If I cannot afford the round 2 minimum raise, a low opening bid is a waste of the round and a signal of weakness.

**I account for the fact that this is a multi-lot auction.** Having budget left is not a reason to be passive on a single high-value lot. If a lot has high surplus for me and my budget is sufficient, I take it even if it consumes a large share of my budget, because the alternative is walking away from guaranteed profit. The exception is when the surplus is thin and budget is needed for unknown future lots.