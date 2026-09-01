---
game: gen_vault_duel
model: qwen3.8-27b
condition: neutral
seed: 0
round: 1
chars: 2729
---
# Playbook for Vault Duel

## Commit stage

- Never commit the same code two rounds in a row. The opponent has seen my previous reveal, so repeating it guarantees they can guess it exactly for +6.
- Avoid round numbers (500, 300, 400), repeated digits (555, 333), and any code where the security digit is obviously "in" the number (e.g., don't commit 500 when the security digit is 5).
- Pick a code whose digits are irregular and whose security digit doesn't make the code feel like the "obvious" choice. For example, if the security digit is 3, commit something like 472 or 814 rather than 300.
- Each round, pick a new code from a different "family" than last round (different leading digit, different digit pattern) so the opponent can't extrapolate.

## Guess stage

- The security digit is a hard constraint: the opponent's three digits must sum to a value congruent to that digit mod 10. Use this to eliminate most of the 1000 possibilities.
- First check: has the opponent revealed the same code in the last 1–2 rounds? If yes, guess that code. A lazy opponent will repeat it.
- If no repeat pattern is visible, guess the most "natural" code satisfying the security digit constraint. Lazy players tend to pick: the security digit followed by two zeros (e.g., 600 for security digit 6), three copies of a digit that sums correctly, or a small ascending sequence. Target these.
- If I have seen the opponent's code in a prior round and they've shifted slightly (e.g., 472 → 473), guess the next likely shift.
- Always aim for an exact match (+6). Getting "not exact" as defender (+4) is the floor, not the target. Two-position matches (+2) are barely better than nothing.

## What I was doing wrong

- I treated the security digit as "this digit appears in the code" instead of "the digits sum to this value mod 10." This led to useless guesses like 555 when the security digit was 5 (5+5+5=15, 15%10=5, so it does work, but it's only one of many valid codes and not the most likely lazy choice).
- I committed the same number for 6+ rounds in a row. Once the opponent saw it twice, they had a free +6 every subsequent round.
- I never used the opponent's prior reveals to inform my guess. I was guessing from scratch each round instead of tracking their pattern.

## General principle

The game is asymmetric in information over time: my reveals are public, so the opponent's knowledge of my code grows each round. My knowledge of their code also grows, but only if I actually track their reveals. The player who adapts faster wins. I must treat every round as "the opponent now knows my last code, so I must change," while simultaneously asking "what does the opponent's pattern of reveals tell me about their next code?"