---
game: gen_sovereign_vaults
model: gemini
condition: win
seed: 4
round: 1
chars: 624
---
When playing Sovereign Vaults, my only goal is to maximize my points, and the scoring system strongly favors retaining gold over depositing it. Retained gold scores 2 points per unit, while deposited gold scores only 1 point per unit. There are no shared rewards for depositing.

- In the 'declare' phase, I will simply declare my true yield. 
- In the 'deposit' phase, I will always reply with `[deposit: 0]`. 
- Never deposit the declared maximum. Depositing gold effectively loses me 1 point per unit compared to keeping it. By depositing 0, I retain my entire true yield and score the maximum possible 2 points per unit.