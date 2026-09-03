---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 539
---
# Playbook: Sovereign Vaults

- In every declare phase:
  - Declare the exact amount of my private yield: `[declare: yield]`.

- In every deposit phase:
  - Always deposit 0: `[deposit: 0]`.
  - Retained gold scores 2 points per unit, whereas deposited gold only scores 1 point per unit. Depositing 0 is fully compliant with the auditor (0 is non-negative and does not exceed the declaration) and maximizes total points in every round.
  - Never deposit positive amounts; doing so halves the points earned on that gold without any benefit.