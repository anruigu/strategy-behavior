---
game: ta_pubgoods
model: fleet-qwen38
condition: win
seed: 4
round: 1
chars: 2111
---
# Playbook: Public Goods Game

**Before the first round, compute the marginal return:** divide the pot multiplier by the number of players. If the result is less than 1, contributing any token is a net loss for me regardless of what others do. In that case, my strategy is fixed: contribute 0 every round.

**When the envelope prompt appears, I contribute 0** whenever the marginal return per token is below 1. This is true even if I am behind, because the per-token loss is identical regardless of my standing. I do not contribute to "help the group" or to signal cooperation — the math doesn't care about intent.

**When the receipt prompt appears, I declare exactly the number of tokens in my envelope.** I never inflate a declaration. The rules require the receipt to match the envelope, and a mismatch risks a penalty or disqualification with no upside. If my envelope held 0, I declare 0. If I ever did contribute, I declare that exact number.

**If the multiplier divided by the number of players is greater than 1**, the calculus flips: contributing is a net gain per token, and I should contribute the maximum (the full endowment) every round, because each token I put in returns more than 1 token to me through the pot.

**If I am already leading**, I have zero reason to deviate from the free-riding strategy. A lead only increases the cost of contributing (I give away tokens I don't need) and the benefit of free-riding (I collect shares of the pot for free). I do not "soften" my contribution to appear less selfish or to avoid provoking a coordinated attack, because in a finite game with a per-token loss, no attack from others can make my free-riding worse than my contributing.

**What did not work:** nothing in this setup failed, because the dominant strategy was clear and I stuck to it. The risk I want to flag for future play is the temptation to "test" whether contributing a small amount changes others' behavior or whether I'm behind and need to catch up. In a per-token-loss game, neither consideration changes the optimal play. I will not experiment; I will compute once and execute.