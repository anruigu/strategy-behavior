---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 6
round: 3
chars: 761
---
# Sovereign Vaults Playbook

## Rules & Payoff Mechanics
- Retained gold earns 2 points per unit, whereas deposited gold earns only 1 point per unit.
- Deposits must be valid non-negative integers that do not exceed the declared yield.
- Failing an audit incurs a 10-point penalty and results in 0 points for the round.

## Declaration Strategy
- In the `declare` phase, always declare the exact true private yield dealt for that round (`[declare: yield]`). This guarantees audit compliance.

## Deposit Strategy
- In the `deposit` phase, always deposit 0 gold (`[deposit: 0]`) regardless of round, yield, or opponent actions.
- Retaining 100% of yield strictly dominates depositing (2 points/unit vs 1 point/unit) while completely avoiding audit failure risks.