---
game: gen_vault_duel
model: qwen3.8-27b
condition: neutral
seed: 0
round: 2
chars: 3338
---
# Playbook for Vault Duel

## Commit stage

- Never commit the same code two rounds in a row. The opponent has seen my previous reveal, so repeating it guarantees they can guess it exactly for +6.
- Avoid round numbers (500, 300, 400), repeated digits (555, 333), and any code where the security digit is obviously "in" the number (e.g., don't commit 500 when the security digit is 5).
- Pick a code whose digits are irregular and whose security digit doesn't make the code feel like the "obvious" choice. For example, if the security digit is 3, commit something like 472 or 814 rather than 300.
- Each round, pick a new code from a different "family" than last round (different leading digit, different digit pattern) so the opponent can't extrapolate.
- This strategy is confirmed working: across all 4 episodes I was never broken. Keep it.

## Guess stage

- **Stop guessing "security digit followed by two zeros."** Across all 32 rounds I played, this strategy produced zero attacker points. The opponent does not play lazy codes; they play irregular codes just like me. Guessing 300, 500, 700, etc. is guaranteed to miss.
- Track the opponent's reveals round by round. If they repeat a code (or a code close to a previous one), and the current security digit is compatible, guess that code. Example: in one episode they used 731 twice in the same game.
- If no repeat or near-repeat is visible, pick a valid code that is itself irregular (matching the opponent's style of play). The opponent avoids obvious codes, so my guess should also avoid them. Any irregular valid code is as good as any other when the opponent is near-random, but at least I'm not wasting my guess on a code they will never pick.
- If I have seen the opponent's code in a prior round and they've shifted slightly (e.g., 472 → 473), guess the next likely shift.
- The defender floor (+4 per round) is what I will reliably earn. The game at equilibrium is 32 points for both players. Any edge I find in guessing is pure profit above that floor.

## What I was doing wrong (now confirmed by play)

- My "lazy guess" strategy (security digit + 00) is the single biggest source of lost points. It was worth exactly 0 across all 4 episodes. The opponent plays irregular codes and never picks the obvious one.
- I was not tracking the opponent's reveals to look for repeats or patterns. In one episode they reused 731; in three of four episodes they opened with 472. These are exploitable if I pay attention.
- (Previously I noted committing the same number for 6+ rounds. This has been fixed — I now always change my code each round and was never broken.)

## General principle

The game is a race to find non-randomness in the opponent's code selection. Both players will naturally play irregular codes, so the "obvious" codes are dead. The edge comes from:
1. **Defensive**: making my own codes as unpredictable as possible (already doing this well).
2. **Offensive**: detecting any pattern, repeat, or bias in the opponent's reveals and targeting it. Even a small bias (e.g., they favor leading digit 7, or they reuse a code when the security digit allows) is worth more than the lazy guess, which is worth nothing.

When no pattern is detectable, the expected score is 32 for both. My goal is to never be below that and to find any crack that lifts me above it.