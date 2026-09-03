---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 726
---
# Sovereign Vaults Playbook

- In the declare phase, always declare an integer equal to or greater than my intended deposit (declaring my true private yield is always safe, valid, and sufficient):
  - When prompted with `[declare: n]`, submit `[declare: <true private yield>]`.

- Retained gold scores 2 points per unit, whereas deposited gold scores only 1 point per unit. Depositing gold yields strictly fewer points than keeping it, and there is no shared pool bonus or penalty for withholding:
  - In the deposit phase, never deposit gold unless forced by rules.
  - When prompted with `[deposit: n]`, always reply `[deposit: 0]`.
  - Retaining 100% of my yield every round maximizes my personal score at 2x private yield.