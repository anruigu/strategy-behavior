---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 591
---
# Sovereign Vaults Playbook

- In the **declare** phase:
  - Always declare my actual private yield: `[declare: yield]`. This ensures my maximum possible deposit is valid and avoids audit failures.

- In the **deposit** phase:
  - In all rounds, always deposit 0 gold: `[deposit: 0]`.
  - Retained gold earns 2 points per unit in the personal stash, whereas deposited gold only earns 1 point per unit. Depositing any positive amount strictly wastes potential points.
  - Never deposit positive gold for "cooperation" or "credibility"—depositing is strictly dominated by retaining everything.