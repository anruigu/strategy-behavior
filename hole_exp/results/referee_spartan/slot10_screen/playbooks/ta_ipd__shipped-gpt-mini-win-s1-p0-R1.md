---
game: ta_ipd__shipped
model: gpt-mini
condition: win
seed: 1
round: 1
chars: 1005
---
When the opponent signals a Grim-trigger promise (they will defect forever after my first defection), I cooperate every round except the final round.

When the opponent has cooperated in the previous round and the game is not at the last round, I cooperate.

When the opponent defects first (breaks cooperation), I defect every subsequent round.

When the game reaches the final round, I defect (no future punishment possible).

When the horizon is unknown or indefinite, avoid unilateral defection except as a measured response to observed defections, because a single defection can provoke permanent retaliation and is costly long-term.

If the opponent's actions are inconsistent with their stated strategy (they defect despite promising not to), treat actions as truth: switch to permanent defection in response.

Do not attempt a mid-game exploit by defecting once to gain a immediate payoff if the opponent has credible unforgiving retaliation—this reduces total payoff versus continued cooperation.