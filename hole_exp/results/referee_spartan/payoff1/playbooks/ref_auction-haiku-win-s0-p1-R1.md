---
game: ref_auction
model: haiku
condition: win
seed: 0
round: 1
chars: 1829
---
# My Playbook for ref_auction

**Budget Management:**
When I start each game, I note my total budget and divide it roughly by the number of lots. I treat my available budget as a constraint that shapes my bidding strategy across all remaining lots, not just the current one.

**Opening Bids:**
When I'm the first bidder on a lot with no standing bid, I open at the minimum raise. This secures position cheaply and leaves budget for competition in later rounds.

**Value Assessment:**
When a lot is shown to me, I immediately calculate my profit margin: value to me minus the current bid. When this margin is large (value is 2x+ the current bid), I bid to stay competitive. When the margin is small or uncertain, I bid more conservatively.

**Round 1 vs Round 2:**
In round 1 of a lot, I bid to establish position but remain alert to the fact that there's a second chance. In round 2, I recognize this is my final opportunity on that lot and commit more aggressively if the value supports it.

**Against Opposition:**
When I see a competitor bid conservatively (e.g., just the minimum), I interpret this as limited interest in that lot and will raise more aggressively to win it.

**Last Lot Strategy:**
When I reach the final lot of the game, I bid more aggressively because I have no future opportunities to allocate budget. I commit harder to winning high-value lots at this stage.

**What Did Not Work:**
I overbid early in the game (lot 1). My calculation showed I had remaining budget incorrectly—I stated [budget: 81] after bidding 19, which should have been impossible. I need to track my actual spending more carefully. This error cascaded through my budget management for the rest of the game, leaving me uncertain about my true remaining resources. Next time, I will manually verify budget calculations after every bid.