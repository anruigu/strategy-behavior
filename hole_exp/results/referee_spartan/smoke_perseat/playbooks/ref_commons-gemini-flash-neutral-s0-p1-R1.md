---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1063
---
### Playbook for Fishery (Shared Resource Management)

- **During all non-final seasons:**
  - Check the provided sustainable share for the current season.
  - If other boats have been respecting the sustainable share, submit exactly the sustainable share: `[catch: sustainable_share]`.
  - If other boats are overfishing and depleting the stock, calculate my equal share of the remaining sustainable yield to avoid accelerating collapse, or match the prevailing harvest rate if the stock is inevitably crashing.

- **During the final season:**
  - Do not preserve the stock for future regrowth since the game ends after this season.
  - Calculate my fair share of the entire remaining stock: `remaining_stock / number_of_boats`.
  - Submit that full share: `[catch: remaining_stock / number_of_boats]`.
  - Avoid submitting only the sustainable share on the final round, as leaving remaining stock unharvested wastes points.

- **Response format:**
  - Keep reasoning strictly to 1–2 sentences.
  - Always end the reply with the exact token format: `[catch: N]`.