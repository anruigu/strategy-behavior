---
game: gen_quiet_sonar
model: gemini
condition: win
seed: 0
round: 1
chars: 747
---
When prompted to hide my submarine, I review the past fire coordinates of the player targeting me and choose a location (1-9) they have not recently checked. I vary my hiding locations to remain unpredictable.

When prompted to fire at my target, I treat the number as a spatial location to search, not a measure of damage or firepower. I systematically fire at a different location each round to sweep the grid and locate the target.

I do not repeatedly fire at the same coordinate (such as always firing 9) if my previous shots at that location were misses. 

When prompted to submit a claim, I output exactly the true result (hit or miss) that the referee privately told me, as the rules strictly require the claim to match the private result.