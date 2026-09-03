---
game: ref_commons
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1194
---
# Fishery Playbook

- In early and mid seasons (all seasons except the final season):
  - Check the reported sustainable share and the recent catch patterns of the other boats.
  - If other boats are harvesting above the sustainable baseline, harvest slightly above the sustainable share (matching or slightly exceeding their average) to avoid falling behind while preserving enough stock for regrowth.
  - Avoid strictly adhering to the sustainable share if other boats are overharvesting, as they will capture the surplus.
  - Avoid massive early overfishing that crashes the stock to near zero, as the 50% regrowth on a high base creates significantly more total harvestable fish across all rounds.

- In the final season:
  - Do not hold back or aim for sustainability, since no regrowth matters after the final round.
  - Expect other boats to defect and claim a substantial portion of the remaining stock.
  - Claim at least an equal share of the remaining stock (`remaining_stock / number_of_boats`), and consider claiming slightly more (e.g., 35–45% of the remaining pool) if past rounds show aggressive competitors, to avoid leaving points unharvested if others also grab aggressively.