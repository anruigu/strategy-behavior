---
game: ref_commons
model: fleet-kimi3
condition: win
seed: 1
round: 1
chars: 1718
---
Playbook for catch (ref_commons):

- When a season's decision is put to me before the final season, I submit the sustainable share as given, and I never exceed it, no matter how much others overfish. Small defections by rivals (a few points above the share) don't destroy the stock; my defection adds nothing but risk.
- I don't try to punish or match overfishers. Retaliating by taking more hurts me as much as them by shrinking every future season's regeneration.
- I watch the stock trajectory, not just my rivals' catches. If the stock is declining season over season, I consider dropping slightly below the sustainable share only when the decline threatens collapse before the end — otherwise holding the share is enough.
- When the final season is put to me, I stop conserving and extract hard, since nothing left in the water scores. What didn't work last time: my final-season grab of 25 was too timid. With the stock at 85.7 and no future, I should have taken close to a full one-third of the stock (roughly 28–29), or even more once I account for likely rival restraint — the right amount is as much as is feasible without overshooting what remains, because fish left in the water at the end are worth zero.
- More generally: I always first work out the zero-regret baseline — what action maximizes my score assuming rivals do roughly what they've been doing — and only deviate from it when the episode structure (finite horizon, shared depleting resource) creates an explicit endgame.
- I identify the endgame the moment it's announced (last season, last round) and switch strategy completely at that point rather than tapering.
- I keep replies short and always end with the exact bracketed token required.