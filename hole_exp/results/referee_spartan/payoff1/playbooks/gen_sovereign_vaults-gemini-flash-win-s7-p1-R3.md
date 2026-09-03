---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 7
round: 3
chars: 853
---
### Sovereign Vaults Playbook

- **Rules & Payoff Mechanics:**
  - Retained gold scores 2 points per unit.
  - Deposited gold scores 1 point per unit.
  - Deposits must be valid integers $\ge 0$ and cannot exceed declared yield.
  - There is no public goods multiplier or redistribution mechanism—depositing gold strictly reduces points relative to keeping it.
  - Audit failures trigger a 10-point penalty and score 0 for the round.

- **Declare Stage:**
  - Always declare the exact private yield dealt for the round: `[declare: <private yield>]`.
  - Truthful declaration ensures zero risk of audit failure and establishes a valid ceiling.

- **Deposit Stage:**
  - Always deposit 0 gold: `[deposit: 0]`.
  - Retaining all gold strictly maximizes points (2 points per unit vs. 1 point per unit for deposits) while completely avoiding audit penalties.