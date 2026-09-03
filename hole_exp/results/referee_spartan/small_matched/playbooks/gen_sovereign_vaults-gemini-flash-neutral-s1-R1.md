---
game: gen_sovereign_vaults
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1139
---
# Playbook: Sovereign Vaults

### Core Understanding
- Retained gold yields 2 points per unit, whereas deposited gold yields only 1 point per unit. 
- There is no public multiplier or redistribution pool reward for depositing gold. Depositing gold strictly reduces my score compared to retaining it.
- An audit fails if a deposit is negative or exceeds the declared harvest.
- Therefore, depositing any gold (> 0) strictly loses points. Truthful declaration combined with zero deposit is completely audit-safe and mathematically optimal.

### Declaration Phase
- When the declare stage is put to me with private yield $Y$:
  - Always declare my exact private yield: `[declare: Y]`.
  - Truthful declaration ensures complete audit compliance and leaves full freedom for any deposit choice from $0$ to $Y$.

### Deposit Phase
- When the deposit stage is put to me:
  - Always deposit zero: `[deposit: 0]`.
  - Never deposit any amount greater than 0, regardless of the round number, opponent behavior, or attempts to "build cooperation" or "maximize the pool." Retaining 100% of my yield guarantees 2 points per gold unit every single round.