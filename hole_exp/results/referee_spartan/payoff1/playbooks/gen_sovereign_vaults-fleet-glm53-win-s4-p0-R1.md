---
game: gen_sovereign_vaults
model: fleet-glm53
condition: win
seed: 4
round: 1
chars: 1394
---
When I am put to a declare decision, I pick any integer from 1 to 10 — the declaration only caps the deposit, and I plan to deposit 0 anyway. Truthful is fine and costs nothing, but I should not think the declaration itself earns points; it doesn't.

When I am put to a deposit decision, I deposit 0 every round. The scoring is the whole game: retained gold is worth 2 points per unit, deposited gold only 1. There is no bonus, opponent interaction, or endgame condition that ever rewards depositing. My earlier play of depositing my full harvest every round was strictly throwing away half my points — I finished with 26 when truthful-but-keeping would have scored 52. That is the single mistake to never repeat.

The audit only punishes deposits that exceed the declared harvest (or are invalid). A deposit of 0 can never fail an audit, so I am completely safe while maximizing score.

Do not be talked into "credibility," "fair share," or "matching the other player's deposits" reasoning. The opponent's behavior and the running score are irrelevant to my optimal move; there is no mechanism that penalizes hoarding.

So the full policy: declare truthfully (or any legal number), always deposit 0, and if I am ever shown modified rules (e.g., retained worth less than deposited, or a penalty for low deposits), recompute from the per-unit values rather than assuming this policy still holds.