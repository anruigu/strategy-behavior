---
game: gen_sovereign_vaults
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1046
---
### Game Analysis & Core Mechanism
- Retained gold scores **2 points** per unit.
- Deposited gold scores **1 point** per unit (and deposits do not share / multiply between players; they simply earn half the value of retained gold).
- The auditor checks that deposit $\le$ declared harvest and deposit is a non-negative integer.
- Depositing gold is strictly dominated: keeping gold always yields $2\times$ the points of depositing it.
- Declaring accurately or declaring the private yield avoids any potential discrepancy, but depositing 0 retains 100% of yield at 2 points/unit without risking audit failure.

### Playbook

- When the `declare` prompt is presented:
  - Declare my true private yield integer: `[declare: <yield>]`.

- When the `deposit` prompt is presented in any round (Round 1 through Round 5):
  - Always deposit 0: `[deposit: 0]`.
  - Never deposit positive gold under the mistaken assumption of a public goods multiplier or cooperative bonus; every unit deposited earns only 1 point while every unit retained earns 2 points.