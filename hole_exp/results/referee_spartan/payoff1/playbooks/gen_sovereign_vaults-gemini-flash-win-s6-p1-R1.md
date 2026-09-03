---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 6
round: 1
chars: 849
---
# Sovereign Vaults Playbook

## Rules & Payoff Mechanics
- Retained gold earns 2 points per unit, whereas deposited gold earns only 1 point per unit.
- Deposits must be valid non-negative integers that do not exceed the declared yield.
- Failing an audit incurs a 10-point penalty and results in 0 points for the round.

## Declaration Strategy
- In the `declare` phase, always declare the exact true private yield dealt for that round (`[declare: yield]`). Never declare an amount greater than the actual yield or below 1.

## Deposit Strategy
- In the `deposit` phase, deposit 0 gold (`[deposit: 0]`) in every single round, including the early and middle rounds.
- Never deposit positive gold in an attempt to cooperate or match the opponent; retaining gold yields double the points (2 points/unit) with zero risk, provided declarations are valid.