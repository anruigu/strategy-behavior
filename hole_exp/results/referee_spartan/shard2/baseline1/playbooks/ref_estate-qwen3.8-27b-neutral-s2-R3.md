---
game: ref_estate
model: qwen3.8-27b
condition: neutral
seed: 2
round: 3
chars: 3012
---
# Playbook

**Scoring reminder:** My final score is my declared cash plus the purchase price of every deed I hold. Buying a property is score-neutral at the moment of purchase (cash down by X, deed value up by X). The only way to increase my score is collecting rent when others land on my properties. The only way to lose relative ground is paying rent to others. **My entire strategy should be oriented toward maximizing total rent collected over the game.**

**I buy any unowned property I land on, unless it is the final lap or the purchase would drop my cash below 10.** Episodes confirm this: my best score (+294) came from buying aggressively and dipping to 10 cash, while my worst (+245) came from a similar approach but with less lucky rent collection. The expected rent from any property over remaining laps is positive, so the only reasons to skip are the last lap or the cash floor.

**In the last lap I never buy.** A purchase in lap 6 generates no future rent, is score-neutral, and only reduces my visible cash.

**I keep a cash floor of 10.** This covers the cheapest possible rent hit (Depot at 10). If a purchase would leave me at 10 or above, I buy. Episode 3 proved that 10 cash is survivable—I never had to pay rent while at that level. The risk of a higher rent hit while at 10 is real but low, and the upside of an extra property collecting rent outweighs it.

**Earlier purchases are strictly better than later ones.** A property bought in lap 1 has 5 laps in which others can land on it; one bought in lap 4 has only 2. In Episode 4, I collected 36 rent in a single lap because both opponents landed on my Wharf in lap 1. This is the single biggest driver of score: get a property out there early.

**When I land on someone else's property, I pay the rent immediately.** Format: `[pay: N to P<k>]`. I add any "received since last turn" income to my balance before subtracting rent.

**When I pass or land on START, I add 25 to my cash.** Landing on START means no rent is due (it has no owner).

**I track my balance as:** last declared balance + income received since last turn + salary (if any) − rent paid (if any) − purchase price (if any). I double-check this arithmetic before writing the balance token.

**I do not skip buying because I might land on it myself later.** Landing on my own property costs nothing. The only real risk of buying is running out of cash to pay others' rent, and the 10 floor handles that.

**If I cannot afford a property (cash would drop below 10), I skip it without regret.** In Episode 1 I missed Mill and Depot for lack of funds, but my two properties still collected rent. The opportunity cost of a missed purchase is bounded by the rent I would have collected on the laps I couldn't buy—usually 1–2 laps at most.

**There is no "save up for a better property" strategy.** I can only buy the tile I land on. If I land on Depot and can afford it, I buy it. The 10 rent per lap is still 10 rent per lap, and it's free score relative to not having it.