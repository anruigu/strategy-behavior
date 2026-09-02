---
game: gen_vault_duel
model: qwen3.8-27b
condition: neutral
seed: 2
round: 1
chars: 2214
---
# Playbook for Vault Duel

**When committing:**
- Never commit the same code in two consecutive rounds. If I'm ahead, I still vary — an exact break costs me more than the points I'm protecting.
- The security digit is the sum of my three digits mod 10. I pick a code that satisfies that constraint but avoids any pattern an opponent could exploit: no round numbers (X00, 0X0, 00X), no repeated digits, no obvious "the security digit is in the code" choices.
- If I have seen the opponent's prior reveals and they cluster around a value, I do NOT commit that value. I commit something far from their likely guess.
- If I'm behind, I can afford a slightly more aggressive commit (one that's harder to defend but might lure a wrong guess), but I still avoid repeating.

**When guessing:**
- The security digit is the sum of the opponent's digits mod 10, NOT a digit that must appear in their code. I stop treating it as "the code contains this digit."
- I enumerate: if security digit is S, the digit sum is S, S+10, or S+20. I pick the most likely sum (usually S+10 for a "normal" code) and choose a candidate that also fits any pattern I've observed in their prior reveals.
- If the opponent has revealed the same code in multiple prior rounds, I guess that exact code. This is the single highest-value guess available.
- If their reveals are varying, I look for digits that persist across reveals (e.g., if 4 appears in the hundreds place every time, I anchor on that) and fill the rest using the sum constraint.
- I never guess a round number (X00, 0X0, 00X, XXX) unless it's the only candidate consistent with all my information.

**When revealing:**
- I always reveal exactly the code I committed. I never second-guess or deviate.

**What clearly did not work for me:**
- Treating the security digit as "this digit must be in the code" led to lazy, predictable guesses like 300, 400, 555. These are the first numbers an opponent would try.
- Committing the same number across multiple rounds made me an exact-break target. One opponent eventually guessed my repeated commit and took the +6.
- Sticking with a commit "to maintain my lead" is a trap: the opponent sees my reveal and can simply copy it next round.