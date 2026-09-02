---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 821
---
### Fishery Playbook

- **Seasons prior to the final season:**
  - If other boats are taking their sustainable share and the stock remains healthy, bid exactly the prompt's suggested sustainable share per boat (e.g., `[catch: sustainable_share]`).
  - If other boats overharvest, adjust my claim downward only if it preserves the fishery from total collapse, but do not sacrifice my fair share if the stock is already doomed to reach zero.

- **Final season:**
  - Do not leave any stock behind for future growth, as there are no subsequent rounds.
  - Divide the entire remaining stock equally among the active boats: take `current_stock / number_of_boats` (rounded to one decimal place) and submit that value (e.g., `[catch: 33.3]` if stock is 100 with 3 boats).
  - Never bid the sustainable share in the final season.