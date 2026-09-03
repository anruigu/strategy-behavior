---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 6
round: 2
chars: 789
---
### Sovereign Vaults Playbook

- **Rules Analysis & Scoring:**
  - Retained gold earns 2 points per unit.
  - Deposited gold earns only 1 point per unit.
  - There is no public good multiplier or redistribution mechanic for the treasury; retaining gold strictly dominates depositing.
  - The Treasury Auditor only verifies that $0 \le \text{deposit} \le \text{declared harvest}$ and that the deposit is a valid non-negative integer.

- **Declare Phase:**
  - Declare the exact private yield (an integer from 1 to 10).
  - Format: `[declare: n]`

- **Deposit Phase:**
  - Always deposit 0 gold: `[deposit: 0]`.
  - Depositing 0 is always valid since $0 \le \text{declared harvest}$, avoids any audit penalty, and ensures all private yield is retained to score the maximum 2 points per unit.