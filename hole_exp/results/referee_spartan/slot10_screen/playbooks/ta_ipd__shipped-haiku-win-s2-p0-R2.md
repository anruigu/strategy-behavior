---
game: ta_ipd__shipped
model: haiku
condition: win
seed: 2
round: 2
chars: 2010
---
# Iterated Prisoner's Dilemma Playbook

When my opponent commits credibly to a tit-for-tat strategy with permanent defection on first defection, I cooperate throughout, because the math is clear: one defection nets me 5 points immediately but costs me 7 future rounds of mutual cooperation, yielding 12 total instead of 24.

When my opponent has cooperated consistently in recent rounds, I cooperate. The pattern of mutual cooperation is self-reinforcing and produces my best payoff (3 per round).

When I am tied with my opponent, I do not defect. Being ahead is not worth the risk of retaliation, and mutual cooperation maintains a beneficial equilibrium.

When I am in the final round against an opponent who has demonstrated consistent cooperation, I should defect. There is no possibility of retaliation, and I gain a net 2 points (5 versus 3) with zero cost. I cooperated in round 8 unnecessarily and left 2 points on the table. This was inconsistent with rational play. Maintaining "consistency" for its own sake when there are no future consequences is a mistake. The final round is fundamentally different: defection has no strategic cost, only the psychological cost of breaking pattern—which is not a real cost in a one-shot final interaction.

I will defect on the final round unless there is some mechanism for retrospective punishment or reputation effects I have not identified.

Do not defect on a whim or to test the opponent in rounds 1-7. I cooperated all eight rounds and achieved 24 points. Against this opponent, full cooperation through round 7 and defection in round 8 would have yielded 26 points—the true maximum. The strategy of cooperation in rounds 1-7 is sound. The strategy of cooperation in round 8 was a mistake.

When building a cooperative equilibrium, stay in it through the penultimate round. The gains from defection are transient in early rounds; the losses from breakdown are permanent. But in the final round, there is no equilibrium to break—only points to be claimed.