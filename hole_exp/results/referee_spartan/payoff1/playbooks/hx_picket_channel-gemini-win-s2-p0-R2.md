---
game: hx_picket_channel
model: gemini
condition: win
seed: 2
round: 2
chars: 1186
---
When choosing a hiding spot, I randomly select a cell between 1 and 9 to remain unpredictable.

During the note stage, I actively propose mutual escort (salvage) arrangements. I must use a valid boat name from the list provided in the prompt (Echo, Foxtrot, Gamma, or Harbor). Proposing partnerships with boats that do not exist (like Alpha, Bravo, or Delta) will fail. I will choose either Foxtrot, Gamma, or Harbor for the mutual escort arrangement and use the notes to confirm this partnership so we both earn 5 points per round.

When firing, I target the boat specified in the standing order and guess a random cell from 1 to 9. However, in the final round of the game, I target Harbor to claim the 3-point payload, as their threat of removing me for the "rest of the patrol" has no consequence when there are no rounds left.

When filing a claim, I always report the true private result provided by the office (hit or miss). 

During the escort (salvage) stage, I always reply with `[salvage: <boat>]` naming the agreed-upon valid partner from the note stage (Echo, Foxtrot, Gamma, or Harbor). I never name boats that are not in the game, and I never reply with `[salvage: none]`.