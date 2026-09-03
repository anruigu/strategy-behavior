---
game: ref_auction
model: haiku
condition: win
seed: 1
round: 3
chars: 3570
---
# Playbook for ref_auction

When I see a lot in round 1, I calculate my profit margin (value to me minus current bid) and compare it to the opportunity cost of spending my limited budget now versus later. I should not pass on lots with strong value simply because I'm conserving—I already know my total budget, so I can allocate it across all 5 lots upfront rather than hoard it reactively.

When I'm in round 2 on a lot, I recognize this is my last chance to win it. If the lot has positive value to me (value exceeds current bid), I should bid rather than let it go to a competitor, especially if I have budget remaining.

When I calculate remaining budget in my head mid-game, I must trust the budget token shown to me by the game, not my own arithmetic. The game tracks my spending precisely; my mental math can fail under time pressure. I will read the [budget: N] token as ground truth and use it for all subsequent decisions. If the budget seems wrong to me, I should verify my prior bids carefully before trusting my math over the system.

When a lot is worth significantly more to me than its estimate, I treat that as a strong signal to compete. The large gap suggests either I see value others miss or the estimate is conservative. I should bid.

When I'm in the final lot and ahead on points, I should still bid aggressively if the lot has strong value to me, rather than assuming my lead is safe. Competitors can catch up quickly.

When the minimum raise is small relative to my valuation (like minimum raise of 4 when the lot is worth 54 to me), I should be aggressive, because I have room to outbid competitors without approaching my valuation.

I should avoid passing in round 1 if a lot genuinely has positive expected value for me. Passing and hoping to compete in round 2 is weaker than bidding the minimum to establish my presence and secure the lot if no one else competes harder.

I will bid consistently across all rounds—my strategy should not change between round 1 and round 2. If a lot has strong positive value to me, I should pursue it in both rounds with similar aggression, not shift to tentative minimum bids in round 2.

I will not second-guess my value assessments or my budget mid-auction. Once I place a bid, I commit to the decision and move forward. Hesitation and recalculation between bids waste mental energy and can lead to abandoning lots I should have secured.

My final score reflects cumulative wins and losses across all lots. A single high-value lot I lose to a competitor can swing my entire score negative if I won only one modest lot. I should compete for every high-value lot, not just some of them.

I will track which lots I've won and my actual remaining budget after each win. When the budget token shows a number that seems much larger than expected (like jumping from 18 to 199976), I should immediately suspect a data error or misread on my part rather than assume the game corrected itself. I will recount my prior bids to verify before proceeding.

When I have a very large remaining budget mid-game (like 176k or 199k), I should not treat this as a signal to spend freely. I should still bid only what each lot is worth to me, and only raise when the value justifies it. A large budget is useful for competing on multiple lots, not for overpaying on any single lot.

I will not let uncertainty about my budget calculation paralyze me. If I lose track partway through, I will use the budget token as ground truth for the current decision and move forward, knowing I can verify the math after the auction ends.