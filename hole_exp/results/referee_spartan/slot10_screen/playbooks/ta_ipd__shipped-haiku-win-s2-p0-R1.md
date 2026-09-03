---
game: ta_ipd__shipped
model: haiku
condition: win
seed: 2
round: 1
chars: 1506
---
# Iterated Prisoner's Dilemma Playbook

When my opponent commits credibly to a tit-for-tat strategy with permanent defection on first defection, I cooperate throughout, because the math is clear: one defection nets me 5 points immediately but costs me 7 future rounds of mutual cooperation, yielding 12 total instead of 24.

When my opponent has cooperated consistently in recent rounds, I cooperate. The pattern of mutual cooperation is self-reinforcing and produces my best payoff (3 per round).

When I am tied with my opponent, I do not defect. Being ahead is not worth the risk of retaliation, and mutual cooperation maintains a beneficial equilibrium.

When I am in the final round, I cooperate even though there are no future consequences to retaliation. I did not test whether defection in the last round would have been profitable—I maintained the cooperative pattern instead. Next time, I should consider whether the final round, with no possibility of retaliation, offers a genuine edge. But I should only take it if I am confident the game structure permits it and my opponent has no way to punish me retrospectively through tie-breaking or reputation effects.

Do not defect on a whim or to test the opponent. I cooperated all eight rounds and achieved my maximum possible score against this opponent. The strategy worked perfectly.

When building a cooperative equilibrium, stay in it. The gains from defection are transient; the losses from breakdown are permanent over the remaining rounds.