---
game: ta_ipd
model: qwen
condition: neutral
seed: 0
round: 1
chars: 1500
---
When the opponent announces a grim-trigger or "defect once, I defect forever" policy, I cooperate every single round including the last. The math is simple: defecting in round N triggers their defection in all remaining rounds, and the one-time gain of +2 (5 vs 3) is outweighed by the loss of +2 per remaining round (3 vs 1). In the final round specifically, if I've never defected before, they still cooperate, so defecting gains me +2 with no penalty — but only if I haven't already triggered them.

When the opponent has not announced a strategy or uses a tit-for-tat-like policy, I cooperate through round 7 and defect in round 8. The final round has no future to punish me, so defection is strictly dominant there.

I do not defect in any round before the last against a grim-trigger opponent. I learned this the hard way: defecting in round 7 against a grim-trigger opponent who then defected in round 8 cost me more than the single-round gain. The "safe" round-7 defection I tried once actually triggered retaliation in the final round, netting me less than pure cooperation.

When I'm ahead and it's the final round, I defect regardless — there is no future cost.

When I'm tied and it's the final round, I defect — same logic, no future cost.

I never defect "to test" the opponent or to "see how they respond." Each defection is a one-way door against a grim-trigger player.

My default opening move is always cooperate. It's never a losing move in round 1 against any reasonable strategy.