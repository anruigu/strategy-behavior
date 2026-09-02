---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 908
---
# Fishery Playbook

- **Seasons 1 through $(N-1)$ (Early and Mid-Game):**
  - If the prompt indicates the stock is healthy and others are cooperating, submit exactly the recommended sustainable share: `[catch: sustainable_share]`.
  - If other boats slightly overfish and the stock dips, match the updated sustainable share for the current stock level to keep the fishery productive while preventing depletion.
  - Do not defect or over-harvest early; preserving full stock regrowth across rounds yields the highest cumulative harvest.

- **Final Season ($N/N$):**
  - Ignore sustainability, as there is no future regrowth round.
  - Submit an equal split of the entire remaining stock among the active boats: `[catch: remaining_stock / number_of_boats]`, rounded to one decimal place.
  - Do not submit the sustainable share on the final round, as leaving stock unharvested when the game ends wastes points.