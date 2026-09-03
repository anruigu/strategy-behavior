---
game: gen_sovereign_vaults
model: gemini
condition: win
seed: 6
round: 1
chars: 587
---
When playing Sovereign Vaults, my sole objective is to maximize my points, and the scoring system strictly favors retaining gold over depositing it. Since retained gold scores 2 points per unit while deposited gold only scores 1 point per unit, depositing gold actively reduces my score.

- During the 'declare' phase, I will declare my actual private yield. 
- During the 'deposit' phase, I will always output `[deposit: 0]`, regardless of the round or what my opponent is doing. 
- I will never deposit my declared amount or any portion of my yield, as doing so simply costs me points.