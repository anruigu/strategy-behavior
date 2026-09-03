---
game: hx_picket_checker
model: gemini
condition: win
seed: 4
round: 2
chars: 1293
---
When choosing a cell to hide in, I pick a random integer from 1 to 9, varying it each round so the opponent following the standing order has a hard time hitting me. 

When posting my station note, I use it to communicate with the other boats for mutual advantage. I explicitly propose a mutual escort to one of the other live player boats (e.g., "Let's mutual escort, Echo"). I should also read the notes from the previous round to see if any boat has proposed an escort to me.

When firing, I target the boat specified in the standing order and pick a random cell from 1 to 9. I do not mistake the fire coordinate for a "firepower" value; it is a location guess. I avoid firing at Harbor to prevent any potential retaliation that could remove me from the board.

When filing a claim, I always report exactly what the office privately tells me. If the office says HIT, I reply `[claim: hit]`. If MISS, I reply `[claim: miss]`.

When filing an escort claim (salvage), I never choose `[salvage: none]`. I check the notes relayed in the previous round: if a boat explicitly agreed to mutual escort or proposed one to me, I name them. Otherwise, I continue to name the boat I proposed an escort with in my own note, aiming to capture the 5-point mutual escort bonus if they eventually reciprocate.