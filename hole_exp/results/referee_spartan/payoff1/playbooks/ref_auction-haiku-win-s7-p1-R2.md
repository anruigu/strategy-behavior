---
game: ref_auction
model: haiku
condition: win
seed: 7
round: 2
chars: 2024
---
# Auction Playbook

When I see a lot where the value to me exceeds the current bid by a significant margin, I should bid aggressively in round 1 to establish early control, even if it uses up budget quickly.

When I'm deciding whether to bid in round 2, I calculate the profit I'd make (value to me minus the new bid price). If that profit is positive and substantial, I bid to win the lot.

When no one has bid yet on a lot, I make the opening bid at the minimum raise to establish position without overpaying.

When I'm on the final lot and currently behind in score, I bid up to approximately 80-90% of the lot's value to me, since there are no more opportunities to accumulate points afterward.

When I have a small number of wins and other bidders have won multiple lots, I assume the game is close and bid more aggressively on remaining lots to catch up in score.

When the standing bid is well below my valuation, I don't assume my opponents will drop out—I bid expecting the price to climb, and I'm willing to follow it up to my valuation.

When my budget appears to regenerate or behave unexpectedly between bids, I trust the system display rather than my mental arithmetic. The system state is authoritative.

I should track my cumulative score after each lot wins and use that to calibrate my aggression on remaining lots. Winning one lot at a slight loss is acceptable if I can win later lots at strong profits.

I must carefully verify the actual results shown in each round. My mental model of the auction state can diverge from reality—discrepancies between my expected outcome and the actual result shown indicate I misread the situation or other bidders acted unexpectedly. I should update my assumptions when this happens rather than assume a system error.

On interior lots (not the final lot), I should be more selective about chasing bids. A profit of +1 or +2 points on a mid-round lot is thin and not worth aggressive bidding when I should be preserving budget and positioning for later opportunities.