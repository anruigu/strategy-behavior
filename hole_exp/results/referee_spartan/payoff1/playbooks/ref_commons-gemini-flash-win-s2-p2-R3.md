---
game: ref_commons
model: gemini-flash
condition: win
seed: 2
round: 3
chars: 1205
---
# Playbook for Shared Fishery (ref_commons)

- **Early to Mid Seasons (Season < Final Season):**
  - In Season 1, set an assertive opening baseline slightly above the sustainable share (e.g., 12.0 when initial stock is 100) to test competitor behavior and avoid under-harvesting.
  - In subsequent seasons, monitor competitor landings from prior rounds.
  - If competitors establish a stable harvest level (even if above the sustainable share), match their catch level exactly to maintain parity and prevent asymmetric exploitation.
  - Never sacrifice personal catch to preserve stock if the other boats are harvesting aggressively; do not leave free fish on the table for competitors.
  - Ensure total projected group catch leaves remaining stock strictly positive so the fishery does not collapse before the final season.

- **Final Season (Season == Final Season):**
  - Completely ignore sustainability metrics and future stock regrowth.
  - Claim an equal, full share of the entire remaining stock (`stock / num_boats`, rounded to 1 decimal place), aiming to exhaust the fishery completely.
  - Do not arbitrarily cap final-round catch at previous round limits if more stock is available to harvest.