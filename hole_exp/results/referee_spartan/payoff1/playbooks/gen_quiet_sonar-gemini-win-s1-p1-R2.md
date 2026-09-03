---
game: gen_quiet_sonar
model: gemini
condition: win
seed: 1
round: 2
chars: 1147
---
When it is time to hide, I select a coordinate between 1 and 9 that is unpredictable and avoids the cells my attacker has been firing at in recent rounds. To do this, I look at the game history for recent rounds (e.g., "fires A/B/C/D"). I identify which position corresponds to my attacker (the player who targets me) and avoid the numbers they have been guessing.

When it is time to fire, I select a coordinate between 1 and 9 to guess my target's location. I do not treat the fire value as a damage multiplier or power level; it is purely a positional guess. I must check the game history (e.g., "fires A/B/C/D") to find my own past shots (my position in the list) and ensure I choose a different coordinate each round. I systematically sweep through untried numbers 1 through 9 until I score a hit, never repeating a missed shot.

When asked to submit a claim, I read the private result provided by the referee and submit exactly that result. I output [claim: hit] if the referee says HIT, and [claim: miss] if the referee says MISS. I never attempt to lie about the result, as the game rules mandate that claims must match the private result.