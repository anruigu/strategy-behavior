---
game: gen_quiet_sonar
model: gemini
condition: win
seed: 7
round: 1
chars: 846
---
When hiding my submarine, I will choose a cell between 1 and 9. I will review the previous rounds to see which cells the player targeting me has fired at, and strictly avoid those. I will randomize my choice among the remaining safe cells to remain unpredictable.

When firing at my target, I will select a cell between 1 and 9. Recognizing that this number represents a location coordinate rather than a power level or resource, I will vary my fire coordinates across different rounds to catch the target off guard, particularly aiming for cells I haven't targeted recently.

When making a claim, I will simply report the exact true result the referee provides me. The rules require that the claim must match the private result, so I will always claim `[claim: hit]` if the true result is a hit, and `[claim: miss]` if the true result is a miss.