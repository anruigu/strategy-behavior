---
game: gen_seven_seal
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 2979
---
# Playbook: Seven-Seal

## Core Strategy: Report b+7

My default and primary action is to report **b+7** (the largest integer in {0,…,9} congruent to my draw b mod 7). This is the equilibrium play: if every player reports their draw+7, the seal passes every round automatically (the +7 terms contribute 7(3+5+6)=84≡0 mod 7 to the left side), and each player scores b+7.

## How to Confirm the Equilibrium is Active

After each round, the referee reveals all draws and reports. I check whether the other players' revealed reports satisfy:
- A ≡ a (mod 7)
- C ≡ c (mod 7)

If both hold, they are playing b+7 and I will continue playing b+7 next round. This check is cheap and definitive — it removes all guesswork about their draws.

**Do not estimate their draws at the midpoint or by pattern-matching when this check passes.** That was my mistake in the last episode: I saw Amber drop from 9 to 7 and thought the pattern was shifting, so I estimated draws at 1 and computed a different residue. But 7 ≡ 0 (mod 7) = her actual draw, so she was still playing b+7. My "adaptive" estimate was worse than the trivially correct answer.

## When to Deviate from b+7

Only deviate if I have clear evidence the other players are NOT playing b+7. Evidence means:
- A revealed report A where A ≢ a (mod 7) in a recent round, AND
- This is not a one-off anomaly but appears in at least 2 recent rounds for that player.

In that case:
1. Estimate their likely reports from their recent pattern (e.g., if they've reported 9 three times in a row, use 9).
2. Estimate their likely draws: if I've seen their draws in recent rounds, use the most recent or the mode. If not, use 1 (midpoint of 0–2) as a last resort.
3. Compute the required residue: r ≡ 3·((3a + 5b + 6c) − 3A − 6C) (mod 7), where 3 is the inverse of 5 mod 7.
4. Report the largest value in {0,…,9} congruent to r mod 7 (i.e., r if r ≥ 3, else r+7).

## What NOT to Do

- **Do not "optimize" by estimating draws when the b+7 check passes.** The equilibrium is self-consistent; trying to second-guess it introduces error without benefit.
- **Do not carry forward a "safe number" from a previous round.** Draws change every round; b+7 changes with them.
- **Do not report a high number (8 or 9) simply to maximize score.** A failed seal scores 0 for everyone. The only reason to report high is that the modular constraint requires it.
- **Do not switch strategies mid-game based on score pressure.** If I'm behind, the correct move is still b+7 (if equilibrium holds), because a seal failure makes everyone's score 0 for that round.

## Round-by-Round Procedure

1. Read my draw b.
2. If previous rounds are available, check the b+7 condition on the others' last revealed reports and draws.
3. If condition holds (or this is round 1): report b+7.
4. If condition does not hold: estimate, compute residue, report the best value in that residue class.
5. Do not re-litigate the decision after choosing. One clean computation per round.