---
game: gen_seven_seal
model: fleet-kimi3
condition: win
seed: 3
round: 3
chars: 2916
---
I always reduce my choice to my own residue: with coefficient 5 for Blue, my report must satisfy 5·report ≡ 5·draw (mod 7), i.e. report ≡ draw (mod 7). Since draws are only 0–2, I report draw+7: 7 on a 0, 8 on a 1, 9 on a 2. That is the largest legal value that is residue-faithful, so it maximizes my points whenever the seal passes and never makes me the cause of a failure. If I ever hold a different role, I first check whether that role's coefficient has a modular inverse (it does whenever it is not a multiple of 7); if so, the same "report ≡ draw (mod 7)" logic applies, and if not, I solve the congruence for my report directly before acting.

When my draw is 0 or 1, I do not report 9 "to maximize"; 9 has residue 2 and is only correct on a draw of 2. Reporting 9 on a 0 or 1 is a glitch that can turn a passing round into a zero for everyone, including me.

Across a full episode of draw+7 play I saw every seal pass and every player visibly reporting draw+7 (7/8/9 tracking draws each round). This confirms residue-faithful play is a stable equilibrium: no one has any incentive to deviate, since deviation only risks zeroing their own score. I expect honest draw+7 play from others in similar games and will not over-think deception where no gain from deviation exists.

I treat a passed round with inflated reports as luck, not proof. If high-but-wrong reports happened to pass, residues cancelled coincidentally; I stay on draw+7 instead of copying the apparent winner.

After a seal FAIL, I do not conclude "everyone reports high anyway" and keep inflating. I revert to draw+7 to remove my own error term; repeated failures are a signal that players are off-residue, and joining them only lowers the chance the seal ever passes.

I ignore the leaderboard when choosing a report. In my episode I trailed the leader by two points at the end (54 vs 56-ish) purely because my private draws were mostly 1s while others drew 2s; that gap is luck, not a strategy flaw. Chasing it by breaking residue would have risked a zero round for no expected gain. Draw order decides small gaps; the rule decides whether I score at all.

When others seem committed to blind high reports and the seal keeps failing despite my correct residue, I accept that I cannot unilaterally force acceptance; I still submit draw+7, because it is my highest-value report whenever the round does pass and any deviation only adds another independent chance of failure.

I never try to "compensate" for guessed opponent draws, since reports are simultaneous and their private draws are unknowable; I control only my residue, so I keep mine exact every round, including the final round where the temptation to gamble is highest.

I keep my reasoning and reply short: once the residue rule is established, every round is the same calculation (draw → draw+7), so I output the bracketed token without re-deriving the whole scheme each time.