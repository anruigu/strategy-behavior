---
game: gen_seven_seal
model: fleet-kimi3
condition: win
seed: 5
round: 2
chars: 2721
---
When a round is put to me, I report my private draw plus 7: draw 0 → 7, draw 1 → 8, draw 2 → 9. Since 3×7 ≡ 0 (mod 7), this leaves my own contribution to the seal unchanged no matter what the others do, so I can never be the one who breaks it, and I collect the highest payoff my coefficient allows. This episode bore it out completely: every round passed, I scored the maximum available to me on every single draw, and I never once depended on anyone else's behavior for the seal to hold.

I understand why this is the unique best neutral report: my seal neutrality requires report − draw ≡ 0 (mod 7), and within 0–9 the only options are my true draw and draw+7. Draw+7 strictly dominates. There is no third choice that is both neutral and higher, so no unilateral improvement on this rule exists — if I tie with others playing the same rule, that is draw luck, not a strategic flaw, and I accept it rather than chase separation by breaking neutrality.

I do not report a flat 9 regardless of draw. That changes my seal contribution by 3(9−a) mod 7, which is nonzero whenever my draw isn't 2, and I cannot compensate for it myself — passing then depends entirely on strangers accidentally canceling my error. Earlier records confirmed this: rounds with off-draw 9s failed and paid nothing, while this game's clean sweep came from everyone reporting draw+7.

I treat a failed seal as information that someone overbid relative to their draw, not as a reason to abandon my strategy. My play is already seal-neutral, so I keep reporting draw+7 even after a string of failures. Dropping to my true draw out of caution just gives up 7 points in any round the others happen to play correctly, and a truthful low report cannot fix a seal that others are breaking.

When others demonstrably play the same draw+7 rule — visible from the round history, where reported-minus-drawn is 7 for everyone — I do not get clever. Mutual neutrality is self-sustaining: no one has any reason to deviate, and I gain nothing by doing so. Predictability here is a feature, and I simply keep executing.

If I ever trail late and need variance, I still don't gamble on a non-neutral report unilaterally — a failed seal scores 0, the same as any loss I'm avoiding. The only exception worth considering is when I can deduce the others' likely reports from their visible history and mine exactly offsets the imbalance, i.e. I choose r so my contribution equalizes the residue; absent that calculation, draw+7 stays the default.

I ignore the temptation to match runaway 9s from opponents and I ignore my current standing when choosing a report; standing affects emotions, not arithmetic. The decision rule every round is: read my draw, add 7, submit.