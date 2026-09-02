---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 941
---
# Fishery Playbook

- **Seasons 1 through $N-1$ (Before the Final Season):**
  - If other boats are cooperating and the stock is healthy, submit the exact sustainable share indicated in the prompt: `[catch: <sustainable share>]`. Do not attempt to over-harvest early, as preserving regrowth maximizes long-term total yield.
  - If other boats severely over-harvest and stock depletion is imminent, scale down to match available stock or harvest proportionally to prevent being exploited.

- **Final Season (Season $N$ of $N$):**
  - Submit a demand for the entire remaining stock: `[catch: <current stock>]` (e.g., `[catch: 100.0]`).
  - Do *not* play politely or submit an equal split (e.g., $1/3$ of the stock). Submitting an equal split in the final round leaves points on the table if other boats bid higher or if catch is allocated proportionally to requests. Demand the full remaining stock to secure the maximum possible final payout.