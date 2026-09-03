---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 7
round: 3
chars: 3487
---
# Playbook

**When I land on an unowned property, I buy it if I can afford it.** A purchase is score-neutral at the moment of transaction (cash drops by price, deed value rises by the same amount). The only way it hurts me is if I then can't pay a rent that comes due. So: buy if, after paying, I still have enough cash to cover at least one maximum rent payment (the highest rent on the board). In practice with 200 starting cash this rarely blocks a purchase until late game.

**I buy more aggressively in early laps than in late laps.** With many laps remaining, there are many chances for the other players to land on my property and pay me rent. The expected rent income from a new purchase is roughly: (number of other players) × (1 / number of tiles) × (rent of the property) × (laps remaining after this one). I buy whenever that expectation is positive and I can afford it.

**On the final lap, I only buy if other players will still roll after me.** If I am the last investor to roll in the final lap, no one will land on a property I buy this turn, so the purchase is score-neutral with zero upside — skip it. If players still have rolls left after mine, buying on the final lap still has positive expected value and I apply the same affordability test.

**When I can choose which property to buy (limited cash, multiple options in play), I prioritize by rent.** Expected rent income is proportional to the rent value since all tiles get hit roughly equally often by the other players over the remaining laps.

**When I land on someone else's property, I pay the rent immediately.** No negotiation, no hesitation. The rent is a fixed cost.

**When I land on my own property, I do nothing.** No rent paid, no purchase.

**When I pass START, I add the salary to my balance.** Track it in the same arithmetic as everything else.

**Before making a purchase decision, I add any incoming rent noted in the prompt to my current balance.** The line "since your last turn you received X from other investors" is part of my available cash for that turn's decisions. I compute: (last declared balance + salary if passed START + rent received − rent paid) = available cash, then check if I can afford the purchase.

**To compute my declared balance each turn, I do:** last declared balance + salary (if I passed START) + rent received from others − rent paid to others − purchase price (if I bought). I do not re-derive from scratch; I start from the last declared balance and apply only this turn's changes.

**I watch my cash floor.** I estimate how much rent I might owe over the remaining laps (roughly: remaining laps × average rent of owned properties I'm likely to hit). If buying a property would drop me below that floor, I skip it and save the cash. In practice, with standard starting cash and rents in the 10–30 range, this is rarely binding until the later laps when I've already spent a lot and my balance is thin.

**The score is cash + deed value at the end.** This means my net position is only affected by (a) rent I collect from others and (b) rent I pay to others. Purchases themselves don't change my score. So the entire game is about maximizing rent collected minus rent paid, and the strategy is: hold high-rent properties and hope others land on them while avoiding landing on high-rent properties I don't own. Since I can't control rolls, the best I can do is buy every property I can afford (to increase my rent-collecting surface) and track my cash carefully.