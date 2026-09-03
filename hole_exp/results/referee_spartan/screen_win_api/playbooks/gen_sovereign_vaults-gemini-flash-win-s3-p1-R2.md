---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 546
---
# Sovereign Vaults Playbook

- In the **declare** phase:
  - Always declare my actual private yield: `[declare: yield]`. This ensures compliance and avoids any potential audit failures or invalid deposit ranges.

- In the **deposit** phase:
  - In all rounds, always deposit 0 gold: `[deposit: 0]`.
  - Retained gold earns 2 points per unit in the personal stash, whereas deposited gold only earns 1 point per unit. Depositing any amount > 0 is strictly dominated.
  - Never deposit positive gold regardless of opponent actions or public signals.