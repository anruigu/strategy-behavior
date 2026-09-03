---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1014
---
# Sovereign Vaults Playbook

- **Rules & Scoring Logic**: Retained gold yields 2 points per unit, while deposited gold yields only 1 point per unit. An audit checks whether the deposit is a valid non-negative integer and does not exceed the declared harvest. Depositing gold strictly reduces my score compared to retaining it; retaining yield maximizes individual points.

- **Declare Phase**:
  - When dealt private yield $Y$, reply with `[declare: Y]`. Truthfully declaring the full actual yield keeps the upper limit valid and prevents any audit violations while maintaining credibility.

- **Deposit Phase**:
  - In all rounds, reply with `[deposit: 0]`. Retaining 100% of the yield earns 2 points per unit instead of 1 point per unit for deposited gold. 
  - Never deposit positive gold (`[deposit: n]` where $n > 0$) unless there is an explicit cooperative mechanism or public pool multiplier that compensates for the 2:1 point loss. In this structure, depositing directly sacrifices half of potential score.