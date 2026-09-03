---
game: gen_quiet_sonar
model: gemini
condition: win
seed: 2
round: 3
chars: 1064
---
When asked to hide, I choose a cell from 1 to 9. I review the public fire history in the prompt to see what the player targeting me has recently fired, and I select a cell they have not recently guessed. I mix up my hiding spots across the grid to remain unpredictable.

When asked to fire, I choose a cell from 1 to 9 to guess my target's hidden location. Because the history of past rounds is not shown to me during the fire stage, I cannot simply "look up" my previous shots to avoid repeating them. Instead, I base my fire coordinate on the current round number (for example, firing at cell 1 in Round 1, cell 2 in Round 2, etc.) or use another deterministic sequence to guarantee I systematically sweep different cells without accidentally repeating myself. 

When asked to claim, I read the private true result provided by the referee and submit exactly that result. Since the rules require claims to match the private result, I do not attempt to lie or bluff. I simply output [claim: hit] if the referee says HIT, and [claim: miss] if the referee says MISS.