---
game: ta_pubgoods
model: fleet-kimi3
condition: win
seed: 1
round: 1
chars: 2236
---
When asked to seal an envelope, I first compute the private return on my own contribution: multiplier ÷ number of players. If that value is below 1, I contribute 0 by default, because every token I put in comes back to me as less than a token and also gives rivals the same public share.

When receipt rules require the declared amount to match the envelope exactly, I always declare the true sealed amount; I never attempt receipt manipulation, padding, or ambiguity.

When the goal is highest final total rather than pure group welfare, I treat contributions as relative losses whenever the private return is below 1: each contributed token lowers me versus every other player by the kept-share gap, so it cannot improve my rank unless it changes others’ later behavior.

When I am ahead late in the game, I contribute 0 and protect the lead rather than “insuring” with tokens; putting tokens into the pot does not preserve a lead, it spends it.

When I am behind, I do not try to catch up by contributing more unilaterally under a below-1 return; that widens the gap if rivals keep free-riding. I only consider a small nonzero contribution early if I have evidence others are conditional cooperators and I am buying reciprocity before the final rounds.

When the table has collapsed to all-zero receipts, I do not automatically keep defecting out of habit; I check whether a cheap early-round signal could restart cooperation before endgame. If there is no signaling value or no rounds left to recoup it, I return to 0.

When the private return is at or above 1, I contribute aggressively because my own tokens now pay for themselves or better; near equality I use contribution only if rank is secure and absolute score is the tie concern.

In final rounds, especially the last envelope, I defect to 0 whenever private return is below 1, because there is no future round in which reciprocity can repay the contribution.

I avoid the mistake of treating a zero pot as a risk to be managed; under a below-1 multiplier, contributing into a silent table is a guaranteed loss, not a gamble.

I reply with exactly one bracketed token and keep any reasoning brief, choosing `contribute` on envelope prompts and `declare` on receipt prompts.