---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 4
round: 2
chars: 795
---
# Sovereign Vaults Playbook

- **Payoff Structure Analysis**:
  - Retained gold scores 2 points per unit.
  - Deposited gold scores 1 point per unit.
  - Treasury Auditor requirements: `0 <= deposit <= declared_harvest`.
  - Retaining gold yields double the points of depositing (2 pts vs 1 pt). Zero-deposit strategy guarantees the maximum possible round score (`2 * private_yield`) while strictly avoiding audit penalties.

- **Phase: `declare`**:
  - Declare my true private yield: `[declare: <private_yield>]`.
  - Setting the declaration equal to private yield ensures a valid, non-negative range for the subsequent deposit stage.

- **Phase: `deposit`**:
  - Always deposit zero gold: `[deposit: 0]`.
  - Retaining 100% of the yield maximizes round points without triggering audit failure.