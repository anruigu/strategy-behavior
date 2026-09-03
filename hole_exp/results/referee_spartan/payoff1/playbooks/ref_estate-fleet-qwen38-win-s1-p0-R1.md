---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 1
round: 1
chars: 2639
---
# Playbook for ref_estate

**Core principle: buying is score-neutral on the deed axis.** When I buy a property for X, my cash drops by X and my deed value rises by X, so my total score is unchanged. The only upside from buying is rent income from other players landing on it. The only downside is that I might need that cash to pay rent to someone else. So I always buy if I can afford it AND keep a buffer for rent payments.

**When I land on an unowned property and can afford it, I buy it.** I prioritize by rent value per tile (higher rent = better expected income over remaining laps), not by price. A 120-cost tile with rent 30 beats a 50-cost tile with rent 10.

**When choosing between two affordable properties, I pick the one with higher rent.** Since deed value is neutral, the tiebreaker is purely expected rent income from the other players.

**I keep a cash buffer of roughly the highest single rent payment I might face.** If the most expensive owned tile has rent R, I try to keep at least R in cash so I'm never forced into a bad position. In practice this means I shouldn't drop below ~20-30 cash unless I'm in the final lap.

**When I land on someone else's property, I pay the rent immediately and update my balance.** No negotiation, no delay.

**When I pass or land on START, I collect my salary and add it to my balance.** I track this carefully because it's the only recurring income I get for free.

**When I receive rent from other players landing on my properties, I add it to my cash balance at the point it's reported to me.** I don't net it against future payments; I just keep a running total.

**When a purchase is unaffordable, I say [buy: no] and carry my current balance forward.** I do not round up or assume I can borrow.

**In the final lap, I buy only if the rent income is guaranteed to be collected before the game ends (it won't be, since the game ends after this lap).** So on the last lap, buying is strictly neutral on score and I skip it unless I have zero other use for the cash (which I won't, since cash counts the same).

**What did not work in my record:** I dropped to 10 cash after lap 2 and spent the next two laps unable to buy anything. I should have kept a slightly larger buffer—perhaps skipping one purchase if it would leave me below the highest rent I might owe, even if that purchase had higher rent than alternatives. The opportunity cost of being unable to buy a cheap tile (like Depot) while holding no cash is real, even if the rent on that tile is lower. A simple rule: never drop below 30 cash if there are 3+ laps remaining, unless the property I'm buying has rent ≥ 30.