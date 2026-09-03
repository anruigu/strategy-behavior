---
game: gen_quiet_sonar
model: gemini
condition: win
seed: 3
round: 1
chars: 631
---
When choosing a cell to hide in, I select an integer from 1 to 9 that my attacker has not recently fired at, varying my choices to remain unpredictable.
When choosing a cell to fire at, I select an integer from 1 to 9 to guess my target's hidden location, systematically checking different cells over the rounds.
I do not treat the fire coordinate as a resource to spend or a power level to maximize; cell 9 is just a location, exactly like cell 1.
When prompted to make a claim, I always claim the exact true result (hit or miss) provided by the referee, because the game rules strictly require claims to match the private result.