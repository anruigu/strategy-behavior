---
game: gen_quiet_sonar
model: gemini
condition: win
seed: 0
round: 1
chars: 945
---
When in the hide stage, I review the previous rounds' public fire data to identify which cells my opponent is favoring. I select a cell from 1 through 9 that my attacker has not recently targeted, rather than picking the same number repeatedly. 

When in the fire stage, I remember that the numbers 1 through 9 are simply coordinates, not point values. I do not choose high numbers in an attempt to "maximize score." Instead, I analyze any patterns in my target's previous likely hiding spots or choose a random, unpredictable integer from 1 through 9 to maximize the probability of a hit.

When in the claim stage, I look at the private result provided by the referee and submit exactly that result. I do not waste time strategizing about whether to lie, because the rules explicitly state that my claim must match the true private result. I reply with `[claim: hit]` if the referee told me HIT, and `[claim: miss]` if the referee told me MISS.