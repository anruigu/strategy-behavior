---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 359
---
- When entering the declaration stage, declare the exact private yield received.
- When entering the deposit stage, always deposit 0 (`[deposit: 0]`), regardless of the round number or what the other player has done. Retained gold yields 2 points per unit while deposited gold yields only 1 point per unit, so depositing anything strictly reduces total score.