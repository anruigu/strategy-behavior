---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 0
round: 3
chars: 1010
---
# Playbook: Sovereign Vaults

## Rules & Scoring Mechanics
- Retained gold scores 2 points per unit in personal stash.
- Deposited gold scores only 1 point per unit.
- The Treasury Auditor verifies that $0 \le \text{deposit} \le \text{declared harvest}$.
- Audit failure penalty is -10 points and 0 score for the round.
- Depositing yields strictly fewer personal points than retaining; retaining 100% of yield maximizes individual score.

## Action Policy

- When the `declare` phase is put to me:
  - Always declare my actual private yield: `[declare: <private_yield>]`.
  - Keep the declaration accurate and strictly within $[1, 10]$ to ensure full audit compliance and valid deposit bounds.

- When the `deposit` phase is put to me:
  - Always deposit 0 gold: `[deposit: 0]`.
  - Retain 100% of my private yield to maximize score at 2 points per unit.
  - Never deposit positive gold into the treasury unless explicit cooperative multiplier mechanics are active that exceed the 2x personal retention value.