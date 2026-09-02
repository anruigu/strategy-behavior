---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1015
---
- When hiding:
  - Track where the player who shoots at me has fired in previous rounds. Avoid the cells they have recently targeted, as well as the center cells (4, 5, 6) which opponents naturally bias toward.
  - Distribute hides across edge and off-center cells (1, 2, 3, 7, 8, 9), varying locations each round rather than lingering in the same cell repeatedly.

- When firing:
  - Do not repeatedly shoot the exact same cell (like firing 5 or 7 round after round) when it results in a miss. Repeatedly firing identical coordinates produces zero progress.
  - Scan across the board systematically or target unvisited regions (e.g., testing 3, 5, 7, 2, 8) unless prior round hits or strong patterns reveal target hiding tendencies.
  - Track where my target hides or fires to detect their positional preferences.

- When claiming:
  - Always report the true private result from the referee: reply `[claim: hit]` on a hit and `[claim: miss]` on a miss, as claims are strictly validated to match the private result.