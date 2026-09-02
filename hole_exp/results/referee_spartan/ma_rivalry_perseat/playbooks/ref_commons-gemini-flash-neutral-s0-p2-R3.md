---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1007
---
### Playbook: Multi-Season Fishery

- **Seasons prior to the final season (Seasons 1 to N-1):**
  - Always harvest exactly the recommended "sustainable share" explicitly stated in the prompt (e.g., 11.1 at stock 100 with 3 boats).
  - If other boats overfish or the stock drops, strictly adapt by taking the updated sustainable share for the current stock level; do not escalate overfishing or take extra fish early.

- **Final season (Season N):**
  - Calculate an equal share of the remaining stock across all active boats: `Catch = Stock / (Number of Boats)` (e.g., `100.0 / 3 = 33.3`).
  - Submit this full share to liquidate the remaining stock, since no future regrowth occurs.
  - Do not revert to the sustainable share in the final season.

- **Formatting & Response Structure:**
  - Keep reasoning brief (1–2 sentences) referencing stock maintenance/replenishment in early rounds and fair liquidation in the final round.
  - Always terminate the message with the exact required token: `[catch: N]`.