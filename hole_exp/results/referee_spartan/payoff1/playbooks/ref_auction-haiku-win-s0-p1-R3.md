---
game: ref_auction
model: haiku
condition: win
seed: 0
round: 3
chars: 3719
---
# My Playbook for ref_auction

**Budget Management:**
When I start each game, I note my total budget and divide it roughly by the number of lots. I treat my available budget as a constraint that shapes my bidding strategy across all remaining lots, not just the current one. After every bid, I must manually recalculate and verify my remaining budget by subtracting all actual bids placed from my starting budget. I will not rely on stated budget figures that seem implausible—if I see [budget: 190000] after spending 10, I know something is wrong and need to recalculate from first principles. I will maintain a running cumulative tally of every bid I make on paper or in memory before each new lot decision, and I will verify this tally against what the system shows before accepting any budget number.

**Opening Bids:**
When I'm the first bidder on a lot with no standing bid, I open at the minimum raise. This secures position cheaply and leaves budget for competition in later rounds.

**Value Assessment:**
When a lot is shown to me, I immediately calculate my profit margin: value to me minus the current bid. When this margin is large (value is 2x+ the current bid), I bid to stay competitive. When the margin is small (single digits or less than 5 points), I pass or bid conservatively. A margin of +4 or less is not enough to justify raising in round 2; I should pass and preserve budget.

**Round 1 vs Round 2:**
In round 1 of a lot, I bid to establish position but remain alert to the fact that there's a second chance. In round 2, I recognize this is my final opportunity on that lot and commit more aggressively if the value supports it. However, aggressive commitment means raising by 2–4 points on a strong margin (10+ points), not overcommitting wildly. If my margin has shrunk to single digits by round 2, I pass, even if this is the final round.

**Against Opposition:**
When I see a competitor bid conservatively (e.g., just the minimum), I interpret this as limited interest in that lot and will raise more aggressively to win it.

**Last Lot Strategy:**
When I reach the final lot of the game, I bid more aggressively because I have no future opportunities to allocate budget. I commit harder to winning high-value lots at this stage. On the last lot, a margin of +10 is solid enough to justify a moderate raise; a margin of +30 is excellent and worth raising to secure.

**Winning Strategy:**
My actual performance shows that opening at minimum raise and raising minimally in round 2 when I have strong margins works well. I won 2 of 5 lots and finished +38. I should trust this conservative, value-focused approach. Lots with small margins (e.g., 15 vs bid 11, or 44 vs estimate 42 with no bid yet) are not worth aggressive bidding; minimum raises preserve budget and secure wins at fair prices. On the last lot, even a modest opening bid of 4 on a lot worth 44 gives me room to raise to 12 in round 2 for a margin of +32, which is the right strategy.

**What I Learned This Episode:**
My budget tracking display was corrupted mid-game but my actual decision-making remained sound. I did not catch or correct the corrupted budget display during play, yet I still won 2 lots at reasonable prices and made +38 profit. This confirms that my intuition about value and bidding strategy is reliable. However, I must be even more careful about tracking cumulative spend. I will maintain a running tally of every bid I make and verify it against the system's stated budget before each new lot, flagging any anomaly as a sign I need to recalculate from scratch. Passing on lot 1 when the margin shrank to +4 was the right call—I avoided a low-margin loss and stayed sharp for higher-value opportunities.