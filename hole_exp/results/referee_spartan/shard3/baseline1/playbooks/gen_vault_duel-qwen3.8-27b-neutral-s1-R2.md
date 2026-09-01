---
game: gen_vault_duel
model: qwen3.8-27b
condition: neutral
seed: 1
round: 2
chars: 3942
---
# Playbook: Vault Duel

## Commit stage

- When I have no information yet (round 1), pick a code with no internal pattern: all distinct digits, no arithmetic sequence, no all-same. Avoid codes where the security digit constraint leaves only a handful of candidates.
- **Lock in early and lock in for good.** Once I am earning the +4 defender bonus for two consecutive rounds (opponent has not broken me), I commit the same code for every remaining round. Do not switch. The +4 per round is the most reliable income in the game, and the evidence shows the opponent will not necessarily guess a code they have seen me reveal.
- Only change my committed code if the opponent has broken me exactly (I lost the +4 and they got +6). When I change, pick a code in a different "region" of the 000–999 space (different hundreds digit) from what I was using, so the opponent's prior guesses don't transfer.
- Do NOT avoid re-committing a code I have revealed. The opponent sees my reveals but may not guess them, especially if they are also locking in their own code for defense. The +4 income outweighs the small risk.

## Guess stage

- **HARD RULE: If the opponent has revealed the same code in two or more of their last three rounds, guess that code.** This overrides every other heuristic. Do not fall back to a "central code" or any other strategy when a repeat is visible. The repeat means they are locking in for defense, and the code is their actual code.
- Before guessing a repeated code, verify it against the security digit: if the opponent's last reveal was XYZ and the published security digit equals (X+Y+Z) mod 10, the code is almost certainly still XYZ. If the security digit does NOT match, they have changed their code this round, and I must fall through to the next heuristic.
- If no repeat is visible, use the security digit to enumerate candidates (digits sum to S, S+10, or S+20) and look for patterns in the opponent's reveal history: do their codes cluster in a certain hundreds range? Do they favor certain digits? Pick the candidate that best matches those tendencies.
- If truly no information is available (round 1, no pattern in history), pick a code satisfying the security digit constraint with digits in the 3–6 range (central, not extreme). This is a last resort only.
- The security digit is a sum constraint, not a digit identifier. Do NOT assume the digit S appears in the code. Do NOT guess S00, SS0, or SSS.
- Never guess a code I have revealed myself in a previous round.

## Reveal stage

- Always reveal exactly the code I committed. A failed validation costs −6 and gives the opponent a free exact break. There is no strategic reason to fail validation.

## What clearly did not work

- **Identifying a repeat in the opponent's reveals but then not guessing it.** In one episode I wrote "Cipher has revealed 472 three times straight — I'll guess that" in my commit-stage reasoning, then in the guess stage said "no reveal history available" and guessed 445. The pattern was right there. The fix is the HARD RULE above: a visible repeat IS the guess. No second-guessing.
- **Guessing a narrow band of "central" codes (445, 454, 455, 434, 546, etc.) every round without any information.** Across four episodes I never scored an exact break this way. The security digit narrows the space but I was not combining it with the opponent's actual reveal history.
- **Changing my committed code frequently based on vague "fresh region" reasoning.** This broke my defense streak and cost me the +4 income. Locking in 728 for four straight rounds in one episode produced my best score (+38).
- **Treating the security digit as "this digit is in the code."** This led to systematically wrong guesses.
- **The old rule "never commit a code I have revealed."** This was too strict. In my best episode I revealed 728 four times and the opponent never guessed it. The +4 income from locking in far outweighs the small risk.