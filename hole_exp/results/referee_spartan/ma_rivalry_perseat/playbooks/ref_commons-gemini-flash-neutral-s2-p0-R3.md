---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1241
---
# Playbook for Shared Fishery (ref_commons)

### Core Strategy & Rules of Play

- **Non-Final Seasons (Seasons 1 through T - 1):**
  - If it is Season 1 or all boats have been cooperating, submit exactly the prompt's stated `sustainable share` (e.g., `11.1` at stock 100.0 with 3 boats).
  - If other boats overfish, adjust catch to mirror the overfishing while ensuring post-harvest stock remains strictly above 0 so regrowth continues.
  - Never drain the stock early; preserving stock to regrow compounding yield maximizes the total cumulative catch.

- **Final Season (Season T of T):**
  - No future regrowth is required, so the entire remaining stock should be extracted.
  - If all boats have cooperated sustainably throughout, request an equal share of the current stock: `Current Stock / Total Boats` (e.g., `33.3` for 100.0 stock and 3 boats).
  - If opponents have previously defected or overfished, request a higher aggressive share (up to the full remaining stock or proportional contested allocation) to avoid being under-rationed.

- **Formatting & Execution:**
  - Keep reasoning brief (1–2 concise sentences).
  - Always conclude the reply with the required token format: `[catch: N]`, with `N` rounded to one decimal place.