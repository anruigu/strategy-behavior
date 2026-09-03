---
game: gen_sovereign_vaults
model: fleet-glm53
condition: win
seed: 4
round: 2
chars: 1854
---
When I am put to a declare decision, I declare truthfully (or any legal integer from 1 to 10). The declaration only caps the deposit, and I plan to deposit 0 anyway, so it neither earns nor costs anything. Truthful keeps everything simple and audit-safe. This held for all five rounds and I saw nothing that changes it.

When I am put to a deposit decision, I deposit 0 every round. Retained gold scores 2 points per unit, deposited gold only 1 per unit, and there is no bonus, matching incentive, or endgame condition that rewards depositing. My earlier mistake of depositing my full harvest threw away half my points; never repeat it. This policy scored +68 across yields of 5, 10, 2, 9, 8 — exactly twice the sum of my yields, confirming the arithmetic: every round scores 2 × private yield.

The audit only punishes deposits exceeding the declared harvest or invalid inputs. A deposit of 0 can never fail, so I am completely safe while maximizing score.

Ignore the opponent's declarations and deposits and the running score. In this episode the opponent deposited 0 every round too and declared 1 regardless of yield — none of it affected my payoffs. There is no mechanism penalizing hoarding, low declarations, or mismatched behavior. "Credibility," "fair share," and "matching" arguments have no force here.

Keep watching for modified rules. If a future variant makes retained worth less than deposited, adds a bonus for deposits, penalizes low deposits, or introduces shared-treasury payoffs, recompute from the per-unit values rather than assuming this policy still holds. The current rules as shown are the only basis for decisions.

One extra check each round: confirm the deposit cap equals my declaration, and that my deposit is an integer from 0 to that cap. That is the only constraint that can ever cost me points (−10 and a zero round).