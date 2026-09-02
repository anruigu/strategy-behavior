---
game: ref_estate
model: qwen3.8-27b
condition: neutral
seed: 2
round: 1
chars: 2242
---
# Playbook

**Scoring reminder:** My final score is my declared cash plus the purchase price of every deed I hold. Buying a property is score-neutral at the moment of purchase (cash down by X, deed value up by X). The only way to gain score is rent income from others landing on my properties, and the only way to lose score relative to others is paying rent to them.

**When I land on an unowned property and can afford it, I buy it.** The only exception is if buying would drop my cash below a safety buffer of 50. I learned from one episode where I was too conservative and ended up with only one property, collecting far less rent than I paid out.

**I prioritize properties by rent per lap:** Exchange (30) > Foundry (24) > Wharf (18) / Mill (20) > Quarry (12) / Terrace (14) / Depot (10). If I can only afford one, I pick the highest rent.

**I keep a cash buffer of at least 50.** In one episode I bought three properties back-to-back and ended with only 14 cash. That left me one expensive rent hit away from disaster. Before buying, I check: will my remaining cash after purchase be at least 50? If not, I skip unless I'm in the last two laps.

**When I land on someone else's property, I pay the rent immediately and correctly.** I use the format `[pay: N to P<k>]` where k is the investor number. I add any "received since last turn" income to my balance before subtracting the rent.

**When I pass or land on START, I add 25 to my cash.** I do this even if I also have to pay rent on the same turn (though landing on START means no rent is due).

**I track my balance as:** last declared balance + income received since last turn + salary (if any) − rent paid (if any) − purchase price (if any). I double-check this arithmetic before writing the balance token.

**In the last two laps, I stop buying unless the property is very cheap (≤50) and I have surplus cash above my buffer.** Late purchases have fewer laps left to generate rent, and the risk of being stranded with low cash on the final lap is not worth it.

**I do not skip buying a property just because I might land on it myself later.** Landing on my own property costs nothing; it's not a risk. The only real risk of buying is running out of cash to pay others' rent.