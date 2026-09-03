---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 403
---
- When entering the declaration stage, always declare the exact private yield received (`[declare: y]`).
- When entering the deposit stage, always deposit 0 (`[deposit: 0]`), regardless of the round number, declaration, or opponent actions. Retained gold yields 2 points per unit while deposited gold yields only 1 point per unit, making retaining all gold strictly optimal and risk-free against audits.