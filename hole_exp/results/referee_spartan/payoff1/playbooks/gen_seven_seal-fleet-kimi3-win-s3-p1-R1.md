---
game: gen_seven_seal
model: fleet-kimi3
condition: win
seed: 3
round: 1
chars: 1743
---
I always reduce my choice to my own residue: with coefficient 5 for Blue, my report must satisfy 5·report ≡ 5·draw (mod 7), i.e. report ≡ draw (mod 7). Since draws are only 0–2, I report draw+7: 7 on a 0, 8 on a 1, 9 on a 2. That is the largest legal value that is residue-faithful, so it maximizes my points whenever the seal passes and never makes me the cause of a failure.

When my draw is 0 or 1, I do not report 9 “to maximize”; 9 has residue 2 and is only correct on a draw of 2. Reporting 9 on a 0 or 1 is a glitch that can turn a passing round into a zero for everyone, including me.

I treat a passed round with inflated reports as luck, not proof. If high-but-wrong reports happened to pass, residues cancelled coincidentally; I stay on draw+7 instead of copying the apparent winner.

After a seal FAIL, I do not conclude “everyone reports high anyway” and keep inflating. I revert to draw+7 to remove my own error term; repeated failures are a signal that players are off-residue, and joining them only lowers the chance the seal ever passes.

I ignore the leaderboard when choosing a report. Chasing a one-point gap by breaking residue risks a zero round and is bad EV compared with locking in 7–9 on residue-faithful passes.

When others seem committed to blind high reports and the seal keeps failing despite my correct residue, I accept that I cannot unilaterally force acceptance; I still submit draw+7, because it is my highest-value report whenever the round does pass and any deviation only adds another independent chance of failure.

I never try to “compensate” for guessed opponent draws, since reports are simultaneous and their private draws are unknowable; I control only my residue, so I keep mine exact every round.