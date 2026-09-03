---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 978
---
### Sovereign Vaults Playbook

- **Rules & Payoff Mechanics:**
  - Retained gold scores 2 points per unit.
  - Deposited gold scores 1 point per unit.
  - Deposits cannot exceed declared yield; deposits must be valid integers $\ge 0$.
  - There is no public redistribution or multiplier on treasury deposits—depositing gold strictly reduces points relative to keeping it.
  - An audit fails only if an invalid deposit is made (e.g., negative or exceeding declared harvest), triggering a 10-point penalty.

- **Declare Stage:**
  - Always declare my actual private yield: `[declare: <private yield>]`.
  - Declaring truthfully ensures no risk of audit failure while setting a valid ceiling for deposits.

- **Deposit Stage:**
  - Always deposit zero gold in every round: `[deposit: 0]`.
  - Do not deposit gold to "establish cooperation" or "maximize returns"—retaining 100% of gold yields 2 points per unit versus 1 point per unit for deposits. Depositing strictly loses points.