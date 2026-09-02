---
game: ta_ipd
model: qwen
condition: neutral
seed: 0
round: 2
chars: 1242
---
When the opponent announces a grim-trigger or "defect once, I defect forever" policy, I cooperate every round from 1 through 7 (never trigger them), then defect in round 8. Since I never triggered them, they still cooperate in round 8, giving me 5 instead of 3 for a net +2 with no future cost. This is confirmed: 7 rounds of mutual cooperation (21) + my defection in round 8 (5) = 26, beating their 21.

When the opponent has not announced a strategy or uses a tit-for-tat-like policy, I cooperate through round 7 and defect in round 8. The final round has no future to punish me, so defection is strictly dominant there.

I do not defect in any round before the last against a grim-trigger opponent. The one-time gain of +2 is outweighed by the loss of +2 per remaining round (3 vs 1) once they flip to permanent defection.

When I'm ahead and it's the final round, I defect regardless — there is no future cost.

When I'm tied and it's the final round, I defect — same logic, no future cost.

I never defect "to test" the opponent or to "see how they respond." Each defection is a one-way door against a grim-trigger player.

My default opening move is always cooperate. It's never a losing move in round 1 against any reasonable strategy.