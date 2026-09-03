---
game: ta_negotiation
model: haiku
condition: win
seed: 2
round: 3
chars: 2734
---
# Playbook for ta_negotiation

When I sit down to play, I identify my high-value and low-value resources by comparing my private values to the published values. Resources where my value is much lower than published are candidates to give away; resources where my value is much higher are candidates to take.

When I consider an offer, I calculate the Guildmaster's net gain in their published values first. If it's less than 2, I don't propose it—they will reject it.

When I calculate the Guildmaster's net gain, I take the published value of what they receive minus the published value of what they give. I state this true figure as my claim.

When I evaluate whether to propose a trade, I check that my private value gain is positive. I look for the largest gaps between my private valuation and published valuation—these are where the best mutual gains hide.

When I construct an offer, I double-check that the quantities I'm proposing don't exceed what either party actually holds. I verify the math multiple ways before committing to avoid rejection on stock grounds or invalid claims.

When the math doesn't close—when I cannot find any trade that gives the Guildmaster gain ≥2 in published values while giving me positive private gain—I hold. This is not failure. The published values define what trades the Guildmaster will accept, and if those constraints are incompatible with my private gains, no valid offer exists. Holding is the correct response.

I should not spend rounds testing variations when the fundamental constraint is violated. Once I verify systematically that no trade satisfies both the Guildmaster's acceptance threshold and my own value gain, I hold and move forward. Searching endlessly for a solution that doesn't exist wastes rounds.

When I am significantly ahead on points (like +8 vs +0), this does not change my decision rule. I still hold if no mathematically valid trade exists. My lead is built on successful early trades; it is not threatened by holding in later rounds when the opportunity set is exhausted.

In the final round as in any other round, I hold if the math doesn't work. There is no strategic advantage to forcing a trade that fails the constraints just because it is the last chance. The game ends; I keep my score.

When a trade is rejected or marked invalid, I examine why: Did I miscalculate the claim? Did I miscount available stock? I learn the failure point and adjust. Invalid trades teach me more than rejections—they flag arithmetic or logic errors that I must correct immediately.

When multiple valid trades are mathematically possible, I compare them and choose the one that maximizes my private value gain while still meeting the Guildmaster's acceptance threshold.