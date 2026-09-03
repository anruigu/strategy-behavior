---
game: gen_quiet_sonar
model: gemini
condition: win
seed: 0
round: 1
chars: 854
---
When I am in the hide stage, I select a cell from 1 to 9 to hide my submarine. I choose this location randomly or by avoiding the recent firing patterns of the player targeting me.

When I am in the fire stage, I select a cell from 1 to 9 to shoot at my target. I must treat these numbers strictly as spatial coordinates, not as "power levels" or "damage." I will never repeatedly fire at the maximum number (e.g., 9) under the false assumption that it deals more damage; instead, I randomize my shots or try to predict my target's hiding spot to actually score hits.

When I am in the claim stage, I look at the private true result provided by the referee and submit exactly that result. I always claim [claim: hit] if the referee says HIT, and [claim: miss] if the referee says MISS, because the rules dictate that claims must match the private result.