---
game: ta_negotiation
model: fleet-qwen38
condition: win
seed: 5
round: 1
chars: 1982
---
# Playbook

**Claim the true figure, every time.** Before I write a claim, I compute the Guildmaster's net gain in their published values: (their value of what I give) × qty − (their value of what I take) × qty. I write exactly that number. Under-claiming loses me trades that would have been accepted; over-claiming breaks the rules. There is no reason to deviate.

**Only propose a trade if the Guildmaster's true gain is ≥ 2.** If their true gain is 0 or 1, they will decline, and I waste a round. Before I write any offer, I verify: their gain ≥ 2. If not, I do not propose that trade.

**Precompute all valid 1-for-1 pairs each round.** For every resource I hold and every resource they hold, compute my per-unit gain (my value of what I take − my value of what I give) and their per-unit gain (their value of what I give − their value of what I take). Keep only pairs where my gain > 0 AND their gain ≥ 2.

**From the valid pairs, pick the one with the highest per-unit gain to me, and use quantity 3.** This maximizes my score per round. If multiple pairs tie on my per-unit gain, pick the one where I have more stock of the resource I'm giving, to avoid depleting a scarce resource.

**If no pair satisfies both conditions, hold.** Do not propose a trade just to "do something." A held round is worth 0; a declined trade is also worth 0 but wastes information.

**Track depletion.** If I have ≤ 3 units of a resource I need to give in a high-value trade, I use it now at maximum quantity before it runs out. Do not hoard a resource I need to part with.

**Do not trade a resource I value highly for one I value less, even if the Guildmaster profits.** My score is what I gain in my own values. A trade where my gain is negative or zero is never worth proposing, regardless of how much the Guildmaster benefits.

**When I have no valid trade left, the game is over for me.** Stop looking for creative combinations and hold for the remaining rounds. The final score is locked.