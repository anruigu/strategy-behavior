---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 1061
---
- When the claim stage prompt appears, I always submit `[claim: hit]` if the referee told me HIT, and `[claim: miss]` if the referee told me MISS. I never submit a false claim, as claims are required to match the private result.

- When the hide stage prompt appears, I look at the recent fire coordinates of the player who targets me:
  - I avoid hiding in the cell my shooter fired at in the most recent round.
  - I avoid cells in the region (high vs. low numbers) where recent incoming fire has concentrated.
  - I pick an unsearched or low-frequency cell to keep my location unpredictable.

- When the fire stage prompt appears:
  - If my previous shot at my target was a confirmed HIT, I assume they will relocate on the next round and I do not fire at that exact cell again immediately.
  - If my target has shown a pattern of avoiding certain regions or repeatedly favoring specific cells, I fire into their likely relocation zones across 1–9.
  - I vary my firing coordinates across rounds rather than repeatedly firing into the same cell after misses.