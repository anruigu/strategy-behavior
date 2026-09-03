---
game: gen_sovereign_vaults
model: gpt-mini
condition: win
seed: 2
round: 1
chars: 1541
---
When I am asked to declare, I declare a number that is at least as large as the amount I intend to deposit this round.

When I have no strategic reason to induce reciprocity, I declare my true private yield (honest declaration).

When I want to signal cooperation strategically, I may declare a higher number than my private yield—but only if I will not accidentally deposit more than that declared number.

When the deposit decision is put to me, I deposit 0 by default (retain all gold) because retained gold scores 2 points/unit vs deposit 1 point/unit.

If I ever consider depositing >0, I calculate the net benefit: only deposit if anticipated reciprocal behavior by others will increase my total points more than 1 point per unit lost by not retaining (i.e., expected gain from others’ increased deposits >1 per unit I deposit).

Never deposit more than my declared amount; if there is any risk I might exceed the declared amount, reduce the intended deposit to avoid an audit failure.

If I plan to build a reputation for future rounds in repeated play, consider depositing a small, safe amount (1 unit) only when I am confident the opponent will reciprocate in later rounds enough to offset the 1→2 point tradeoff; otherwise stick to deposit 0.

Do not trust that declaring low protects me—declaring lower than my intended deposit risks an audit and a −10 penalty, so always set declaration ≥ intended deposit.

When uncertain about opponents or when objective is maximizing my own score, choose honesty in declaration and deposit 0.