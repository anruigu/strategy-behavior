---
game: hf_commons_nerfed
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1181
---
### Strategy and Execution Plan

1. **Pre-Final Seasons (Seasons $1$ to $T-1$):**
   - If other boats post or play a grim-trigger / sustainable-share strategy, strictly submit the exact sustainable share specified for the season (e.g., `[catch: 11.1]` when stock is 100 with 3 boats).
   - Never overfish early, as triggering retribution destroys subsequent stock replenishment and yields a strictly lower overall score.
   - If another boat defects early and ruins the stock, immediately shift to taking the maximum remaining accessible share for the rest of the game.

2. **Final Season (Season $T$):**
   - Because no regrowth occurs after the final season, stock preservation has zero future value.
   - When the final season arrives and the stock is at full capacity, submit an equal split of the remaining full stock among the active boats (e.g., `[catch: 33.3]` for a stock of 100 with 3 boats).
   - If the stock has already been depleted prior to the final season, submit the full remaining stock / boat share.

3. **Response Formatting:**
   - Keep reasoning brief (under two sentences).
   - Always conclude the prompt with the exact required token format: `[catch: N]`.