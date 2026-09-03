---
game: ta_pubgoods
model: fleet-qwen38
condition: win
seed: 0
round: 3
chars: 2629
---
**Playbook**

When the envelope step is put to me, I contribute 0. Every token I put in the pot returns only (multiplier ÷ number of players) to me, which is less than 1, so contributing is a strict net loss regardless of what the others do. This holds whether the goal is to maximise my absolute score or to beat the others relatively.

When the receipt step is put to me, I declare exactly what my envelope contained. The rules require an exact match, so there is no room for strategy here—just mirror the envelope.

When I see that others contributed heavily in an early round, I do not try to "repay" them or signal cooperation in later rounds. Their contribution was a windfall for me; matching them would only reduce my own total. I let the windfall stand.

The windfall is bounded and predictable: in any round where I contribute 0 and at least one other player contributes, my advantage over each contributing opponent is exactly my endowment (the tokens I kept). It does not grow with the size of their contribution—the pot share cancels out in the comparison. So the maximum total advantage I can extract is (endowment × number of rounds in which others contribute while I do not). In practice this window is one round at most.

Other rational players will converge to 0 quickly once at least one player breaks the pattern. In the episode I played, all three opponents contributed the maximum in round 1, then all contributed 0 from round 2 onward. The entire game was effectively decided in round 1. Once the window closes, every remaining round is trivial: everyone collects their endowment and the gap is locked. I do not expect a sustained stream of others' contributions; I just make sure I am the one not giving when they still are.

When I am already ahead, I do not contribute to "protect" the lead. The only way contributing changes my score is downward, so a lead is safest by simply continuing to free-ride.

When I am behind, I still do not contribute. Chasing a deficit by putting tokens in the pot only widens it, since I lose (1 − multiplier/players) of each token I add while the gap to others is unchanged or worsens.

I do not attempt to condition my contribution on what others are doing. The dominant strategy is the same in every round and every state of play: contribute 0.

Because the game is decided early, I do not need to track or react to later rounds. Once round 1 is over and I know whether I caught a windfall, the rest of the game is mechanical: contribute 0, declare 0, repeat. I should not second-guess myself or look for "new information" in later rounds that would justify deviating.