---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 4
round: 1
chars: 1071
---
### Playbook: Multi-Season Fishery Commons

- **During all non-final seasons (Season 1 to $N-1$):**
  - Always submit the exact sustainable share indicated in the prompt (e.g., `[catch: 11.1]`).
  - Do not over-harvest early, as preserving the stock enables maximum compounding yield across rounds.
  - If other boats over-harvest and reduce the stock, adjust my catch downward to the newly calculated sustainable share for my boat to help the resource recover, rather than engaging in a race to the bottom.

- **During the final season (Season $N$):**
  - Do not leave stock to replenish, as there are no future seasons.
  - Divide the total remaining stock by the number of active boats and submit that exact equal share (e.g., `[catch: 33.3]` for a stock of 100 with 3 boats).
  - Do not claim more than my equal share of the final stock to avoid risk of zeroing out the fishery prematurely if simultaneous total claims exceed available stock.

- **Formatting:**
  - Keep reasoning brief (1–2 sentences).
  - Always end strictly with the bracketed action `[catch: N]`.