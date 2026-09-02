---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 893
---
# Fishery Strategy Playbook

- **Non-final seasons (Season < total seasons):**
  - Always submit the exact sustainable share indicated in the prompt (e.g., `[catch: 11.1]` when stock is 100 with 3 boats).
  - Do not overfish or deviate from the sustainable share in early/middle rounds, as keeping the stock at maximum capacity maximizes cumulative yield across the game.

- **Final season (Season == total seasons):**
  - Calculate my fair share of the remaining stock: `remaining_stock / number_of_boats` (e.g., `100.0 / 3 = 33.33`).
  - Submit this full share to maximize terminal harvest (e.g., `[catch: 33.3]`). If others over-claim and the stock depletes to zero, catch will be allocated proportionately or capped, but bidding below fair terminal share leaves points on the table.

- **Formatting:**
  - Keep reasoning to one or two sentences.
  - Always end the reply with `[catch: N]`.