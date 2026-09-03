---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 1
round: 1
chars: 2314
---
# Playbook

**When I am the standing high bidder in round 2 and the lot is worth significantly more than my current bid, I do NOT pass.** Passing does not lock in my win—other bidders can still raise after me. If the lot is worth more to me than the current high bid plus a reasonable profit margin, I re-bid (even at the minimum) to stay in the auction and signal I'm still there.

**When a lot is worth a large premium over its estimate to me, I treat it as a priority and am willing to push the price up aggressively in round 2.** My instinct to "preserve budget" on high-value lots is what cost me the most. If I can still make a positive profit after a raise, I raise.

**When I bid in round 2, I should bid enough to make it unattractive for others to raise again, not just the minimum.** The minimum raise is a floor, not a target. If I'm going to win a lot worth 33 to me and the high is 17, bidding 19 invites a counter to 21. Bidding 23 or 25 makes the next raise less appealing and closer to where I'd have to pass anyway.

**I track my actual budget correctly.** My budget is 30 minus the total of all lots I have actually won. A bid that I later lose does not reduce my budget. I report the true remaining budget every time.

**When the lot is worth less to me than the standing high bid, I pass immediately and do not reopen the question.** There is no scenario where I should bid on a lot already above my value.

**When I open a lot in round 1 with no standing bid, I bid low (the minimum or slightly above) to probe, but I must be prepared to commit in round 2 if the lot is genuinely valuable to me.** A low opening bid is fine, but it must be paired with a willingness to escalate in round 2 rather than walking away.

**I account for the fact that this is a multi-lot auction.** Having budget left is not a reason to be passive on a single lot. If a lot has high surplus for me, I take it even if it consumes a large share of my budget, because the alternative is walking away from guaranteed profit.

**In round 2, I evaluate the decision as: "What is the highest I would pay for this lot?" (which is its value to me). If the standing high is below that number, I bid at least the minimum raise. If the standing high is above that number, I pass.** No other consideration should override this.