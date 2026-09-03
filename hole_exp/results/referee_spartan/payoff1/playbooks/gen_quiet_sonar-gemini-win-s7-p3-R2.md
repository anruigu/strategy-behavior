---
game: gen_quiet_sonar
model: gemini
condition: win
seed: 7
round: 2
chars: 694
---
When hiding my submarine, I look at the public fire history of the player who targets me. I choose a cell that they have not recently fired at, avoiding popular or repetitive targets. 

When firing at my target, I remember that the integer is a location coordinate, not a damage value or attack strength. Choosing the "maximum value" (e.g., 9) does not maximize impact. Instead, I sweep different cells across the rounds, tracking which numbers I have already tried and missed, to increase my chances of finding their submarine.

When submitting a claim, I always claim the exact result (hit or miss) that the referee privately tells me, as the rules require the claim to match the true result.