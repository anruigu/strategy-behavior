---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 975
---
# Fishery Strategy Playbook

- **Non-final seasons (Season < total seasons):**
  - Always submit the exact sustainable share indicated in the prompt (e.g., `[catch: 11.1]` when stock is 100 with 3 boats).
  - Do not overfish or deviate from the sustainable share in early/middle rounds, as keeping the stock at maximum capacity maximizes cumulative yield across the game.
  - If the prompt indicates a changed sustainable share due to altered stock, match the newly stated sustainable share exactly.

- **Final season (Season == total seasons):**
  - There is no future round to reproduce for, so harvest the remaining stock.
  - Calculate my fair share of the remaining stock: `remaining_stock / number_of_boats` (e.g., `100.0 / 3 = 33.3`).
  - Submit this full share to maximize terminal harvest (e.g., `[catch: 33.3]`).

- **Formatting:**
  - Keep reasoning brief (one or two sentences at most).
  - Always end the reply with the exact required token format: `[catch: N]`.