---
game: gen_quiet_sonar
model: gemini
condition: win
seed: 4
round: 2
chars: 950
---
When I am asked to hide, I review the previous rounds' firing history to see which cells the player targeting me has been guessing. I choose a cell number between 1 and 9 that they have not recently fired at. 

When I am asked to fire, I treat the number (1 through 9) strictly as a location coordinate to guess where my target is hiding. I do not treat the number as a "firepower level" or "damage amount" to be maximized. To effectively hunt for the target's hiding spot, I must systematically sweep through the numbers (e.g., 1, 2, 3, 4, 5, 6). I will look at my own firing history in previous rounds and ensure I fire at a completely new cell each round, rather than repeatedly guessing the same middle numbers.

When I am asked to claim, I submit exactly the result (hit or miss) that the referee privately told me. I do not agonize over deception or strategy here, because the rules strictly dictate that my claim must match the private result.