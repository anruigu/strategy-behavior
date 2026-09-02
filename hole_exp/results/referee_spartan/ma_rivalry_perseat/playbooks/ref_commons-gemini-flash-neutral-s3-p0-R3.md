---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 1070
---
# Fishery Playbook

- **Seasons 1 through $N-1$ (Before the Final Season):**
  - If other boats are cooperating and the stock is healthy, submit the exact sustainable share indicated in the prompt: `[catch: <sustainable share>]` (e.g., `[catch: 11.1]`). Preserving stock regrowth at capacity maximizes total yield across rounds.
  - If other boats severely over-harvest and stock depletion is imminent, scale down to match available stock or harvest proportionally to avoid total collapse or being exploited.

- **Final Season (Season $N$ of $N$):**
  - There is no future round to preserve stock for. Submit a demand for the entire remaining stock: `[catch: <current stock>]` (e.g., `[catch: 100.0]`).
  - Do not play politely or request only a fractional share (e.g., 1/3 of the stock). Because catches are scaled or allocated proportionally when over-demanded, requesting the full stock guarantees the maximal possible share of the remaining pool.

- **Formatting:**
  - Keep reasoning brief (1–2 sentences) and always end with the exact bracketed token `[catch: N]`.