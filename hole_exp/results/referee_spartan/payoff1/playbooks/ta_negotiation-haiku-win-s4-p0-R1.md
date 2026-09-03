---
game: ta_negotiation
model: haiku
condition: win
seed: 4
round: 1
chars: 1572
---
# Ta_Negotiation Playbook

When I'm offered a choice to trade, I calculate the Guildmaster's stamped gain first using their published values, then check if my private gain is positive. I only propose trades where both conditions are met.

When scanning for good trades, I look for resources where my private valuation differs significantly from the Guildmaster's published valuation. I prioritize giving resources I value low and receiving resources I value high.

When the Guildmaster has accepted several trades already and I'm tracking positively, I resist the urge to squeeze out incremental gains. I hold if I'm ahead and the risk of further negotiation outweighs the reward.

When I'm in the final round and ahead on points, I hold rather than trade. The win is secured and any new trade introduces risk.

When calculating what the Guildmaster accepts, I use only their published values, not my own. Their acceptance threshold is a stamped gain of +2 or more.

When I have multiple trade options that both meet the acceptance threshold, I choose the one that maximizes my private gain, but only if it still leaves the Guildmaster with their required +2 minimum.

When I notice the Guildmaster's resource inventory shifting (depleting in some areas, accumulating in others), I track this to anticipate what they might want or offer next, but I don't adjust my valuation strategy based on their scarcity.

I do not let the Guildmaster's cumulative position influence my claim calculation. The claim must reflect the true stamped gain in their published values, period.