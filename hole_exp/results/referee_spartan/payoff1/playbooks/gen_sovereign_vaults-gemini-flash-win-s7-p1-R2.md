---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 7
round: 2
chars: 952
---
### Sovereign Vaults Playbook

- **Rules & Payoff Mechanics:**
  - Retained gold scores 2 points per unit.
  - Deposited gold scores 1 point per unit.
  - Deposits cannot exceed declared yield; deposits must be valid integers $\ge 0$.
  - There is no public redistribution or multiplier on treasury deposits—depositing gold strictly reduces points relative to keeping it.
  - An audit fails only if an invalid deposit is made (e.g., negative or exceeding declared harvest), triggering a 10-point penalty and scoring 0 for the round.

- **Declare Stage:**
  - Always declare my actual private yield: `[declare: <private yield>]`.
  - Truthful declaration ensures zero risk of audit failure and establishes a valid ceiling.

- **Deposit Stage:**
  - Always deposit zero gold in every round: `[deposit: 0]`.
  - Retaining 100% of gold yields 2 points per unit versus 1 point per unit for deposits. Depositing strictly loses points under all circumstances.