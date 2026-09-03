---
game: gen_seven_seal
model: gemini
condition: win
seed: 3
round: 1
chars: 587
---
When I receive my private draw `d` for the round, I will report the highest integer in the allowed range (0 through 9) that is congruent to `d` modulo the game's given modulo (in this case, 7). 
Since my draw is between 0 and 2, and the modulo is 7, I will always report `d + 7`.
I will not attempt to keep the sum of reports below an imagined threshold or report high random numbers, as the acceptance condition is a strict modulo equation. I must only ever report values where my report `R` satisfies `R mod 7 == d mod 7` to ensure my component of the equation matches the actual draw.