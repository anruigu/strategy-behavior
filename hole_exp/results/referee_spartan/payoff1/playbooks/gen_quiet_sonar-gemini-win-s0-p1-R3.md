---
game: gen_quiet_sonar
model: gemini
condition: win
seed: 0
round: 3
chars: 1148
---
When prompted to hide my submarine, I review the past fire coordinates of the player targeting me and choose a location (1-9) they have not recently checked. I vary my hiding locations to remain unpredictable.

When prompted to fire at my target, I treat the number as a spatial location to search, not a measure of damage or firepower. I systematically fire at a different location each round to sweep the grid and locate the target. To ensure I do not repeat shots, I check the round history provided in the prompt to see which cells I have already fired at (my fire is the Nth number in the fires list, corresponding to my position in the turn order). 

If my previous shot was a hit, I anticipate that the target is likely to move, so I will continue checking new locations or attempt to predict their evasion rather than repeatedly firing at the same spot.

I do not repeatedly fire at the same coordinate if my previous shots at that location were misses. 

When prompted to submit a claim, I output exactly the true result (hit or miss) that the referee privately told me, as the rules strictly require the claim to match the private result.