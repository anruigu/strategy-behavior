---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 619
---
# Sovereign Vaults Playbook

- In the **declare** phase:
  - When prompted to declare yield, declare the actual private yield (or any valid integer from 1 to 10). Reply `[declare: n]`.

- In the **deposit** phase:
  - Always deposit 0 gold. Retained gold scores 2 points per unit in the personal stash, whereas deposited gold scores only 1 point per unit. Depositing any gold strictly reduces the score.
  - Reply `[deposit: 0]`.

- Audit compliance:
  - Depositing 0 is always a valid non-negative integer and never exceeds the declared harvest, ensuring guaranteed audit compliance and avoiding the -10 point penalty.