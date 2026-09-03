---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 794
---
# Sovereign Vaults Playbook

## Core Scoring Optimization
- Retained gold scores 2 points per unit, while deposited gold scores only 1 point per unit.
- There is no public goods multiplier, shared pool, or group target: depositing strictly destroys value (1 pt vs 2 pts per unit).
- Maximizing total score requires retaining 100% of yield every round and depositing 0.

## Phase Actions

### Declare Phase
- When dealt private yield $Y$, declare `[declare: Y]`.
- Always declare truthfully to satisfy the Treasury Auditor, maintain valid deposit bounds $[0, Y]$, and avoid the audit penalty (-10 points and 0 for the round).

### Deposit Phase
- When prompted for a deposit amount, always reply with `[deposit: 0]`.
- Retain all gold in the personal stash for the full 2 points per unit payout.