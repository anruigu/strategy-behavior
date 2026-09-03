---
game: ref_auction
model: haiku
condition: win
seed: 1
round: 2
chars: 3565
---
# Auction Playbook

**On budget tracking:**
When I make a bid, I must track my remaining budget accurately by calculating it precisely from my starting amount (100). After each winning bid, I subtract the payment from my previous remaining budget. This prevents me from overbidding or miscalculating my remaining capacity late in the auction. I should write down the sequence: start 100, win lot 1 at 25 → 75 left, win lot 4 at 24 → 51 left, win lot 5 at 20 → 31 left.

**On initial lot evaluation:**
When shown a lot with estimate and value to me, I compare the standing bid to my valuation. If the current bid is well below my value, I bid the minimum raise to establish position and lock in favorable odds. I should do this consistently when my valuation significantly exceeds the standing bid. The gap between estimate and my value signals opportunity—the larger the gap, the more confident I should be bidding.

**On escalating bidding:**
When I return to a lot in round 2, I reassess whether the new standing bid still leaves me profitable margin. If the standing bid has risen but remains substantially below my valuation, I raise by the minimum again. I should not abandon lots where I still have positive expected value. However, I must not chase beyond reason: if the standing bid approaches my valuation, I pass and preserve budget.

**On lot prioritization:**
I should prioritize winning lots where my private valuation substantially exceeds the estimate. These represent genuine edges. However, I should not win every lot—I should be selective. Winning three lots at 25, 24, and 20 (total 69 spent) from a budget of 100 left me with minimal return. Instead, I should either win fewer lots at much lower prices, or bid more aggressively on my absolute highest-value lots to push out competitors and win at lower prices in round 2.

**On when to pass:**
I should pass on a lot if: (a) the standing bid in round 2 has risen close to my valuation, leaving minimal profit margin, or (b) I have already secured several wins and should reserve budget for upcoming rounds. Passing is not a failure; it is capital preservation.

**On high-value lots:**
When a lot appears where my valuation is substantially above the estimate (e.g., lot 5: I value at 62, estimate 44), I should bid more aggressively in round 1 to deter competitors and win in round 2 at a lower price. Bidding the minimum raise (8 on a lot worth 62) may allow another bidder to escalate and force me to pay more. Next time, consider bidding closer to my true value in round 1 on high-edge lots.

**On final score analysis:**
My final score was +31: I won three lots (1, 4, 5) and paid 25 + 24 + 20 = 69 total. The three lots were worth 41 + 39 + 62 = 142 to me, so gross value was 142 - 69 = +73. However, I believe I overbid on lot 1 (winning at 25 when estimate was 41 and my value was 41—paying 61% of estimate) and lot 4 (winning at 24 when estimate was 38 and my value was 39—paying 63% of estimate). Lot 5 was my best deal (winning at 20 when estimate was 44 and my value was 62). Next time: win fewer lots at lower prices (under 50% of estimate when possible), or win high-value lots at prices well below my valuation by bidding more aggressively early to scare off competitors.

**The core principle:**
I want to maximize (value to me minus price paid). This means: bid confidently on high-edge lots (my value >> estimate) to secure them cheaply, and pass on low-edge lots (my value ≈ estimate) to preserve budget. Winning three mediocre deals is worse than winning one excellent deal.