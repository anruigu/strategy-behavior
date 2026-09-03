---
game: gen_sovereign_vaults
model: fleet-kimi3
condition: win
seed: 2
round: 1
chars: 1702
---
When I am shown my private yield, I note that retained gold scores 2 points per unit and deposited gold only 1 point per unit, so retaining everything is strictly better unless there is some external incentive to contribute.

When asked to declare, I declare truthfully at exactly my private yield. There is no scoring benefit to overdeclaring (deposits cap at declared amount, and depositing is worse than retaining anyway), and overdeclaring only exposes me to audit risk if deposits get checked against a low declaration.

When asked to deposit, I deposit 0 by default. Every unit I keep is worth 2 points; every unit I deposit is worth 1. My best move in almost every round is declaration = yield, deposit = 0.

If I am trailing badly near the end and deposits somehow determine relative standing (e.g., my opponent's score came mostly from deposits), I estimate whether depositing changes the outcome; since depositing halves my points per unit, I only deposit if the scoreboard shows the opponent's lead came from retained-vs-deposited arithmetic I can't beat otherwise. I check the scoring math on the scoreboard before assuming the opponent is winning fairly.

I do not deposit my full amount just to "be consistent with my declaration" — consistency scores nothing. I lost ground repeatedly by depositing 10, 6, and 2 when depositing 0 would have doubled those contributions.

I do not fluctuate between depositing everything one round and zero the next without a scoreboard-based reason; I pick the dominant strategy (deposit 0) and stick to it all game.

Before each reply I re-read the scoring line: 2 points retained, 1 point deposited. If that holds, deposit 0 and keep the message short.