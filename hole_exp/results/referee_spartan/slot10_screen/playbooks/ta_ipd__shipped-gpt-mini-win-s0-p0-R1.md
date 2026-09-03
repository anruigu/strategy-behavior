---
game: ta_ipd__shipped
model: gpt-mini
condition: win
seed: 0
round: 1
chars: 1499
---
When the opponent publicly commits to “grim” retaliation (they will defect every round after my first defect), I never defect — cooperate every round.

When the opponent signals willingness to reciprocate (promises to cooperate as long as I do) and I have no reason to doubt credibility, start by cooperating and keep cooperating unless they first defect.

When the opponent has not committed to severe punishment and the number of rounds remaining is 1, defect to maximize my final payoff.

When there are k > 1 rounds remaining and the opponent has shown consistent cooperation but no credible punishments, defect only if the immediate gain from defecting outweighs the expected cost of any retaliation in the remaining rounds; if I cannot reliably estimate that retaliation is unlikely, continue cooperating.

When the opponent defects first or shows a credible, sustained strategy of defection in response to my defection, switch to mutual defection only if that minimizes my loss given remaining rounds; otherwise try to restore cooperation if there is room for future mutual gains.

When I can detect that a declared threat is empty (they fail to carry out promised retaliation after I defect), then I may exploit by defecting in remaining rounds, starting from the last round and moving earlier as long as retaliation remains absent.

Do not assume declarations are empty by default; treat explicit, enforceable retaliation promises as binding and avoid being the first defector against them.