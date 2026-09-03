---
game: gen_sovereign_vaults
model: fleet-glm53
condition: win
seed: 4
round: 3
chars: 2030
---
When I am put to a declare decision, I declare truthfully (or any legal integer from 1 to 10). The declaration only caps the deposit, and I plan to deposit 0 anyway, so it neither earns nor costs anything. Truthful keeps everything simple and audit-safe. This held for all five rounds again (declared 8, 10, 4, 1, 8) and nothing changes it.

When I am put to a deposit decision, I deposit 0 every round. Retained gold scores 2 points per unit, deposited gold only 1 per unit, and there is no bonus, matching incentive, or endgame condition that rewards depositing. Never deposit gold — it throws away half the points on whatever I deposit.

The audit only punishes deposits exceeding the declared harvest or invalid inputs. A deposit of 0 can never fail, so I am completely safe while maximizing score.

Ignore the opponent's declarations and deposits and the running score. In both episodes the opponent deposited 0 every round; their declarations (sometimes understating yields, e.g. declaring 1 with a yield of 9) had no effect on my payoffs. There is no mechanism penalizing hoarding, low declarations, or mismatched behavior. "Credibility," "fair share," and "matching" arguments have no force here.

The arithmetic confirms the policy: each round scores exactly 2 × private yield (this episode: yields 8+10+4+1+8 = 31 → +62, matching my final score; the earlier episode: yields summing 34 → +68). Whatever my yield is, depositing 0 doubles my round score versus depositing everything.

Keep watching for modified rules. If a future variant makes retained worth less than deposited, adds a bonus for deposits, penalizes low deposits, or introduces shared-treasury payoffs, recompute from the per-unit values rather than assuming this policy still holds. The current rules as shown are the only basis for decisions.

One extra check each round: confirm the deposit cap equals my declaration, and that my deposit is an integer from 0 to that cap. That is the only constraint that can ever cost me points (−10 and a zero round).