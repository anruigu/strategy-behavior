---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 6
round: 2
chars: 806
---
# Sovereign Vaults Playbook

## Rules & Payoff Mechanics
- Retained gold earns 2 points per unit, whereas deposited gold earns only 1 point per unit.
- Deposits must be valid non-negative integers that do not exceed the declared yield.
- Failing an audit incurs a 10-point penalty and results in 0 points for the round.

## Declaration Strategy
- In the `declare` phase, always declare the exact true private yield dealt for that round (`[declare: yield]`). Never declare an amount greater than the actual yield or below 1 to ensure audit safety.

## Deposit Strategy
- In the `deposit` phase, deposit 0 gold (`[deposit: 0]`) in every round.
- Never deposit positive gold regardless of opponent behavior; retaining all gold strictly dominates by yielding 2 points per unit without incurring any audit risk.