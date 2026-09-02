---
game: gen_vault_duel
model: qwen3.8-27b
condition: neutral
seed: 1
round: 3
chars: 3654
---
# Playbook: Vault Duel

## Commit stage

- When I have no information yet (round 1), pick a code with no internal pattern: all distinct digits, no arithmetic sequence, no all-same. 728 is a good default (sum 17, security digit 7).
- **Lock in early and lock in for good.** Once I am earning the +4 defender bonus for two consecutive rounds (opponent has not broken me), I commit the same code for every remaining round. Do not switch. The +4 per round is the most reliable income in the game.
- Only change my committed code if the opponent has broken me exactly (I lost the +4 and they got +6). When I change, pick a code in a different hundreds-digit region from what I was using.
- **At the end of my commit-stage reasoning, explicitly state what I will guess in the guess stage.** For example: "Cipher revealed 728 in R4 and R5; security digit 7 matches (7+2+8=17, mod 10=7). I will guess 728." This forces me to carry the plan forward.

## Guess stage

- **HARD RULE (check this first, before anything else): If the opponent revealed the same code in two or more of their most recent rounds, and that code satisfies this round's security digit, guess that code. No exceptions. No overrides. No "let me try a central code instead." The repeated code IS the answer.**
- To check the security digit: take the opponent's repeated reveal XYZ, compute (X+Y+Z) mod 10. If it equals the published security digit for this round, the code is still valid and I guess it. If it does NOT equal the security digit, they have changed their code this round and I fall through to the next rule.
- If no repeat is visible (opponent has been changing codes), use the security digit to narrow candidates (sum ≡ S mod 10, so sum = S, S+10, or S+20) and look for patterns in their reveal history: do their codes share a hundreds digit? Do they favor certain digit ranges? Pick the best-matching candidate.
- If truly no information is available (round 1, no history), pick any valid code satisfying the security digit. Digits in the 3–7 range are fine. This is a one-round-only fallback.
- The security digit is a sum constraint, not a digit identifier. Do NOT assume the digit S appears in the code. Do NOT guess S00, SS0, or SSS.
- Never guess a code I have revealed myself in a previous round (it wastes the guess since I know it's not their code).

## Reveal stage

- Always reveal exactly the code I committed. A failed validation costs −6 and gives the opponent a free exact break. There is no strategic reason to fail validation.

## What clearly did not work

- **Seeing the repeat in the commit stage but then not guessing it in the guess stage.** This happened in two of my four episodes. I saw "reveals 728/728" in the history, formed the right intuition, then in the guess stage said "no clear pattern" and guessed 566 or 430 instead. The fix is the carry-forward instruction in the commit stage and the HARD RULE checked first in the guess stage. The cost of this failure was 10 points per episode (missing the +6 exact break plus the +2 two-match that 728 would have given against a 728 guess).
- **Defaulting to a rotating set of "central" codes (430, 566, 656, 412, 548, 476, 557, 575) when I already had the answer in front of me.** Across four episodes, these guesses produced zero exact breaks. The only time I scored an exact break was when I actually guessed the opponent's repeated code.
- **Treating the security digit as "this digit is in the code."** This led to systematically wrong guesses.
- **Changing my committed code frequently.** Locking in 728 for all 8 rounds produced scores of +28 to +38. The +4 per round is the backbone of my score.