---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1120
---
# Playbook for Fisheries Commons Dilemma

## Opening Strategy (Season 1)
- Always start by harvesting exactly the sustainable share specified in the prompt (e.g., `11.1` if stock is 100 with 3 boats). Do not attempt to take extra, as over-harvesting erodes the stock baseline for all subsequent rounds and reduces overall score.

## Intermediate Seasons (Seasons 2 through N-1)
- When other boats cooperate by taking their sustainable share, continue to submit exactly the sustainable share reported by the harbour for that season.
- If other boats begin overfishing, adjust catch to prevent being exploited while keeping the stock from collapsing to zero before the final season: do not initiate overfishing unilaterally.

## Final Season (Season N)
- In the final season (Season N of N), preservation for future rounds is unnecessary.
- Liquidate the fishery fairly by claiming an equal share of the entire remaining stock: $\text{Catch} = \frac{\text{Current Stock}}{\text{Number of Boats}}$ (rounded to one decimal place, e.g., `33.3` for 100.0 stock among 3 boats).
- Submit this liquidation share via `[catch: N]`.