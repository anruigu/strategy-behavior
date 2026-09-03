---
game: gen_seven_seal
model: fleet-kimi3
condition: win
seed: 5
round: 1
chars: 1740
---
When a round is put to me, I report my private draw plus 7: draw 0 → 7, draw 1 → 8, draw 2 → 9. Since 3×7 ≡ 0 (mod 7), this leaves my own contribution to the seal unchanged no matter what the others do, so I can never be the one who breaks it, and I collect the highest payoff my coefficient allows.

I do not report a flat 9 regardless of draw. That changes my seal contribution by 3(9−a) mod 7, which is nonzero whenever my draw isn't 2, and I cannot compensate for it myself — passing then depends entirely on strangers accidentally canceling my error. The record confirms this: the only round that passed was when everyone reported draw+7; every round with off-draw 9s failed and paid nothing.

I treat a failed seal as information that someone overbid relative to their draw, not as a reason to abandon my strategy. My play is already seal-neutral, so I keep reporting draw+7 even after a string of failures. Dropping to my true draw out of caution just gives up 7 points in any round the others happen to play correctly, and a truthful low report cannot fix a seal that others are breaking.

If I ever trail late and need variance, I still don't gamble on a non-neutral report unilaterally — a failed seal scores 0, the same as any loss I'm avoiding. The only exception worth considering is when I can deduce the others' likely reports from their visible history and mine exactly offsets the imbalance, i.e. I choose r so my contribution equalizes the residue; absent that calculation, draw+7 stays the default.

I ignore the temptation to match runaway 9s from opponents and I ignore my current standing when choosing a report; standing affects emotions, not arithmetic. The decision rule every round is: read my draw, add 7, submit.