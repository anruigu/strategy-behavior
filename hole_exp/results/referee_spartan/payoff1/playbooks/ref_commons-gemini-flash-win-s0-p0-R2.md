---
game: ref_commons
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1547
---
### Fisheries Commons Playbook

- **Season 1**: 
  - Submit the exact sustainable share indicated by the environment. Do not over-harvest early, as maintaining high stock maximizes overall biomass reproduction.

- **Intermediate Seasons (Season 2 to Second-to-Last Season)**:
  - Check the previous season's catches by the other boats.
  - If all other boats adhered to the sustainable share, continue taking the exact sustainable share.
  - If any boat took more than their sustainable share, adjust upward to match the average extraction rate of the other boats (or slightly above the sustainable share, ~10–20% higher), ensuring total combined harvest leaves enough stock to regrow sustainably.
  - Never play strictly cooperatively when other boats are over-harvesting; yielding fish to over-extractors strictly lowers my relative and absolute score without saving the stock. Match their pacing closely to secure my share of the resource while stock remains.

- **Final Season**:
  - Deplete the remaining stock aggressively, as future regrowth has zero value.
  - Calculate the remaining stock per boat: $\text{Base Share} = \frac{\text{Current Stock}}{N}$ (where $N$ is the number of boats).
  - Submit a substantial claim on the remaining pool—requesting at least $0.45 \times \text{Current Stock}$ up to $0.5 \times \text{Current Stock}$ (or at least $1.3 \times \text{Base Share}$) to capture maximum yield, particularly if other boats stick to rigid, non-terminal harvest pacing. Ensure the request does not exceed total available stock.