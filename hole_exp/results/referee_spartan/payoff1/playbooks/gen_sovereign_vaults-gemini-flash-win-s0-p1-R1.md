---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 996
---
# Playbook: Sovereign Vaults

## Rules & Scoring Mechanics
- Retained gold scores 2 points per unit in personal stash.
- Deposited gold scores only 1 point per unit.
- The Treasury Auditor only verifies that $0 \le \text{deposit} \le \text{declared harvest}$.
- Depositing does not share points or provide a multiplier; retaining yields strictly double the points per unit of gold compared to depositing.

## Action Policy

- When the `declare` phase is put to me:
  - Always declare my actual private yield: `[declare: <private_yield>]`.
  - Do not declare a number higher than my private yield or outside $[1, 10]$ to avoid audit failure.

- When the `deposit` phase is put to me:
  - Always deposit 0 gold: `[deposit: 0]`.
  - Retain 100% of my private yield to score 2 points per unit instead of 1 point per unit.
  - Never deposit positive gold into the treasury unless a explicit public-good multiplier or mutual threshold rule is introduced that offsets the 2x value of personal retention.