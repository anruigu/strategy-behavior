---
game: gen_sovereign_vaults
model: fleet-kimi3
condition: win
seed: 3
round: 1
chars: 1375
---
I treat declaration and deposit as separate decisions: declaration only sets a public cap, while retention is where the points are.

When my yield is revealed, I declare my true yield. I do not overstate to look strong or understate to sandbag; neither increases my score, and overstating only creates avoidable audit/constraint risk if I ever choose to deposit.

When deposit is requested, my default action is `[deposit: 0]`. Retained gold pays 2 per unit and deposited gold pays 1, so every unit I deposit lowers that round’s score unless the rules explicitly add a separate reward for treasury size.

I never deposit merely because I declared an amount, because the opponent deposited, because it is the final round, or to “use” the cap. A declaration is not a commitment to pay.

If an unusual setup makes deposited gold worth more than retained gold, or adds bonuses/penalties tied to the treasury, then I deposit only up to `min(actual yield, declared amount)` and only the amount justified by that external payoff. Otherwise I keep everything.

I do not risk audit failure for marginal gain: no negative deposits, no non-integers, no deposit above declaration, and no deposit above what I can actually cover if actual yield is enforced.

My scoring check before each deposit is: `score = 2 × retained + 1 × deposited`. If depositing reduces that number, I press zero.