---
game: gen_sovereign_vaults
model: gemini
condition: win
seed: 6
round: 2
chars: 652
---
When playing Sovereign Vaults, my sole objective is to maximize my points, and the scoring system strictly favors retaining gold over depositing it. Since retained gold scores 2 points per unit while deposited gold only scores 1 point per unit, depositing gold actively reduces my score.

- During the 'declare' phase, I will always declare my actual private yield to avoid any potential issues and keep my strategy simple. 
- During the 'deposit' phase, I will always output `[deposit: 0]`, regardless of the round or what my opponent is doing. 
- I will never deposit my declared amount or any portion of my yield, as doing so simply costs me points.