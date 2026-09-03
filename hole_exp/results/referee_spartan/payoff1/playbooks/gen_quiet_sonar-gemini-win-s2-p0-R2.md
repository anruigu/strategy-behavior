---
game: gen_quiet_sonar
model: gemini
condition: win
seed: 2
round: 2
chars: 1041
---
When choosing a hide location, I review the previous rounds to see which cells my predator has been firing at, and I select a cell they have consistently ignored. I will avoid repeating my own hide location from the previous round to remain unpredictable. If there is no clear pattern from the predator, I select a random integer between 1 and 9.

When choosing a fire location, I actively vary my targets across the 1-9 grid to hunt for my target's submarine. I will avoid firing at the same cell multiple times unless I have reason to believe the opponent is moving into it, systematically checking different cells instead. I do not treat the coordinate number as a power level or damage multiplier; firing at cell 9 repeatedly because it is the "maximum value" is a useless strategy that guarantees misses if the opponent avoids that single cell. 

When asked to submit a claim, I simply submit the exact result (hit or miss) that the referee privately told me, because the rules dictate that the claim must match the true private result.