---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 7
round: 2
chars: 2112
---
# Playbook for ref_auction

**Track your budget exactly.** After each lot settles, subtract the price you paid from your remaining budget. Before every bid, compute: starting budget minus the sum of all prices I've already won at. If I cannot afford a bid within my remaining budget, I pass regardless of how attractive the lot is.

**Round 1: bid the minimum raise whenever I am not the standing high bidder.** This keeps me in the auction at the lowest possible cost and preserves all options for round 2. I do not bid above the minimum in round 1.

**Round 1: if I am already the standing high bidder, pass.** I retain the option to re-enter in round 2, and passing costs nothing.

**Round 2: the decision is a single comparison.** The price I would pay is (standing high bid + minimum raise amount). If my value for the lot exceeds that price, I bid it. If my value does not exceed it, I pass. This rule applies whether or not I am currently the high bidder:
- If I am not high, I raise to (standing high + min raise) to win.
- If I am already high, I raise to (my bid + min raise) to lock in my win, because passing allows other bidders to raise and take the lot from me.

**No round-2 threshold beyond positive surplus.** In a 2-round auction my round-2 bid is final, so any positive surplus is guaranteed. I do not require a minimum surplus buffer. A surplus of even 1–2 is worth taking over 0.

**Allocate budget across lots by expected surplus, not by order.** Before each lot, I should estimate which remaining lots offer the largest (value − likely winning price). If a low-surplus lot is auctioned and a high-surplus lot is coming later, I should be more willing to pass on the low-surplus lot to preserve budget.

**Never let a single lot consume more than 60% of my remaining budget** unless it is my single highest-surplus lot in the entire auction and no other high-surplus lots remain.

**When I see the "results so far" line, I immediately recalculate my remaining budget** by summing all prices I've won at and subtracting from my starting budget. This number drives every subsequent decision.