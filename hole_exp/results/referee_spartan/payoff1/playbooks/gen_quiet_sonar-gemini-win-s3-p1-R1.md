---
game: gen_quiet_sonar
model: gemini
condition: win
seed: 3
round: 1
chars: 820
---
When asked to hide my submarine, I choose an integer from 1 through 9 that varies from my previous locations and avoids the recent firing patterns of my attacker. 

When asked to fire at my target, I choose an integer from 1 through 9 that represents a spatial coordinate to guess their hidden location. I do not treat the fire value as an amount of "damage" or "firepower"; repeatedly firing at 9 under the assumption that it maximizes damage does not work and guarantees misses against an evasive target. I vary my firing coordinates every round.

When asked to make a claim, I read the true result of the shot provided privately by the referee and submit exactly that result. I do not deliberate on lying or building credibility, as the game rules explicitly require the public claim to match the private true result.