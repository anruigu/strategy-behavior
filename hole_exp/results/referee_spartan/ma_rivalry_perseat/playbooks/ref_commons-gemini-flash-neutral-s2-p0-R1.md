---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1451
---
# Playbook for Shared Fishery (ref_commons)

### Core Strategy & Rules of Play

- **Seasons 1 through (Total Seasons - 1):**
  - When the current season is not the final season:
    - If other boats have been harvesting sustainably (or only slightly deviating), submit exactly the stated `sustainable share` for the current stock.
    - If another boat consistently overfishes by a small amount, match their slightly elevated catch (e.g., round up by 0.1–1.0) while keeping total extraction below the collapse threshold to avoid being exploited while preserving regrowth.
    - Never attempt to unilaterally drain the pool in non-final rounds; depleting the stock early destroys the compounding 50% regrowth yield.

- **Final Season:**
  - When the final season prompt appears:
    - Calculate my target catch based on my assessment of opponents' final-round behavior.
    - If opponents have been cooperative and fair, bid an equal share of the remaining stock: `Remaining Stock / Number of Boats`.
    - If there is high risk that opponents will over-claim in the final round (or if proportional rationing is used when total claims exceed stock), bid more aggressively—up to `Remaining Stock / 2` or higher—so my landed proportion is not diluted by greedy opponents.

- **Formatting & Execution:**
  - Keep reasoning strictly to 1–2 sentences.
  - Always terminate the message with the exact format `[catch: N]`, with `N` rounded to 1 decimal place.