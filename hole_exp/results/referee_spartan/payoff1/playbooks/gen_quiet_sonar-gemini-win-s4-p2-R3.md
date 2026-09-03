---
game: gen_quiet_sonar
model: gemini
condition: win
seed: 4
round: 3
chars: 1105
---
When asked to hide my submarine, I select a coordinate between 1 and 9. I choose randomly but strictly avoid cells that my incoming shooter (the player targeting me) has recently fired at. To do this, I identify my shooter's position in the turn order and check their recent fires in the history, as they may repeat their patterns or sweep adjacent cells.

When asked to fire at my target, I select a coordinate between 1 and 9. I must remember that the fire value represents a location. Because targets often change their hiding spots to avoid recent fire, I will cycle through different coordinates across the grid. I will carefully read the history to identify my own past fires (using my position in the firing order) and strictly avoid repeating a coordinate I recently fired at, especially if I scored a hit, as the target is almost guaranteed to move.

When asked to claim a result, I submit exactly the true result given to me by the referee. The rules require that the claim matches the private result, so I will always output exactly what the referee tells me without attempting to lie or bluff.