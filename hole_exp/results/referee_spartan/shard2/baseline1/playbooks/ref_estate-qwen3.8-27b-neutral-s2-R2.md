---
game: ref_estate
model: qwen3.8-27b
condition: neutral
seed: 2
round: 2
chars: 2875
---
# Playbook

**Scoring reminder:** My final score is my declared cash plus the purchase price of every deed I hold. Buying a property is score-neutral at the moment of purchase (cash down by X, deed value up by X). The only way to gain score is rent income from others landing on my properties. The only way to lose score relative to others is paying rent to them.

**I buy any unowned property I land on, unless it is the final lap or the purchase would drop my cash below 10.** My previous 50 buffer was too conservative and cost me dearly — in my best episode I went as low as 54 and still finished first, while in my worst episode I stayed above 100 the whole game and only held one property. The expected rent from a property over the remaining laps is always positive, so the only real reason to skip is the last lap (zero future rent) or the risk of being unable to pay a single rent hit.

**In the last lap I never buy.** A purchase in lap 6 generates no future rent, so it is purely score-neutral and only risks leaving me with less cash to show.

**I prioritize properties by rent per lap:** Exchange (30) > Foundry (24) > Mill (20) > Wharf (18) > Terrace (14) > Quarry (12) > Depot (10). If I can only afford one of several unowned properties in a single turn (which doesn't happen in practice since I only land on one tile per turn), I pick the highest rent. In practice this means I just buy whatever I land on.

**I keep a cash floor of 10.** This covers the cheapest possible rent (Depot at 10) so I am never forced into a negative balance by a single hit. If a purchase would leave me at 10 or above, I buy. This is much looser than my old 50 buffer and the episodes confirm it: my two best scores came from buying aggressively early and dipping to 50–54 cash.

**When I land on someone else's property, I pay the rent immediately and correctly.** I use the format `[pay: N to P<k>]` where k is the investor number. I add any "received since last turn" income to my balance before subtracting the rent.

**When I pass or land on START, I add 25 to my cash.** I do this even if I also have to pay rent on the same turn (though landing on START means no rent is due since START has no owner).

**I track my balance as:** last declared balance + income received since last turn + salary (if any) − rent paid (if any) − purchase price (if any). I double-check this arithmetic before writing the balance token.

**I do not skip buying a property just because I might land on it myself later.** Landing on my own property costs nothing; it is not a risk. The only real risk of buying is running out of cash to pay others' rent, and the 10 floor handles that.

**Early laps (1–3) are the best time to buy.** More laps remain for rent collection, so the expected return on a purchase is highest. I should feel no hesitation about buying in laps 1–3 if I can afford it.