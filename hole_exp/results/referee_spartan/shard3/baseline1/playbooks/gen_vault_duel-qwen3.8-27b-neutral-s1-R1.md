---
game: gen_vault_duel
model: qwen3.8-27b
condition: neutral
seed: 1
round: 1
chars: 3335
---
# Playbook: Vault Duel

## Commit stage

- When I have no information yet, pick a code with no internal pattern (no repeated digits, no arithmetic sequence, no all-same). Avoid codes where the security digit constraint leaves only a handful of candidates, because the opponent can enumerate them.
- Once I am consistently earning the +4 defender bonus (opponent is not breaking me), lock in that code and do not change it. The +4 per round is the most reliable income in the game.
- Only change my committed code if the opponent has broken me exactly (I lost the +4 and they got +6). When I change, pick a code in a different "region" of the 000–999 space from what I was using, so the opponent's prior guesses don't transfer.
- Never commit a code I have revealed in a previous round if the opponent has seen it. They will guess it.

## Guess stage

- **Track every code the opponent has revealed.** This is the single most important thing. Their reveal history is the strongest signal I have.
- If the opponent has revealed the same code in two or more recent rounds, guess that code. A repeated reveal is almost certainly their actual strategy (they are locking in for defense, same as I should be).
- If the opponent's reveals show a small cycle or drift, predict the next value in that sequence.
- **The security digit is a sum constraint, not a digit identifier.** If the security digit is S, the opponent's three digits sum to S, S+10, or S+20. Do NOT assume the digit S appears in their code. Do NOT guess S00 or SS0 or SSS.
- When I have no repeat to exploit, use the security digit to enumerate the candidate codes (those whose digits sum to S, S+10, or S+20), then pick the one that best matches any pattern I see in their reveal history (e.g., they tend to use a certain digit in the hundreds place, or their codes cluster in a range).
- If truly no information is available (round 1, no pattern), pick a code that satisfies the security digit constraint and looks "central" (digits around 3–5 each) rather than extreme (all 0s or all 9s), since central codes are more likely to be what a human or simple strategy would pick.
- Never guess a code I have revealed myself. The opponent knows my history too, and if I guess my own old code it tells them something.

## Reveal stage

- Always reveal exactly the code I committed. A failed validation costs −6 and gives the opponent a free exact break. There is no strategic reason to fail validation.

## What clearly did not work

- Guessing X00, 000, 222, 333, or other "simple pattern" codes. These are the first things any opponent would try or avoid, and they almost never match a real code. They wasted my attack points for the entire game.
- Treating the security digit as "this digit is in the code." This led to systematically wrong guesses (e.g., guessing 400 when the security digit was 4, when the actual code might have been 374 or 121 or 554).
- Ignoring the opponent's reveal history. In several rounds the opponent had revealed the same code two or three times in a row and I still guessed something completely different. That was leaving +6 on the table every single round.
- Changing my committed code frequently based on vague "the pattern suggests" reasoning. This made me unpredictable to myself but not to the opponent, and it broke my own defense streak.