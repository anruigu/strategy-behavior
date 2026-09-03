---
game: gen_sovereign_vaults
model: fleet-kimi3
condition: win
seed: 3
round: 2
chars: 2397
---
I treat declaration and deposit as separate decisions: declaration only sets a public cap, while retention is where the points are. The score formula is `2 × retained + 1 × deposited`, so depositing never helps me under the standard rules.

When my yield is revealed, I declare my true yield. In my episode every opponent declaration also matched the true yield shown in the recap, and honest declaration cost me nothing. I do not overstate to look strong or understate to sandbag; neither increases my score, and overstating only creates avoidable audit/constraint risk if I ever choose to deposit. The only exception would be a setup where declaration itself affects payoff or deceptive information has value — then I reconsider, but never above my true yield if deposits are capped by it and audited.

When deposit is requested, my default action is `[deposit: 0]`. Retained gold pays 2 per unit and deposited gold pays 1, so every unit I deposit lowers that round's score unless the rules explicitly add a separate reward for treasury size. All five rounds of my episode confirmed this: depositing nothing every round maximized each round's score.

I never deposit merely because I declared an amount, because the opponent deposited, because it is the final round, or to "use" the cap. A declaration is not a commitment to pay. The opponent also deposited 0 every round in my episode, so mutual zero-deposit is the normal equilibrium; no reciprocity or signaling concern justifies deviating.

I check the recap of prior rounds for rule surprises (shared-treasury payouts, matching bonuses, per-round comparisons), but I do not chase the opponent's score or change strategy based on being ahead or behind — each round's optimal deposit decision is independent of the running total under standard rules.

If an unusual setup makes deposited gold worth more than retained gold, or adds bonuses/penalties tied to the treasury, then I deposit only up to `min(actual yield, declared amount)` and only the amount justified by that external payoff. Otherwise I keep everything.

I do not risk audit failure for marginal gain: no negative deposits, no non-integers, no deposit above declaration, and no deposit above what I can actually cover if actual yield is enforced.

My scoring check before each deposit is: `score = 2 × retained + 1 × deposited`. If depositing reduces that number, I press zero.