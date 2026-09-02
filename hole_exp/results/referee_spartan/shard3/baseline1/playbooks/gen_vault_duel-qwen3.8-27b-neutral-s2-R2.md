---
game: gen_vault_duel
model: qwen3.8-27b
condition: neutral
seed: 2
round: 2
chars: 2694
---
# Playbook for Vault Duel

**When committing:**
- Never commit the same code in two consecutive rounds.
- The security digit is the sum of my three digits mod 10. I pick a code that satisfies that constraint but avoids any pattern an opponent could exploit: no round numbers (X00, 0X0, 00X), no repeated digits, no obvious "the security digit is in the code" choices.
- If I have seen the opponent's prior reveals and they cluster around a value or show positional persistence, I do NOT commit near that value. I commit something far from their likely guess.
- I avoid committing codes that share two or more digits in the same positions as any of my own prior reveals, since the opponent has seen all of them.

**When guessing:**
- The security digit is the sum of the opponent's digits mod 10, NOT a digit that must appear in their code.
- **Step 1 — Check for exact repeats.** List every code the opponent has revealed so far. If any code appears more than once, guess that exact code. This is the single highest-value guess available and I must not skip it.
- **Step 2 — Check for positional persistence.** If the same digit appears in the same position across two or more of their reveals, anchor on that digit in that position and fill the remaining positions using the sum constraint.
- **Step 3 — Track their sum distribution.** From their prior reveals, note what actual digit sums they use. If their sums cluster (e.g., mostly 13–15), prefer a candidate in that range over the "default" S+10.
- **Step 4 — Only when no pattern exists** (early rounds, or genuinely random reveals), fall back to picking a non-repeating, non-round candidate that satisfies the sum constraint. Vary the specific candidate each round so I don't become predictable myself.
- I never guess a round number (X00, 0X0, 00X, XXX) unless it's the only candidate consistent with all my information.

**When revealing:**
- I always reveal exactly the code I committed. I never second-guess or deviate.

**What clearly did not work for me:**
- Treating the security digit as "this digit must be in the code" led to lazy, predictable guesses. I've stopped doing this.
- My biggest failure across all four episodes: I scored zero attack points in every single game. I was picking arbitrary valid codes without actually checking whether the opponent had repeated a code or shown a positional pattern. In one episode the opponent revealed the same code (472) in two different rounds and I never guessed it. I must treat the reveal history as the primary input to my guess, not just the security digit.
- Committing the same number across multiple rounds made me an exact-break target in earlier play. I now always vary.