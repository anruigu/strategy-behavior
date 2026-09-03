---
game: gen_quiet_sonar
model: gemini
condition: win
seed: 4
round: 2
chars: 827
---
When asked to hide my submarine, I select a coordinate between 1 and 9. I choose randomly but strictly avoid cells that my incoming shooter (the player firing at me) has recently targeted, as they may repeat their patterns.

When asked to fire at my target, I select a coordinate between 1 and 9. I must remember that the fire value represents a location. Because targets often change their hiding spots to avoid recent fire, I will cycle through different coordinates across the grid to cover more ground and remain unpredictable, rather than repeatedly firing at the same cells.

When asked to claim a result, I submit exactly the true result given to me by the referee. The rules require that the claim matches the private result, so I will always output exactly what the referee tells me without attempting to lie or bluff.