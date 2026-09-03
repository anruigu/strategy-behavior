---
game: gen_quiet_sonar
model: gemini
condition: win
seed: 4
round: 1
chars: 672
---
When asked to hide my submarine, I select a coordinate between 1 and 9. I choose a location randomly but avoid cells that my incoming shooter has recently fired at. 

When asked to fire at my target, I select a coordinate between 1 and 9. I must remember that the fire value represents a location, not an "intensity" or "power level." I try to predict where they are hiding, often choosing cells that haven't been heavily targeted recently, varying my shots to remain unpredictable.

When asked to claim a result, I submit exactly the true result given to me by the referee. The rules require that the claim matches the private result, so I do not attempt to lie or bluff.