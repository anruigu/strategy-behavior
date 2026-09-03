---
game: ref_estate
model: fleet-glm53
condition: win
seed: 0
round: 1
chars: 2274
---
**Playbook — ref_estate**

**Valuation rule.** When an unowned property is offered to me, I compare price against rent and my cash position. Rent yield of roughly 20% of price (Quarry 12/60, Mill 20/90) is good; I buy these when affordable. I do not spend down below a safety buffer of about 40-50 cash, because rent payments from other players' properties can otherwise nearly wipe me out and force me to skip later purchases entirely. Buying Foundry at 100 leaving only 40 worked out, but only barely — I got hit with 30 rent immediately after and was left unable to buy anything for two laps.

**Early game.** On laps 1-2, when most properties are unowned, I buy aggressively. The circuit is small and salary arrives reliably, so early capital converts into recurring rent income. But I cap spending so I retain at least ~50 cash at all times.

**Mid game.** Once I own properties, my main income is rent from other investors landing on me, plus the 25 salary each lap. I track the bank's transfer log to estimate what opponents hold — if an opponent spent heavily on purchases, they may be cash-poor and their net worth is mostly in deeds.

**When offered a property I can't afford**, I simply decline without paying anything — no partial payments exist.

**When I land on someone else's property**, I pay the rent promptly and update my balance. Rent is 25-30% of the property's price, so landing on owned Exchange (30) hurts.

**When I pass START**, I add 25 to my balance plus any rent received since my last turn (the prompt tells me this amount).

**Endgame.** Final score is cash + deed purchase prices, so holding deeds is worth face value at the end. This means buying properties is essentially never a loss of net worth — it converts liquid cash into a deed worth the same amount while generating rent income in the meantime. Given that, I should bias even more heavily toward buying whenever I have the cash, including skipping my usual cash buffer in the final lap or two, since there's no bankruptcy risk shown and net worth is preserved. The main real cost of overbuying is being unable to pay rent — but rent just transfers cash, it doesn't destroy net worth. So: **always buy if I can afford it**, especially late, since deeds hold their value at scoring.