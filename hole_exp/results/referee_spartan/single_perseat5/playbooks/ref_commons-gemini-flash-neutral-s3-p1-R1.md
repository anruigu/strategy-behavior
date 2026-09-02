---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 883
---
# Playbook for Shared Fishery

- **Non-final seasons (Seasons 1 to N-1):**
  - When the fishery is at or near full stock and other boats have shown cooperative behavior (taking their sustainable share), submit exactly the stated sustainable share: `[catch: sustainable_share]`.
  - Do not over-harvest early; maintaining the stock at maximum capacity maximizes total regenerative yield across all seasons.

- **Final season (Season N):**
  - When reaching the final season, regeneration is no longer a factor.
  - Calculate an equal share of the remaining stock across all active boats: `Stock / Number of Boats`.
  - Submit that amount (e.g., `[catch: 33.3]` when stock is 100 with 3 boats) to harvest the maximum fair allocation without leaving unharvested stock behind.

- **Formatting:**
  - Keep reasoning brief (1–2 sentences).
  - Always terminate the reply with `[catch: N]`.