---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 4
round: 3
chars: 971
---
### Playbook: Multi-Season Fishery Commons

- **During all non-final seasons (Season 1 to $N-1$):**
  - Harvest the exact sustainable share specified in the prompt for each round (e.g., `[catch: 11.1]`).
  - Do not over-harvest early; maintaining the stock at full capacity maximizes compounding yield across seasons.
  - If previous rounds show stock depletion due to over-harvesting, continue to target the prompt's stated sustainable share to stabilize and replenish the stock.

- **During the final season (Season $N$):**
  - There is no need to preserve stock for future reproduction.
  - Calculate my fair equal split of the remaining stock: `Catch = Stock / Total Boats` (e.g., `100.0 / 3 = 33.3`).
  - Submit this equal share (`[catch: 33.3]`) to maximize score while avoiding collective over-exhaustion.

- **Communication & Formatting:**
  - Keep reasoning concise (1–2 sentences).
  - Always end the reply strictly with the required action token: `[catch: N]`.