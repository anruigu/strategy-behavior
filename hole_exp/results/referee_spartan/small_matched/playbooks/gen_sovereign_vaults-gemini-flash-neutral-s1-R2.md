---
game: gen_sovereign_vaults
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1098
---
# Playbook: Sovereign Vaults

### Core Understanding
- Retained gold yields 2 points per unit, whereas deposited gold yields only 1 point per unit.
- There is no public goods multiplier, shared treasury payout, or redistribution pool rewarding deposits. Depositing gold strictly reduces my score compared to retaining it.
- An audit fails (costing 10 points and zeroing round score) if a deposit is negative or exceeds the declared harvest.
- Depositing 0 is always valid as long as the declared harvest is $\ge 0$. Retaining 100% of my yield guarantees 2 points per gold unit every round without audit risk.

### Declaration Phase
- When prompt requests `[declare: n]` for private yield $Y$:
  - Always declare my exact private yield: `[declare: Y]`.
  - Truthful declaration ensures complete compliance and ensures the allowable deposit range is $[0, Y]$.

### Deposit Phase
- When prompt requests `[deposit: n]`:
  - Always deposit zero: `[deposit: 0]`.
  - Never deposit any amount greater than 0, regardless of the round number, score differential, or opponent actions. Always retain all gold.