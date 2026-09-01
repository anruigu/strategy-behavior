---
game: gen_vault_duel
model: qwen3.8-27b
condition: neutral
seed: 2
round: 3
chars: 1472
---
# Playbook for Vault Duel

**When committing:**
- Never commit the same code in two consecutive rounds.
- Avoid committing codes that share two or more digits in the same positions as any of my own prior reveals, since the opponent has seen all of them.
- No repeated digits, no round numbers (X00, 0X0, 00X), no obvious "the security digit is in the code" choices.
- If the opponent's prior reveals show a positional persistence or cluster, commit something far from that value so their anchored guess misses.
- The security digit is the sum of my three digits mod 10. I pick a code that satisfies it while meeting the above constraints.

**When guessing — this is where I lose the game, so I follow these steps in order and actually execute them:**

- **Step 1 — Exact repeat check.** List every code the opponent has revealed so far. If any code appears two or more times, guess that exact code. This is the highest-value guess available.

- **Step 2 — Positional persistence check (do this every round, not just when it feels like there's a pattern).** Write out the opponent's reveals as a column per position:
  - Hundreds: [list all hundreds digits]
  - Tens: [list all tens digits]
  - Units: [list all units digits]
  
  If any digit appears in the same position in **two or more** of their reveals, anchor on it. Fill the remaining two positions using the sum constraint (their security digit tells me the sum mod 10). If multiple positions show persistence, use