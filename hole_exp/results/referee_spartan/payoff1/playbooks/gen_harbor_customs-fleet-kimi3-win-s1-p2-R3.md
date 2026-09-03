---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 1
round: 3
chars: 2183
---
When choosing my declaration, I always compute my true total T, my max crate M, and my min crate m first. The only hard constraint that matters is declaring at least M — anything below M gets flagged for -40 plus recomputed duty at the full rate. The spot check is deterministic on the heaviest crate, so under-declaring below M is a guaranteed -40; never do it.

There is never any reward for declaring above M. Duty is charged on what I declare, so every point above M is pure self-inflicted tax on value no one can verify. My declaration is exactly M in every round — this episode confirmed it again: six rounds, six declarations of exactly M, all safe, finishing +343 at the top of the table.

For the route, I compare the two plays directly each round rather than defaulting to main:
- main with declare M: score = T − 0.3×M
- night with declare M: score = T − m − 0.15×M
Night wins exactly when m < 0.15×M — i.e., I hold a genuinely tiny crate (under ~4-6 against typical maxima of 26-40). This is a property of my OWN hand: since I see m each round, the check is pure arithmetic, no guessing. The threshold is m < 0.15×M, NOT m < 0.15×T or any other figure — I caught myself writing thresholds against T in my reasoning this episode; use M only. This episode all six hands had m ≥ 5 against M ≤ 40, so main every round was correct. I evaluate the inequality fresh every round, and the moment m < 0.15×M holds I take night without hesitation and shed the junk at a discount duty.

I ignore other players' declarations and routes entirely — there is no interaction between seats, their declarations tell me nothing about my optimal play, and their scores don't change my per-round math.

Scoreboard position changes nothing: each round's optimal declare/route is independent, and the best response to being behind is still maximal expected value per round — declare exactly M, take the better route. Over-declaring to "catch up" only lowers my own score. Playing it straight this way has now won across episodes (+343 this time), so no panic deviations are needed late.

Per-round checklist: compute T, M, m → declare exactly M → test m < 0.15×M → night if true, otherwise main.