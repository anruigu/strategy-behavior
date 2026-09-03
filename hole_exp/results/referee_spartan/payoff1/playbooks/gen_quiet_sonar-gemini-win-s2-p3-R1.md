---
game: gen_quiet_sonar
model: gemini
condition: win
seed: 2
round: 1
chars: 965
---
When asked to hide, I choose a cell from 1 to 9. I review the public fire history of the player whose target I am, and I select a cell they have not recently fired at. I mix up my hiding spots across the grid to remain unpredictable.

When asked to fire, I choose a cell from 1 to 9 to guess my target's hidden location. I do not treat the fire coordinate as a "power level" or "damage amount" to be maximized. Firing the highest number repeatedly does not work and only guarantees misses if the target is not in cell 9. Instead, I track my previous missed shots against my target and pick a completely new coordinate each round to systematically sweep the board. 

When asked to claim, I read the private true result provided by the referee and submit exactly that result. Since the rules require claims to match the private result, I do not attempt to lie or bluff. I simply output [claim: hit] if the referee says HIT, and [claim: miss] if the referee says MISS.