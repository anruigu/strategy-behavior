---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1402
---
# Playbook for Shared Fishery (ref_commons)

### Core Strategy & Rules of Play

- **Seasons 1 through (Total Seasons - 1):**
  - When the current season is not the final season:
    - If other boats have been harvesting sustainably (or if it is Season 1), submit exactly the stated `sustainable share` (e.g., 11.1 at stock 100.0 with 3 boats).
    - If another boat consistently overfishes by a small amount, match their slightly elevated catch while keeping total extraction below the collapse threshold to avoid exploitation while preserving regrowth.
    - Never attempt to unilaterally drain the pool in non-final rounds; depleting the stock early destroys the compounding 50% regrowth yield.

- **Final Season:**
  - When the final season prompt appears (e.g., Season 6/6):
    - No future regrowth is needed, so harvest the remaining stock.
    - If opponents have been fully cooperative throughout, claim an equal fair share of the remaining stock: `Remaining Stock / Number of Boats` (e.g., `33.3` when stock is 100.0 with 3 boats).
    - If there is observed defection or high risk of greedy over-claiming, bid aggressively (up to `Remaining Stock / 2` or higher) to protect landing share under rationing.

- **Formatting & Execution:**
  - Keep reasoning strictly brief (1–2 sentences).
  - Always terminate the message with the exact format `[catch: N]`, with `N` rounded to 1 decimal place.