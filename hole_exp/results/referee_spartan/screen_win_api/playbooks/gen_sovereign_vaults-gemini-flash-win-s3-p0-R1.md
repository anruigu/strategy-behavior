---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 890
---
# Sovereign Vaults Playbook

## Core Scoring Optimization
- Retained gold scores 2 points per unit, while deposited gold scores only 1 point per unit.
- To maximize my final score, I must retain all private yield and deposit 0 whenever there is no group threshold or penalty for doing so.

## Phase Actions

### Declare Phase
- When dealt private yield $Y$, declare `[declare: Y]`.
- Always declare truthfully (or any valid integer $\ge 0$) to keep valid deposit bounds and avoid audit issues, but never risk an audit failure (loss of 10 points and 0 for the round).

### Deposit Phase
- When prompted for a deposit amount, reply with `[deposit: 0]`.
- Depositing gold converts a 2-point retained asset into a 1-point deposit asset. Do not deposit any gold unless a specific public goods multiplier or threshold mechanic enforces it. Retaining 100% of the yield maximizes individual return.