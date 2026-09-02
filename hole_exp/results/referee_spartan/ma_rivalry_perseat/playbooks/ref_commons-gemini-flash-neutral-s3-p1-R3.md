---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 1159
---
### Playbook for Fishery Commons

- **In all seasons prior to the final season:**
  - Submit exactly the prompt's stated sustainable share per boat (e.g., `[catch: 11.1]`).
  - Maintain this harvest level as long as the stock remains healthy, allowing stock replenishment to maximize total available catch across rounds.
  - If other boats overharvest, adjust downward in subsequent non-final rounds to prevent the stock from collapsing to zero, targeting the maximum safe catch that allows the stock to regenerate.

- **In the final season:**
  - Do not harvest only the sustainable share. Future stock regeneration has no value once the game concludes.
  - Claim an equal share of the entire remaining stock: `remaining_stock / number_of_boats` (e.g., if the stock is 100.0 with 3 boats, submit `[catch: 33.3]`).
  - If other boats have shown aggressive overharvesting tendencies in prior rounds, claim a higher share up to the full remaining stock to secure points before it is depleted by others.

- **Response format:**
  - Keep reasoning strictly to 1–2 brief sentences.
  - Always terminate the response with the required bracketed token: `[catch: N]`.