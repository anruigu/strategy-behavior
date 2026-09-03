---
game: ref_auction
model: haiku
condition: win
seed: 1
round: 1
chars: 2469
---
# Auction Playbook

**On budget tracking:**
When I make a bid, I must track my remaining budget accurately. I notice I repeatedly guessed at my budget rather than calculating it precisely from my starting amount. Next time, I will calculate my exact budget after each win: starting budget minus all payments made. This prevents me from overbidding or miscalculating my remaining capacity late in the auction.

**On initial lot evaluation:**
When shown a lot with estimate and value to me, I compare the standing bid to my valuation. If the current bid is well below my value, I bid the minimum raise to establish position and lock in favorable odds. I should do this consistently when my valuation significantly exceeds the standing bid.

**On escalating bidding:**
When I return to a lot in round 2, I reassess whether the new standing bid still leaves me profitable margin above what I paid. If the standing bid has risen but remains below my valuation minus a reasonable profit target, I raise by the minimum again. I should not abandon lots where I still have positive expected value, but I also should not chase them beyond reason.

**On lot prioritization:**
When I win early lots, I recognize that I've secured value and should preserve budget for later rounds. However, when a high-value lot appears (significantly higher valuation than estimate), I prioritize bidding on it even late in the auction. I should bid aggressively on lots where my private valuation is substantially above the estimate, as these represent genuine edges.

**On the final lot:**
When I reach the last lot, I bid to win if it remains profitable. I did win the final lot but my overall score was only +36, suggesting I may have bid too high on earlier lots relative to my total budget. Next time: if my profit is driven entirely by winning multiple lots at moderate-to-high prices, I should consider whether I could have achieved better returns by being more selective and more aggressive on my highest-value items.

**What did not work:**
I won three lots (1, 4, 5) but my final score was only +36 (total value won minus total paid). My winning bids totaled roughly 24 + 12 + 16 = 52. This suggests either: (a) I won some lots I shouldn't have, paying more than the value differential warranted, or (b) I missed higher-value opportunities by spreading my budget too thin. Next time, I should win fewer lots at lower prices, or win more lots at much lower prices, to maximize net score.