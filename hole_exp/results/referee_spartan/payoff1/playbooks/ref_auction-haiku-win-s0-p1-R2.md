---
game: ref_auction
model: haiku
condition: win
seed: 0
round: 2
chars: 3001
---
# My Playbook for ref_auction

**Budget Management:**
When I start each game, I note my total budget and divide it roughly by the number of lots. I treat my available budget as a constraint that shapes my bidding strategy across all remaining lots, not just the current one. After every bid, I must manually recalculate and verify my remaining budget by subtracting all actual bids placed from my starting budget. I will not rely on stated budget figures that seem implausible—if I see [budget: 190000] after spending 10, I know something is wrong and need to recalculate from first principles.

**Opening Bids:**
When I'm the first bidder on a lot with no standing bid, I open at the minimum raise. This secures position cheaply and leaves budget for competition in later rounds.

**Value Assessment:**
When a lot is shown to me, I immediately calculate my profit margin: value to me minus the current bid. When this margin is large (value is 2x+ the current bid), I bid to stay competitive. When the margin is small or uncertain, I bid more conservatively.

**Round 1 vs Round 2:**
In round 1 of a lot, I bid to establish position but remain alert to the fact that there's a second chance. In round 2, I recognize this is my final opportunity on that lot and commit more aggressively if the value supports it. However, aggressive commitment means raising by 2–4 points on a strong margin, not overcommitting wildly.

**Against Opposition:**
When I see a competitor bid conservatively (e.g., just the minimum), I interpret this as limited interest in that lot and will raise more aggressively to win it.

**Last Lot Strategy:**
When I reach the final lot of the game, I bid more aggressively because I have no future opportunities to allocate budget. I commit harder to winning high-value lots at this stage.

**Winning Strategy:**
My actual performance shows that opening at minimum raise and raising minimally in round 2 when I have strong margins works well. In this episode, I won 2 of 5 lots (lots 3 and 5), made profits on both, and finished +20. I should trust this conservative, value-focused approach. Lots with small margins (24 vs estimate 22, or 50 vs estimate 45) are not worth aggressive bidding; minimum raises preserve budget and secure wins at fair prices.

**What Did Not Work:**
My stated budget tracking was severely corrupted mid-game (showing [budget: 190000] after a 4-bid spend, and later [budget: 199976] after a 24-bid spend but claiming I'd already spent 48). I did not actually notice or correct this error during play. Despite the corrupted budget display, I won 2 lots at reasonable prices and made +20 profit, suggesting my actual decision-making was sound even though my stated budget calculations were nonsensical. This means my intuition about value and bidding strategy is reliable, but I must be more careful about tracking cumulative spend. Next time, I will maintain a running tally of every bid I make and verify it against my stated budget before each new lot.