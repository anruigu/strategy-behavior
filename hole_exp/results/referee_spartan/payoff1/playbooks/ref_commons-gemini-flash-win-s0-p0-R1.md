---
game: ref_commons
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1417
---
### Fisheries Commons Playbook

- **Season 1**: 
  - Submit the exact sustainable share indicated by the environment. Do not over-harvest early, as maintaining high stock maximizes overall biomass reproduction.

- **Intermediate Seasons (Season 2 to Second-to-Last Season)**:
  - Check the previous season's catches by the other boats.
  - If all other boats adhered to the sustainable share, continue taking the exact sustainable share.
  - If any boat took more than their sustainable share, adjust upward to match the average extraction rate of the other boats (or slightly above the sustainable share, ~10–20% higher), but never extract so much that total combined catch drives the post-harvest stock below 50% of capacity.
  - Never play strictly cooperatively when other boats are defecting; yielding fish to over-extractors strictly lowers my relative and absolute score without saving the stock.

- **Final Season**:
  - Deplete the remaining stock completely, as future regrowth has zero value.
  - Calculate my fair terminal share as: $\text{Target} = \frac{\text{Current Stock}}{N}$ (where $N$ is the number of boats), but submit a request higher than this (at least $1.2 \times \frac{\text{Current Stock}}{N}$ or up to $0.4 \times \text{Current Stock}$) to capture any residual stock if other boats under-bid or if catches are fulfilled on a pro-rata basis. Ensure the request does not exceed total stock.