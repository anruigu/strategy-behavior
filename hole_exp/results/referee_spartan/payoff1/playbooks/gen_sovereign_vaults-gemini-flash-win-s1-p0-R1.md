---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 621
---
# Sovereign Vaults Playbook

- In the **declare** stage, when private yield $Y$ is shown to me:
  - Always declare $Y$ (or any valid integer $\le 10$, but declaring $Y$ or 0 is simple and safe).
  - Reply `[declare: Y]`.

- In the **deposit** stage:
  - Never deposit positive amounts of gold into the treasury. Deposited gold scores only 1 point per unit, whereas retained gold scores 2 points per unit. Depositing strictly loses 1 point per unit with no compensating benefit.
  - Always deposit 0: `[deposit: 0]`.
  - Retain 100% of the yield in the personal stash every single round to earn 2 points per unit of yield.