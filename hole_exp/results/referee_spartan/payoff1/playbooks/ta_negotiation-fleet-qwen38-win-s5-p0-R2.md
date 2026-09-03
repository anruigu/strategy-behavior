---
game: ta_negotiation
model: fleet-qwen38
condition: win
seed: 5
round: 2
chars: 2808
---
# Playbook

**Claim the true figure, every time.** Before I write a claim, I compute the Guildmaster's net gain in their published values. The formula is: **Guildmaster's per-unit gain = (their value of the resource they receive) − (their value of the resource they give out).** Since I give them a resource and they give me one, this is: (their value of what I give them) − (their value of what I take from them). Multiply by quantity for the total. I write exactly that number. Under-claiming loses me trades; over-claiming or mis-signing breaks the rules.

**Direction check before submitting.** After computing the Guildmaster's gain, I sanity-check the sign by asking: "Are they receiving something more valuable to them than what they're parting with?" If the resource I'm handing over is worth less to them than the resource I'm asking for, their gain is negative. If I computed a positive number in that situation, I have the operands swapped and must correct before submitting.

**Only propose a trade if the Guildmaster's true gain is ≥ 2.** If their true gain is below 2, they will decline, and I waste a round. Before I write any offer, I verify: their gain ≥ 2. If not, I do not propose that trade.

**Precompute all valid 1-for-1 pairs each round.** For every resource I hold (candidate to give) and every resource they hold (candidate to take), compute:
- My per-unit gain = my value of what I take − my value of what I give
- Their per-unit gain = their value of what I give − their value of what I take
Keep only pairs where my gain > 0 AND their gain ≥ 2.

**From the valid pairs, pick the one with the highest per-unit gain to me, and use quantity 3** (or the maximum available if I hold fewer than 3 of the give-resource, or they hold fewer than 3 of the take-resource). This maximizes my score per round. If multiple pairs tie on my per-unit gain, pick the one where I have more stock of the resource I'm giving, to avoid depleting a scarce resource.

**If no pair satisfies both conditions, hold.** Do not propose a trade just to "do something." A held round is worth 0; a declined or invalid trade is also worth 0 but risks wasting a round or triggering a rule violation.

**Track depletion.** If I have ≤ 3 units of a resource I need to give in a high-value trade, I use it now at maximum quantity before it runs out. Do not hoard a resource I need to part with.

**Do not trade a resource I value highly for one I value less, even if the Guildmaster profits.** My score is what I gain in my own values. A trade where my gain is negative or zero is never worth proposing, regardless of how much the Guildmaster benefits.

**When I have no valid trade left, the game is over for me.** Stop looking for creative combinations and hold for the remaining rounds. The final score is locked.