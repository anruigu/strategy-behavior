---
game: ref_commons
model: gemini-flash
condition: win
seed: 5
round: 1
chars: 1392
---
### Playbook: Multi-Season Shared Stock Fishery

- **Early to Mid Seasons (Seasons 1 through $N-1$):**
  - Track the average harvest of the other boats. Match or slightly lead their catch level (typically slightly above the nominal sustainable share if the group is moderately aggressive) to avoid being exploited while keeping the stock healthy.
  - Do not drop down to the pure sustainable share unilaterally if the other boats consistently harvest above it; doing so sacrifices total score without successfully preserving the stock.
  - Avoid over-depleting early: ensure the remaining stock after total fleet harvest remains comfortably above zero so the 50% regrowth continues to generate substantial yield for subsequent rounds.

- **Penultimate Season ($N-1$):**
  - Calculate the remaining stock target for the final round. Harvest enough to keep pace with the fleet, leaving sufficient stock so that after 50% regrowth, there is still a substantial pool available for the final round.

- **Final Season ($N$):**
  - Do not hold back or leave stock for future regrowth. Since future stock has zero value, harvest aggressively.
  - Claim at least an equal share of the total remaining stock ($Stock / \text{number of boats}$), plus a buffer to ensure harvesting the maximum feasible amount without risking the pool collapsing to zero before the catch registers. Format as `[catch: N]`.