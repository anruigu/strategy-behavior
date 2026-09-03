---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 4
round: 1
chars: 1943
---
- When I land on an unowned property and can afford it, I buy it almost every time. Deeds count at full purchase price in the final score, so converting cash to a deed loses nothing on the ledger and adds a rent stream. Property is nearly free value.
- I only skip a purchase if buying would leave me unable to pay a plausible upcoming rent before my next salary — I keep a small buffer (roughly one typical rent, ~25–30) unless the laps are nearly over.
- When sitting on cash late in the game with no purchase likely, I do not over-worry: cash and deeds count equally, so idle cash is not a loss. The only true losses are rents paid to others.
- I never skip salary. When the prompt says I passed START, I add 25 to my balance before declaring it — forgetting this is throwing away points.
- When landing on another player's property, I pay the stated rent immediately and declare the reduced balance. There is no choice here, so I keep this short and accurate.
- When landing on my own property, I do nothing except reconcile: I add any rents the bank's book shows I received since my last turn before declaring my balance. I always check "since your last turn you received N" and incorporate it.
- I track my own balance line by line every turn: start from my last declared balance, subtract rent paid or purchase price, add salary and rents received, then declare. I never trust memory without re-deriving from the last declared figure shown in the prompt.
- I watch the bank's transfer book to learn which tiles are owned and by whom, so I am never surprised by a rent demand and never attempt to buy an owned tile.
- Early laps I buy aggressively even down to low cash, because salary replenishes me each circuit and opponents landing on me pay me; holding 200 cash unspent through lap one is the real mistake to avoid.
- I reply with all three tokens every turn and end with the bracketed token, keeping reasoning to a sentence or two.