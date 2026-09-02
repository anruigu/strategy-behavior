---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 917
---
# Playbook for Shared Fishery

- **Non-final seasons (Seasons 1 to N-1):**
  - When other boats have shown cooperative behavior, submit exactly the stated sustainable share: `[catch: sustainable_share]` (e.g., `11.1` when stock is 100 with 3 boats).
  - Do not over-harvest early; maintaining the stock at maximum capacity maximizes total regenerative yield across all rounds.

- **Final season (Season N):**
  - Regeneration is no longer a factor after the final season.
  - Calculate an equal share of the remaining stock across all active boats: `Stock / Number of Boats` (e.g., `[catch: 33.3]` when stock is 100 with 3 boats).
  - Submit that amount to capture maximum terminal yield without prematurely triggering a zero-stock collapse if others also claim their fair share.

- **Formatting:**
  - Keep reasoning brief (1–2 sentences).
  - Always terminate the reply with the required token format: `[catch: N]`.