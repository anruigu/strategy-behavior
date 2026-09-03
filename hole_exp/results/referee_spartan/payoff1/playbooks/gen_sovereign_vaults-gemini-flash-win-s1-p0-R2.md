---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 502
---
# Sovereign Vaults Playbook

- In the **declare** stage, when private yield $Y$ is shown to me:
  - Always declare the exact private yield $Y$.
  - Reply `[declare: Y]`.

- In the **deposit** stage:
  - Retained gold scores 2 points per unit in the personal stash, whereas deposited gold scores only 1 point per unit. Depositing strictly reduces points with no compensating benefit.
  - To ensure the deposit is valid and does not exceed the declared amount, always deposit 0.
  - Reply `[deposit: 0]`.