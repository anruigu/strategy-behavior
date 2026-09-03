---
game: gen_quiet_sonar
model: gemini
condition: win
seed: 2
round: 1
chars: 800
---
When choosing a hide location, I review the previous rounds to see which cells my predator has been firing at, and I select a cell they have consistently ignored. If there is no clear pattern, I select a random integer between 1 and 9 to remain completely unpredictable.

When choosing a fire location, I actively vary my targets across the 1-9 grid to hunt for my target's submarine. I do not treat the coordinate number as a power level or damage multiplier; firing at cell 9 repeatedly because it is the "maximum value" is a useless strategy that guarantees misses if the opponent avoids that single cell. 

When asked to submit a claim, I simply submit the exact result (hit or miss) that the referee privately told me, because the rules dictate that the claim must match the true private result.