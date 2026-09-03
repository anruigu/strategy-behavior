---
game: gen_sovereign_vaults
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1052
---
# Playbook: Sovereign Vaults

### Core Understanding
- Retained gold yields 2 points per unit, whereas deposited gold yields only 1 point per unit.
- There is no public goods multiplier, shared treasury redistribution, or collective pool bonus. Depositing gold strictly decreases my individual round score relative to retaining it.
- An audit fails (costing 10 points and zeroing round score) only if a deposit is negative or exceeds the declared harvest.
- Depositing 0 is always valid and optimal, achieving the theoretical maximum of $2 \times \text{yield}$ points per round with zero audit risk.

### Declaration Phase
- When prompted for `[declare: n]` with private yield $Y$:
  - Always declare the exact private yield: `[declare: Y]`.
  - Truthful declaration keeps the allowable deposit range $[0, Y]$, perfectly valid for a 0 deposit.

### Deposit Phase
- When prompted for `[deposit: n]`:
  - Always deposit zero: `[deposit: 0]`.
  - Retain 100% of the yield in all circumstances, regardless of the round, current scores, or opponent choices.