---
game: gen_quiet_sonar
model: gemini
condition: win
seed: 6
round: 1
chars: 862
---
When prompted for the hide stage, I select a random integer from 1 to 9. I do not hide in cells that my incoming shooter has frequently targeted in previous rounds, and I vary my hiding spots to remain unpredictable. 

When prompted for the fire stage, I treat the integer 1 to 9 as a coordinate to guess my target's hidden location, not as a damage value or power level. I do not repeatedly fire at the highest number (like 9) under the false assumption that it deals more damage. Instead, I fire at a coordinate where I suspect my target is hiding, varying my guesses across the available cells to maximize the chance of a hit.

When prompted for the claim stage, I submit exactly the result the referee privately told me. I do not attempt to bluff or overthink credibility, because the rules strictly require the public claim to match the private true result.