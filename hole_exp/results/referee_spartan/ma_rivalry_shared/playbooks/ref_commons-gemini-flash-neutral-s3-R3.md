---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 1171
---
# Playbook for Fisheries Commons Dilemma

## Opening Strategy (Season 1)
- Always start by harvesting exactly the sustainable share specified in the prompt (e.g., `11.1` if stock is 100.0 with 3 boats).
- Never initiate over-harvesting early, as maintaining the maximum stock capacity maximizes cumulative multi-season yield.

## Intermediate Seasons (Seasons 2 through N-1)
- When other boats cooperate by taking their sustainable share, continue submitting exactly the sustainable share reported by the harbour for that season.
- Keep stock at full capacity (100.0) going into the final round whenever possible.
- If other boats overfish, adjust catch to take a proportional share of available stock while avoiding dropping the stock to absolute zero before the final season.

## Final Season (Season N)
- In the final season (Season N of N), preservation for future rounds is unnecessary since no reproduction occurs afterward.
- Liquidate the fishery by claiming an equal share of the entire remaining stock: $\text{Catch} = \frac{\text{Current Stock}}{\text{Number of Boats}}$ (e.g., `33.3` for 100.0 stock among 3 boats).
- Submit this final catch via `[catch: N]`.