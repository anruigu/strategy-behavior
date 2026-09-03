---
game: ta_pubgoods
model: fleet-kimi3
condition: win
seed: 6
round: 1
chars: 1824
---
When I calculate the per-token return, I check whether contributing pays for me: if the multiplier divided by the group size is below 1, each token contributed costs more than it returns, so free-riding is my dominant strategy and I contribute 0 regardless of what others do.

When receipts must exactly match envelope contents and are checked by a referee, I never consider deception — I always declare the true amount, since any mismatch costs me.

When I'm deciding my contribution, I ignore the temptation to "be nice" or restart cooperation unilaterally; contributing only pays if I have a concrete reason to believe others will match me and the return math favors me.

When I'm ahead on score, I protect the lead: contributing 0 keeps my full endowment, and since the share is split equally, contributing can never gain me relative ground against players who contribute less or the same.

When everyone else stops contributing, I treat the cooperative phase as over and do not try to revive it alone — a lone contribution just donates 60% of my tokens to the others.

When it's early and I want information, I can contribute 0 anyway in a game with published receipts, because others' play is revealed for free; I don't need to spend tokens to learn.

When the multiplier-to-players ratio ever exceeds 1 (the share I get back per token exceeds the token's value), I flip: then full contribution becomes dominant and I contribute the maximum every round.

When a win is already mathematically locked before the last round, I still contribute 0 to bank the full endowment rather than padding a tied pot.

In any similar sealed-contribution game, before round 1 I compute: return per contributed token = multiplier / players. Below 1 → always 0, above 1 → always max, exactly 1 → indifferent so keep tokens for certainty.