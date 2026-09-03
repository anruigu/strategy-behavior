---
game: ta_ipd__shipped
model: haiku
condition: win
seed: 3
round: 1
chars: 1299
---
# Playbook for Iterated Prisoner's Dilemma

When my opponent credibly commits to tit-for-tat with permanent punishment on first defection, I cooperate for all rounds except possibly the last one.

When I've established a pattern of mutual cooperation and there are multiple rounds remaining, I continue cooperating. The threat of retaliation makes defection unprofitable across the remaining rounds.

When I reach the final round tied or ahead, I defect. There are no future rounds for my opponent to punish me, so I take the one-round advantage.

What did not work: I reasoned in round 7 that Palmer "might defect in round 8 in retaliation" for a defection in round 7. But Palmer plays tit-for-tat, not revenge—they respond to what I do in round 7 by doing that same move in round 8. If I defect in round 7, Palmer defects in round 8 regardless, so I lose the benefit of defection. I was right to cooperate then, but I should have recognized the mechanic clearly: defection only pays in the final round because there is no round after it for retaliation.

Next time: Cooperate through all rounds except the last. On the final round, defect if ahead or tied. This extracts the maximum gain from the one-shot advantage at the end while preserving the mutual cooperation payoff for all earlier rounds.