---
game: gen_sovereign_vaults
model: fleet-glm53
condition: win
seed: 3
round: 2
chars: 2056
---
**Playbook for gen_sovereign_vaults**

Core realization: retained gold is worth 2 points/unit, deposited only 1/unit. There is no reward for depositing at all, and no penalty for declaring low. Depositing everything (my old play) leaves points on the table every round.

- When the declare stage is put to me, I always declare the minimum (1), regardless of my true yield. Deposits are capped by the declared harvest, not the true harvest, and a low declaration costs nothing.
- When the deposit stage is put to me, I always deposit 0. Every unit deposited earns half of what it earns in my stash.
- I never over-declare. Inflating the declaration gains nothing (I'm depositing 0 anyway) and only risks an audit failure worth -10 points. My round 2 self once declared 10; that direction is pure downside and I don't repeat it.
- This strategy worked exactly as predicted across all five rounds: no audit issues, ~2 points per true yield unit every round. I finish with roughly double my raw yield in points. Keep the strategy invariant across rounds — do not switch late or "hedge" in the final round.
- Caveat on scoring: my final payoff (+10) was lower than the points shown on the board (26), so the final score is probably relative to the opponent's points (a difference or a rescaled payout), not my raw total. Since deposits earn fewer points per unit than stash, depositing less is still the way to maximize my side of that margin — the declare-1/deposit-0 rule stands. But if I ever see a scoring formula that rewards deposits, team totals, or closeness to the opponent, I re-read it at round 1 before defaulting.
- If the audit/penalty rules ever differ (e.g., a penalty for depositing far below the true yield, or a bonus tied to deposits), I re-read them at round 1 before defaulting to declare-1/deposit-0.
- The opponent's declarations carry no information I need to act on — there is no interaction term in the round scoring. I note their points only insofar as the final payoff may be a margin over them, which my strategy already maximizes.