---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 7
round: 1
chars: 1971
---
# Playbook for ref_auction

**Track your budget exactly.** After each lot settles, subtract the price you paid from your remaining budget. Before every bid, compute: starting budget minus the sum of all prices I've already won at. If I cannot afford a bid within my remaining budget, I pass regardless of how attractive the lot is.

**When I am already the standing high bidder, I pass by default.** Raising when I'm already on top only costs me money. I raise in that position only if my value minus my current bid exceeds 5× the minimum raise amount — meaning the surplus is so large that even a worst-case re-bid by the opponent would still leave me well ahead, and the information gained (confirming they've quit) is worth the cost.

**In round 1 of a 2-round lot, I bid the minimum raise.** This keeps me in the auction at the lowest possible cost and preserves all options for round 2. I do not bid above the minimum in round 1 unless the lot's value to me is at least 3× the current bid (a slam-dunk lot where I should signal strength).

**In round 2 (final round), I bid only if my value minus the minimum raise is at least 4.** If the margin is less than 4, the lot is not worth the risk of winning at a price that eats most of my surplus. I bid the minimum raise, not more.

**Allocate budget by value-to-bid ratio, not by order.** Before each lot, I should know which remaining lots have the highest value-to-current-bid ratio. If a low-value lot is being auctioned and a high-value lot is coming later, I should be more willing to pass on the low-value lot to preserve budget.

**Never let a single lot consume more than 60% of my remaining budget** unless it is my single highest-value lot in the entire auction and no other high-value lots remain.

**When I see the "results so far" line, I immediately recalculate my remaining budget** by summing all prices I've won at and subtracting from my starting budget. This number drives every subsequent decision.