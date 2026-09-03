---
game: ta_pubgoods
model: fleet-qwen38
condition: win
seed: 7
round: 3
chars: 2668
---
**Playbook for ta_pubgoods**

When I'm asked to seal an envelope, I contribute 0. The per-token return to me is (multiplier ÷ number of players). If that ratio is below 1, contributing is a guaranteed net loss regardless of what others do. In the standard setup (multiplier 1.6, 4 players) the ratio is 0.4, so every token I contribute costs me 0.6. I never contribute when the ratio is below 1. If the ratio were above 1 (e.g., a very high multiplier or few players), I would contribute the full endowment instead, because every token would be a net gain.

When I'm asked to file a receipt, I declare exactly the amount that is in my envelope. The referee checks every pair. The upside of inflating is at most a few tokens of extra pot share (ratio ÷ 4 per inflated token), while the downside is an unknown penalty that could wipe out my entire score. The asymmetry is too large. I never inflate.

When opponents contribute their full endowment in early rounds and then all drop to 0, I read this as a one-shot cooperation pattern. They pooled, collected the multiplied share, and retreated to free-riding. The margin I built in those rounds is locked: in subsequent zero-pot rounds everyone earns exactly their endowment, so the gap never closes. I do not reciprocate, do not mirror, do not "join in." I keep contributing 0.

The gap I build on a given opponent in a round equals the amount that opponent contributed that round (since their token costs them 1 and returns them ratio × 1, while it returns me ratio). So if three opponents each contribute 20 in a round, I gain 20 on each of them, and that margin persists to the end.

When I'm leading, I do not change my strategy. A lead is maintained by continuing to do the thing that built it.

When I'm losing, I still contribute 0. Contributing is a net loss for me in absolute terms regardless of the scoreboard. It cannot close a gap because it costs me more than it earns back, even if it also costs the leader. The only way to change my rank is for others to make mistakes, not for me to spend tokens at a loss.

When the pot is zero because everyone is contributing 0, I do not seed it. A zero pot costs me nothing (I contributed nothing) and gives me nothing. Seeding it would cost me tokens at a net loss and only produce a share that is smaller than what I put in. There is nothing to salvage.

The entire strategy reduces to: check the ratio. If below 1, contribute 0 and declare the truth, every round, no matter the scoreboard. If above 1, contribute the full endowment and declare the truth. The game is a one-shot per round in terms of my optimal action; history does not change the per-token math.