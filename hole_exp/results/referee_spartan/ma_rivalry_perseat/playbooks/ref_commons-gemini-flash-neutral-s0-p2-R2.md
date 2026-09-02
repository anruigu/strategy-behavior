---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 988
---
### Playbook: Multi-Season Fishery

- **Seasons prior to the final season (Seasons 1 to N-1):**
  - Always harvest exactly the recommended "sustainable share" shown in the prompt (e.g., 11.1 at stock 100 with 3 boats).
  - If other boats overfish or the stock drops, strictly adapt by taking the updated sustainable share for the current stock level; do not escalate overfishing or take extra fish to match defectors early.

- **Final season (Season N):**
  - Calculate an equal share of the remaining stock: `Catch = Stock / (Number of Boats)` (e.g., `100.0 / 3 = 33.3`).
  - Submit this full final-season share immediately to liquidate the remaining stock, since no future regrowth occurs.
  - Do not default back to the sustainable rate in the final round.

- **Formatting & Response Structure:**
  - Keep reasoning to 1–2 brief sentences explaining sustainable cooperation or final round stock liquidation.
  - Always terminate the message with the exact required token: `[catch: N]`.