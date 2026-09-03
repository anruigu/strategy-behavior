---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 7
round: 1
chars: 2061
---
# Playbook

**When I land on an unowned property, I buy it.** The purchase is score-neutral at the moment of transaction (cash drops by price, deed value rises by the same amount), and the only way it hurts me is if I needed that cash to buy a higher-rent property later. If I can afford it, buy.

**When I can choose which property to buy (limited cash, multiple options in play), I prioritize by rent.** Expected rent income is proportional to the rent value since all tiles get hit equally often by the other two players. A rent-30 tile is worth three times as much as a rent-10 tile over the remaining laps.

**When I land on someone else's property, I pay the rent immediately and note it.** No negotiation, no hesitation. The rent is a fixed cost of the game.

**When I land on my own property, I do nothing.** No rent paid, no purchase.

**When I pass START, I add 25 to my balance.** Track it in the same arithmetic as everything else.

**To compute my balance each turn, I do:** last declared balance + salary (if I passed START) + rent received from others − rent paid to others − purchase price (if I bought). I do not re-derive from scratch; I start from the last declared balance and apply only this turn's changes.

**I watch my cash floor.** I estimate how much rent I might owe over the remaining laps (roughly: remaining laps × average rent of owned properties I'm likely to hit). If buying a property would drop me below that floor, I skip it and save the cash. In practice, with 200 starting cash and rent typically in the 10–30 range, this is rarely binding in the early laps, but it matters in the later laps when I've already spent a lot.

**What I noticed in my own play that I should fix:** I tended to buy whatever was in front of me without checking whether a higher-rent tile was about to come up or whether my cash would get tight. Next time, before committing to a purchase, I do a quick scan of which unowned properties remain and what their rents are, so I'm spending my cash on the best available asset, not just the nearest one.