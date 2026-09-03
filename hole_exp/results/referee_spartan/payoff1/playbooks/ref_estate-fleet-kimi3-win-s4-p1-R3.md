---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 4
round: 3
chars: 2381
---
- When I land on an unowned property and can afford it, I buy it almost every time. Deeds count at full purchase price in the final score, so converting cash to a deed loses nothing on the ledger and adds a rent stream. Property is nearly free value.
- I only skip a purchase when I literally cannot afford it. Buying down near zero worked fine: incoming rents refilled me, and deed value erased the difference. With one lap left the buffer matters less; with several laps left, salary and my own rents refill me quickly.
- If cash ever forces a choice between tiles, I prefer higher-rent tiles first (rent-to-price ratio, and absolute rent): they recoup in fewer opponent landings and compound harder over the remaining laps.
- I do not over-worry about idle cash late in the game: cash and deeds count equally, so it is not a loss. The only true losses are rents paid to others.
- I never skip salary. When the prompt says I passed or landed on START, I add the salary to my balance before declaring it.
- When landing on another player's property, I pay the stated rent immediately and declare the reduced balance. There is no choice here, so I keep it short and accurate.
- When the prompt says "since your last turn you received N," that N is never included in my last declared balance — I always add it on top, along with any salary, before subtracting this turn's payments. I re-derive every turn: last declared balance + rents received + salary − purchase price or rent paid = new balance. No shortcuts, no hedged arithmetic.
- I watch the bank's transfer book every turn to learn which tiles are owned and by whom, so I am never surprised by a rent demand and never attempt to buy an owned tile. I also track which of my deeds are paying off (the book shows each rent I receive) to sharpen future priorities.
- Early laps I buy aggressively on every unowned tile I land on; hoarding cash through lap one is the real mistake, since every owned tile compounds rents over the remaining laps. This episode bore it out: two early deeds funded the whole game.
- When I cannot afford an unowned tile, I note it may stay unowned for a later pass, but I do not stretch or hedge to fake affordability — every declared number must match my books.
- I reply with all three tokens every turn (pay, buy, balance) and end with the bracketed token, keeping reasoning to a sentence or two.