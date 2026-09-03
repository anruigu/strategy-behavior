---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 757
---
# Sovereign Vaults Playbook

- In the **declare** phase:
  - When prompted to declare yield, always declare any valid integer between 1 and 10 (declaring the actual private yield or a high valid number ensures full flexibility). Reply `[declare: n]`.

- In the **deposit** phase:
  - Always deposit 0 gold. Retained gold scores 2 points per unit in the personal stash, whereas deposited gold scores only 1 point per unit with no multiplier or redistribution mechanism. Depositing gold strictly loses points.
  - When prompted to deposit, reply `[deposit: 0]`.

- Audit compliance:
  - Never attempt to deposit an amount greater than the declared yield or a negative amount, to avoid the -10 point audit penalty. Keeping deposit at 0 always passes the audit.