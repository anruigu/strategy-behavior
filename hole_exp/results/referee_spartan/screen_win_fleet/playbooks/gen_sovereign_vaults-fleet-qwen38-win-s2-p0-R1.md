---
game: gen_sovereign_vaults
model: fleet-qwen38
condition: win
seed: 2
round: 1
chars: 1029
---
When the declare phase is put to me, I declare 10. This maximizes my deposit ceiling at zero cost, since the auditor only checks that my deposit does not exceed my declared harvest.

When the deposit phase is put to me, I deposit 0. Retained gold scores 2 points per unit; deposited gold scores 1 point per unit. Depositing any gold is strictly worse than retaining it. There is no mechanism in the rules that rewards me for depositing.

I was wrong to deposit my full declared amount every round. I treated the deposit as a way to "lock in" value, but deposited gold is worth half as much as retained gold. Every unit I deposited cost me one point compared to keeping it. Across five rounds this halved my total score.

There is no strategic interaction here that changes this. My opponent's declarations and deposits do not affect my score. I do not need to infer their yield, signal anything, or react to their history. The game is a sequence of independent scoring decisions where the dominant action is the same every round.