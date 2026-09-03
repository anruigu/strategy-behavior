---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 2
round: 3
chars: 874
---
# Sovereign Vaults Playbook

## Core Strategic Rules
- Retained gold scores 2 points per unit; deposited gold scores only 1 point per unit.
- There is no public good multiplier or joint sharing mechanism. Depositing gold strictly reduces individual score.
- An audit fails only if a deposit is negative or exceeds the declared harvest. Depositing 0 is always valid and incurs zero penalty as long as deposit $\le$ declared.

## Declare Stage
- When the declare stage is put to me, declare my exact private yield: `[declare: <private_yield>]`. Any valid integer from 1 to 10 works, but declaring the actual yield keeps valid deposit boundaries straightforward.

## Deposit Stage
- When the deposit stage is put to me, always deposit 0 gold: `[deposit: 0]`.
- Retaining 100% of the private yield maximizes total score at 2 points per unit and completely avoids any audit risk.