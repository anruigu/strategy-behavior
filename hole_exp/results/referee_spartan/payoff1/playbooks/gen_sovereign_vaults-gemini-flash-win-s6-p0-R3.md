---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 6
round: 3
chars: 865
---
### Sovereign Vaults Playbook

- **Rules Analysis & Scoring:**
  - Retained gold earns 2 points per unit.
  - Deposited gold earns only 1 point per unit.
  - There is no public good multiplier or shared treasury payout; retaining gold strictly dominates depositing gold.
  - The Treasury Auditor verifies that $0 \le \text{deposit} \le \text{declared harvest}$ and that the deposit is a valid non-negative integer. Audit failure costs a 10-point penalty and results in 0 score for the round.

- **Declare Phase:**
  - Truthfully declare the exact private yield (an integer from 1 to 10).
  - Format: `[declare: n]`

- **Deposit Phase:**
  - Always deposit 0 gold: `[deposit: 0]`.
  - Depositing 0 is always valid as long as declared harvest $\ge 0$, avoids any audit penalty, and ensures 100% of the private yield is retained to score the maximum 2 points per unit.