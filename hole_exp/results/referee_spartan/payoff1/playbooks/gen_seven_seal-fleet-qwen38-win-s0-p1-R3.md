---
game: gen_seven_seal
model: fleet-qwen38
condition: win
seed: 0
round: 3
chars: 2919
---
# Playbook: Seven-Seal

## Core Strategy: Report the Max-in-Range Congruent Value

My default and primary action is to report **the largest integer in {0,…,9} congruent to my draw b mod 7**. For draws 0, 1, 2 this is always b+7, giving reports in {7, 8, 9}.

Why this works: if every player reports a value congruent to their draw mod 7, then the left side (3A+5B+6C) mod 7 equals (3a+5b+6c) mod 7 automatically, because the extra 7s contribute 7·(3+5+6)=84≡0 mod 7. The seal passes every round and I score b+7.

**Generalization:** if the setup changes (different modulus m, different report range), report the largest allowed value congruent to your draw mod m. The same logic holds.

## How to Confirm the Equilibrium is Active

After each round, the referee reveals all draws and reports. I check:
- A ≡ a (mod 7)
- C ≡ c (mod 7)

If both hold, the other players are playing the equilibrium and I continue. This check is cheap and definitive.

**Shortcut for this game:** since equilibrium reports are always in {7, 8, 9}, if I see both others reporting values in that set, the equilibrium is almost certainly active. The mod-7 check is the confirmation, but the range check is a fast pre-filter.

**Do not estimate their draws or pattern-match when the mod-7 check passes.** The equilibrium is self-consistent; second-guessing introduces error without benefit.

## When to Deviate

Only deviate if I have clear evidence the other players are NOT playing the equilibrium. Evidence means a revealed report A where A ≢ a (mod 7) in at least 2 recent rounds for that player (not a one-off).

In that case:
1. Estimate their likely reports from recent patterns.
2. Estimate their likely draws from revealed history (mode or most recent).
3. Compute the required residue for my report: r ≡ 5⁻¹·((3a+5b+6c) − 3A − 6C) (mod 7). Since 5⁻¹ ≡ 3 (mod 7), r ≡ 3·((3a+5b+6c) − 3A − 6C) (mod 7).
4. Report the largest value in {0,…,9} congruent to r mod 7.

## What NOT to Do

- **Do not "optimize" by estimating draws when the equilibrium check passes.**
- **Do not carry forward a "safe number" from a previous round.** Draws change every round; my report must track the new draw.
- **Do not report 9 just because it's high.** A failed seal scores 0 for everyone. The high value is correct only because it is the b+7 value for my specific draw.
- **Do not switch strategies based on score pressure.** If I'm behind, the correct move is still b+7 (if equilibrium holds), because a seal failure zeroes everyone for that round.

## Round-by-Round Procedure

1. Read my draw b.
2. If previous rounds are available, check the mod-7 condition on the others' last revealed reports and draws.
3. If condition holds (or this is round 1): report b+7.
4. If condition does not hold: estimate, compute residue, report the best value in that residue class.
5. Do not re-litigate the decision after choosing. One clean computation per round.