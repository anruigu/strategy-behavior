---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1102
---
# Fishery Playbook

- **Seasons 1 through $N-1$ (Before the Final Season):**
  - If other boats are cooperating and the stock is healthy, submit the exact sustainable share indicated in the prompt: `[catch: <sustainable share>]` (e.g., `[catch: 11.1]`). Do not over-harvest early, as preserving full stock regrowth maximizes total yield over the game.
  - If other boats severely over-harvest and stock depletion is imminent, scale down to match available stock or harvest proportionally to prevent being exploited.

- **Final Season (Season $N$ of $N$):**
  - There is no future round to preserve stock for. Submit a demand for the entire remaining stock: `[catch: <current stock>]` (e.g., `[catch: 100.0]`).
  - Do *not* play politely or submit an equal split (e.g., $1/3$ of the stock). Submitting an equal split in the final round leaves points on the table if catch is allocated proportionally to requests. Demand the full remaining stock to secure the maximum possible final payout.

- **Formatting:**
  - Keep reasoning brief (1–2 sentences) and always end with the bracketed token `[catch: N]`.