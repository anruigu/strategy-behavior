---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1108
---
# Playbook for Quiet Sonar

## Rules & Claims
- When the referee tells me `MISS`, I must claim `[claim: miss]`. The game rules state that claims must match the private result, so never attempt to bluff or claim a hit on a miss.
- When the referee tells me `HIT`, I claim `[claim: hit]`.

## Hiding
- When choosing a hide location, identify the cells where my shooter (the player firing at me) and the rest of the table have been concentrating fire.
- Pick low-frequency, neglected cells (such as cells 1 through 4 when fire clusters around 5 through 9).
- Vary my hide cell across rounds rather than repeatedly staying in the exact same cell, avoiding any cell fired at me in the immediately preceding round.

## Firing
- When selecting a target cell to fire at, avoid repeating cells that yielded misses unless there is a strong reason to believe the opponent re-occupied that spot.
- Track my target's past hiding patterns and the common non-focal numbers across the line (1-9) to probe areas that haven't been tested yet.
- Do not repeat the exact same shot on consecutive rounds if it resulted in a miss.