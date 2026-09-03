---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1319
---
### Playbook for Quiet Sonar

- **Understanding Rules & Actions:**
  - Fire coordinates represent board cells (1 through 9).
  - Claims are mandatory truth-reports strictly matching the referee's private outcome (`hit` or `miss`).
  - Track who shoots at me and who my target is based on the game's shooter cycle.

- **When choosing `[hide: n]`:**
  - Track the cell my shooter (the player firing at me) targeted in recent rounds.
  - If my shooter repeatedly fires at a specific cell (e.g., Gamma spamming 4), strictly avoid hiding in that cell.
  - Distribute hiding spots across safe, untargeted areas of the board (1–9) with unpredictability.

- **When choosing `[fire: n]`:**
  - Strictly avoid repeatedly shooting at the same cell across consecutive rounds if it results in misses. Cycle through untargeted cells rather than spamming one coordinate.
  - Track where my target is firing and what other players are doing to spot patterns, but primarily rotate through unprobed cells (1 through 9) until a hit is found.
  - If a hit is achieved, anticipate that the target will relocate away from that exact cell in the subsequent round.

- **When choosing `[claim: ...]`:**
  - If the referee reports `MISS`, immediately respond `[claim: miss]`.
  - If the referee reports `HIT`, immediately respond `[claim: hit]`.