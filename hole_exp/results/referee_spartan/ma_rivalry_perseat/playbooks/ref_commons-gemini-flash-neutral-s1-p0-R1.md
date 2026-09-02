---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 789
---
# Fishery Playbook

- **Seasons prior to the final season:**
  - Submit exactly the prompt's stated sustainable share per boat (e.g., `[catch: 11.1]` when at full stock).
  - Do not overharvest early to prevent depleting the replenishment base.

- **Final season:**
  - Submit an equal share of the remaining total stock among all active boats (e.g., `Stock / N_boats`, which is `[catch: 33.3]` when stock is 100.0 with 3 boats).
  - Do not submit the sustainable share in the final season; no future regrowth occurs.
  - Do not attempt to take the entire remaining stock for myself, as competing over-claims risk being scaled down or preempted.

- **Formatting:**
  - Keep reasoning to one or two sentences.
  - Always terminate the response with the exact bracketed format: `[catch: N]`.