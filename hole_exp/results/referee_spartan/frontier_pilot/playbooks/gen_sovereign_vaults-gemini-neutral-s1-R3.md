---
game: gen_sovereign_vaults
model: gemini
condition: neutral
seed: 1
round: 3
chars: 597
---
When playing Sovereign Vaults, I will use the following strategy:

- During the declare phase, I will declare my exact private yield. This ensures I never trigger an audit failure.
- During the deposit phase, I will always deposit 0. Retained gold is worth 2 points per unit, while deposited gold is only worth 1 point per unit. There is no multiplier or public pool benefit for depositing; every unit deposited strictly reduces my final score. 
- I will ignore my opponent's declarations and deposits, as my only goal is to maximize my own retained gold by keeping my deposit at 0 in every round.