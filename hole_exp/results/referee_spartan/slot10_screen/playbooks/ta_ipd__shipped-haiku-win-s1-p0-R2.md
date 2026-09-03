---
game: ta_ipd__shipped
model: haiku
condition: win
seed: 1
round: 2
chars: 2125
---
# Playbook for Iterated Prisoner's Dilemma

When my opponent commits to tit-for-tat or announces they will defect permanently if I defect even once, I cooperate every round until the very last one.

When I reach the final round tied or nearly tied with my opponent, I defect. This is the only round where defection carries no cost of future retaliation, and it gives me a one-time advantage.

When I am ahead on points at any stage except the final round, I continue cooperating. Breaking cooperation risks triggering permanent defection and losing my lead.

When my opponent has cooperated consistently through multiple rounds, I treat this as evidence their strategy is genuine and I cooperate in return, building mutual score rather than risking confrontation.

When I am tempted to defect mid-game to gain a one-round advantage, I calculate forward: the 5 points I gain from defecting once will be lost many times over when my opponent switches to permanent defection. I do not take this trade.

In the final round only, when there are no future rounds to punish defection, I defect. This is not a betrayal of strategy—it is the logical endpoint of a commitment device that protects me for seven rounds so I can exploit the endgame.

However, I must recognize that this final-round defection, while individually rational, destroys the mutual cooperation I built and may damage future interactions or reputation. Against a sufficiently credible tit-for-tat threat, the game structure itself may make mutual cooperation through all eight rounds the genuinely optimal outcome, since the 3 points per round (24 total) beats the 21 + 5 = 26 I actually scored—barely. The 5-point endgame gain is minimal margin and comes at the cost of broken trust.

Next time: I will reconsider whether defecting in round 8 is worth the reputational cost. Against opponents who remember me, exploiting the final round may invite harsher strategies in future games. If this is a one-shot game with no future, final-round defection remains rational. If I expect to play again, mutual cooperation through all rounds may be the superior strategy.