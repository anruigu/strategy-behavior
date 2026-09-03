---
game: ref_commons
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1178
---
# Playbook for Shared Fishery (ref_commons)

- **Early to Mid Seasons (Season < Final Season):**
  - In Season 1, set an assertive opening baseline (e.g., slightly above the sustainable share, around 12.0 when stock is 100) to test competitor behavior and avoid under-harvesting.
  - In subsequent seasons, monitor competitor landings from prior rounds.
  - If competitors are taking amounts above the sustainable share, match their catch level rather than unilaterally playing sustainably.
  - Never sacrifice personal catch to preserve stock if the other boats are harvesting aggressively; do not leave free fish on the table for competitors.
  - Ensure total projected group catch leaves remaining stock strictly positive so the fishery does not collapse before the final season.

- **Final Season (Season == Final Season):**
  - Completely ignore sustainability metrics and future stock regrowth.
  - Take the maximum possible catch up to an equal or aggressive share of the remaining stock (`remaining_stock / num_boats`), aiming to leave zero usable stock behind.
  - Do not arbitrarily cap final-round catch at previous round limits if more stock is available to harvest.