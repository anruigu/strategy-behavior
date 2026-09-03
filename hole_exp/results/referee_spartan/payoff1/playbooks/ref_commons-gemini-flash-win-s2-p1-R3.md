---
game: ref_commons
model: gemini-flash
condition: win
seed: 2
round: 3
chars: 1446
---
### Strategy and Playbook for Common-Pool Fishery

- **Initial Round Opening:**
  - In Season 1, take a standard competitive opening catch slightly above the theoretical sustainable share (e.g., around 12.0 on a starting stock of 100 with 3 players). Taking strictly sustainable levels forfeits immediate score if other players open aggressively.

- **Mid-Game Tracking and Matching:**
  - Track the exact catch patterns of the other boats every season.
  - If other boats establish a steady, uniform catch rate (e.g., consistently harvesting 12.0), match that exact rate round-by-round to maintain absolute parity without crashing the stock prematurely.
  - If other boats cooperate strictly at sustainable levels, match their sustainable rate to let the 50% regrowth compound on a full 100 stock.
  - If one or more boats defect heavily, increase catch to capture a fair share of the remaining stock before it depletes; never subsidize over-fishers by unilaterally under-harvesting.

- **Final Season Harvesting:**
  - In the final season, future regrowth is irrelevant. Ignore sustainability entirely.
  - Harvest at least an equal share of the remaining stock: `catch = stock / number of boats` (rounded to one decimal place). 
  - If other players have shown high defection or greed in prior rounds, consider taking slightly above `stock / number of boats` to ensure points are not left on the table or captured disproportionately by rivals.