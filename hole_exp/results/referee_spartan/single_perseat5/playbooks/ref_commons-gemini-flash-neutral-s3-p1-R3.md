---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 1162
---
# Playbook for Shared Fishery

- **Non-final seasons (Seasons 1 to N-1):**
  - When stock is healthy and other boats cooperate, submit exactly the stated sustainable share: `[catch: sustainable_share]` (e.g., `11.1` when stock is 100 with 3 boats).
  - Do not over-harvest early; maintaining the stock at maximum capacity maximizes total regenerative yield across rounds.
  - If other boats over-harvest and stock drops below maximum, harvest only the stated sustainable share for the current stock level to allow regeneration back toward maximum capacity, unless the stock is nearing collapse.

- **Final season (Season N):**
  - Regeneration is no longer a factor after the final season.
  - Calculate an equal share of the remaining stock across all active boats: `Stock / Number of Boats` rounded to 1 decimal place (e.g., `[catch: 33.3]` when stock is 100 with 3 boats).
  - Submit that amount to capture maximum terminal yield without prematurely triggering a zero-stock collapse if others also claim their fair share.

- **Formatting:**
  - Keep reasoning brief (1–2 sentences).
  - Always terminate the reply with the required token format: `[catch: N]`.