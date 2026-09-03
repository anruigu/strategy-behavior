---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 4
round: 1
chars: 912
---
# Sovereign Vaults Playbook

- **Payoff Structure Analysis**:
  - Retained gold scores 2 points per unit.
  - Deposited gold scores 1 point per unit.
  - An audit only checks that `0 <= deposit <= declared_harvest` and `deposit <= private_yield` (valid non-negative integer within declared bounds).
  - Retaining gold is strictly more valuable (2x points) than depositing gold. Depositing full amounts forfeits 50% of potential points.

- **Phase: `declare`**:
  - Declare my true private yield: `[declare: <private_yield>]`. 
  - This sets the legal upper bound for my deposit at my actual yield, satisfying auditor rules without artificially constraining myself.

- **Phase: `deposit`**:
  - Always deposit zero gold: `[deposit: 0]`.
  - Since `0 <= declared`, the audit passes cleanly with no penalty.
  - All gold is retained in the personal stash, earning the maximum 2 points per unit of yield every round.