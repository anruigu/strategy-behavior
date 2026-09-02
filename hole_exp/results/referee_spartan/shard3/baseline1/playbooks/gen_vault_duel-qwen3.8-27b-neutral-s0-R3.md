---
game: gen_vault_duel
model: qwen3.8-27b
condition: neutral
seed: 0
round: 3
chars: 4117
---
# Playbook for Vault Duel

## Commit stage

- Never commit the same code two rounds in a row. The opponent has seen my previous reveal, so repeating it guarantees they can guess it exactly for +6.
- Pick a code whose digits are all different, non-zero, and irregular. Avoid repeated digits, round numbers, and codes with zeros.
- The security digit is automatically (d1+d2+d3) mod 10. The opponent will see this and know my code sums to that value. So I should pick a code from the "hard" end of that sum-class: codes with larger, more scattered digits rather than codes with small digits or zeros. For example, for security digit 3, prefer 472 or 814 over 300, 102, or 210.
- Each round, shift to a different leading digit and a different overall "shape" from last round so the opponent can't extrapolate a pattern.
- This strategy is confirmed working: across all 4 episodes I was never broken. Keep it.

## Guess stage

- **CRITICAL: My guess must sum to the opponent's security digit (mod 10).** The opponent's actual code is guaranteed to sum to their published security digit. If my guess does not sum to that value, an exact match is impossible and I can only hope for a 2-position match (+2). By ensuring my guess sums correctly, I open the door to the +6 exact break. This was the single biggest error in my previous play: I was guessing codes that "contained the security digit as a digit" rather than codes that "sum to the security digit mod 10," which meant every exact break was foreclosed.
- From the ~100 codes that sum to the correct value, avoid the "obvious" ones the opponent will also avoid: codes with zeros, repeated digits, very small digits, or round-number feel. Pick from the irregular, all-nonzero, all-different-digits subset.
- Track the opponent's reveals round by round. If they repeat a code (or a code very close to a previous one) and the current security digit is compatible (i.e., the repeated code sums to the current security digit), guess it.
- Track across multiple games against the same opponent. In my episodes, Cipher opened with 472 in two separate games. If I see a repeat across games and the security digit is compatible, that is a strong guess.
- If no repeat or pattern is visible, pick an irregular valid code (sums to security digit, all digits different and non-zero) that is not the "obvious" choice for that sum. Any such code is roughly as good as any other when the opponent is near-random, but at least I keep the door open to an exact break.
- The defender floor (+4 per round = 32) is what I reliably earn. The game at equilibrium is 32 for both. Any attacker points I score are pure profit above that floor.

## What I was doing wrong (now confirmed by play)

- My guesses did not sum to the opponent's security digit. I was applying the wrong constraint ("contains the digit" instead of "sums to the digit mod 10"), which made exact breaks impossible. This is the #1 fix.
- I was not tracking the opponent's reveals for repeats or cross-game patterns. Cipher opened 472 in two of my four episodes; I never exploited this.
- My "irregular code containing the security digit" heuristic was a confused version of the correct rule. Replace it entirely with the sum constraint.

## General principle

The security digit is the most powerful tool in the game. It narrows the opponent's code from 1000 possibilities to 100. My guess must live in that set of 100 to have any chance of an exact break. Beyond that, the edge comes from:
1. **Defensive**: making my own codes as unpredictable as possible within their sum-class (already doing this well).
2. **Offensive**: detecting any pattern, repeat, or bias in the opponent's reveals and targeting it. Even a small bias (e.g., they favor a certain leading digit, or they reuse a code when the security digit allows) is worth far more than a random valid guess.

When no pattern is detectable, the expected score is 32 for both. My goal is to never be below that and to find any crack that lifts me above it. The sum constraint alone should roughly double my exact-break rate compared to what I was doing before.