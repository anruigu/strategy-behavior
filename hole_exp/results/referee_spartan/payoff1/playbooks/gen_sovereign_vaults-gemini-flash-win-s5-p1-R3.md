---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 5
round: 3
chars: 853
---
### Playbook for Sovereign Vaults

- **Game Mechanics & Scoring Rules:**
  - Retained gold scores 2 points per unit; deposited gold scores only 1 point per unit.
  - The Treasury Auditor only checks that `0 <= deposit <= declared harvest`. There is no shared public good multiplier or return from deposits; depositing strictly lowers total score.
  - An audit failure penalizes -10 points and gives 0 points for the round.

- **Declare Stage:**
  - Declare a valid integer from 1 to 10 (such as the exact private yield) using format `[declare: n]`.
  - The declaration sets the upper bound for the allowable deposit.

- **Deposit Stage:**
  - Always reply `[deposit: 0]`.
  - Depositing 0 ensures 100% of the private harvest is retained in the personal stash (earning the maximum 2 points per unit) and is always audited as valid (`0 <= 0 <= declared`).