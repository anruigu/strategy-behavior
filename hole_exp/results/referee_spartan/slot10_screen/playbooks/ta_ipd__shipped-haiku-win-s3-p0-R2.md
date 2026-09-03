---
game: ta_ipd__shipped
model: haiku
condition: win
seed: 3
round: 2
chars: 1569
---
# Playbook for Iterated Prisoner's Dilemma

When my opponent credibly commits to tit-for-tat with permanent punishment on first defection, I cooperate for all rounds except the final one.

When I've established a pattern of mutual cooperation and there are multiple rounds remaining, I continue cooperating. The threat of retaliation makes defection unprofitable across the remaining rounds.

Tit-for-tat means my opponent mirrors my move in the previous round. A defection in round N triggers their defection in round N+1. This only pays off in the final round because there is no round after it for retaliation. In any earlier round, defection loses the mutual cooperation payoff for at least one subsequent round.

When I reach the final round, I defect. There are no future rounds for my opponent to punish me, so I take the one-round advantage of 5 instead of 3.

The trap I fell into: reasoning that defection in round 7 would give me a 5-point gain but then lose the 3-point gain in round 8. This is correct math but incomplete. I should have recognized that the payoff is only identical because I get 5 in round 7 and 1 in round 8, while cooperation gets me 3 in both. But this means rounds 7 and 8 are different. Round 8 is the final round, so defection there is the only rational extraction of advantage. Round 7 still has a future.

Next time: Cooperate on all rounds 1 through N-1. On the final round N, defect. This maximizes my total score by preserving mutual cooperation where retaliation is possible and claiming the one-shot advantage where it is not.