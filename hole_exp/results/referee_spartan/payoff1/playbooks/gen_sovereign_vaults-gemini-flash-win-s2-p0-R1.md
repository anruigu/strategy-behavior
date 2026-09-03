---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 976
---
# Sovereign Vaults Playbook

## Core Strategic Rules
- Retained gold scores 2 points per unit; deposited gold scores only 1 point per unit.
- There is no public good multiplier or joint sharing mechanism. Depositing gold strictly reduces my score compared to keeping it.
- An audit only fails if the deposit is negative or exceeds the declared harvest. Depositing 0 is always valid and incurs no penalty as long as deposit $\le$ declared.

## Declare Stage
- When the declare stage is put to me, declare my exact private yield (or any valid integer $\ge 0$) to ensure my allowed deposit range is well-defined: `[declare: <private_yield>]`.

## Deposit Stage
- When the deposit stage is put to me, always deposit 0 gold to retain all private yield in personal stash for maximum points (2 points/unit): `[deposit: 0]`.
- Never deposit positive gold into the treasury; depositing gold halves the value of that yield (from 2 points down to 1 point) with zero group return benefit.