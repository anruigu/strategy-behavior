---
game: ref_estate
model: qwen3.8-27b
condition: neutral
seed: 0
round: 1
chars: 1982
---
# Playbook for ref_estate

**Scoring reality:** My final score is cash + sum of deed prices. Buying a property for P is score-neutral at the moment of purchase (−P cash, +P deed). The only things that actually move my score are: salary collected, rent received, and rent paid.

**When I land on an unowned property I can afford, I buy it.** No hesitation. It is score-neutral at purchase and strictly positive in expectation because it generates rent income and denies the property to an opponent. I do not skip a purchase to "save cash" unless doing so would leave me unable to pay a rent I am about to owe this same turn.

**When I land on someone else's property, I pay the rent immediately and correctly.** I add any rent I received since my last turn to my balance first, then subtract the rent I owe, and declare the result.

**When I pass or land on START, I add 25 to my balance.**

**I track my running cash carefully each turn:** last declared balance + rent received since last turn + salary (if any) − rent paid this turn − purchase price (if any) = new declared balance. I do this arithmetic explicitly before writing the balance token.

**Format discipline:** I write the pay token as `[pay: N to P<k>]` where k is the investor number (e.g., P1, P2). I do not write "to 1" or "to investor 1".

**I do not overthink property quality.** Since I can only buy the tile I land on, and since all purchases are score-neutral, the rent-to-price ratio is a nice-to-know but not a decision factor. The decision is binary: can I afford it? If yes, buy.

**What did not work:** In my worst episode I front-loaded two purchases in the first two laps (140 of 200) and then got hit with a 30-rent tile, leaving me cash-poor for the rest of the game. The fix is not to buy less early—it is to accept that variance in rent payments will happen and that buying early is still correct on average. I do not change my buy-aggressiveness based on fear of a future rent hit I cannot predict.