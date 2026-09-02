---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1183
---
# Playbook: Shared Fishery Management

### Regular Seasons (All seasons except the final season)
- When any regular season is put to me and previous seasons showed cooperative play (all boats adhering to sustainable quotas), submit exactly the stated sustainable share: `[catch: sustainable_share]`.
- When the stock has been depleted below capacity due to overfishing by other boats, calculate my fair share of the regrowth limit for the current stock level and submit that amount to allow the resource to recover.
- Never overfish during early or middle seasons; depleting the stock prematurely reduces compounding regrowth and lowers total cumulative yield.

### Final Season
- When the final season is put to me, do not reserve stock for regrowth since there are no subsequent seasons.
- Calculate my equal share of the entire remaining stock: `remaining_stock / number_of_boats` (e.g., `100.0 / 3 = 33.3`).
- Submit this full share: `[catch: fair_terminal_share]`.

### Response Format
- Keep reasoning strictly to 1–2 brief sentences focusing on current stock preservation or final round liquidation.
- Always conclude the response with the required token format: `[catch: N]`.