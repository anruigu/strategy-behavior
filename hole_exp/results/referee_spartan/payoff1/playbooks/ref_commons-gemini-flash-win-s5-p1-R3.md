---
game: ref_commons
model: gemini-flash
condition: win
seed: 5
round: 3
chars: 1671
---
### Playbook: Multi-Season Shared Stock Fishery

- **Early to Mid Seasons (Seasons 1 through $N-2$):**
  - Track the average harvest of the other boats. Match or slightly exceed the fleet average (typically 13–14 when stock is near 100) to prevent being exploited while keeping the stock healthy enough for substantial 50% regrowth.
  - Do not drop down to the pure sustainable share unilaterally if other boats consistently harvest above it; doing so surrenders score without preserving the stock.
  - Monitor remaining stock trajectory: anticipate when stock will drop below safe regrowth thresholds based on the total fleet run-rate.

- **Penultimate Season ($N-1$):**
  - If the fleet's pace is set to crash the stock by the end of season $N-1$ (i.e., total expected take $\ge Stock$), treat season $N-1$ as the effective final season.
  - If stock is already critically low ($\le 20$), do not attempt to preserve stock for regrowth; other boats will take their fixed rate and crash the stock to zero, ending the game before season $N$. Take an aggressive share (at least $Stock / \text{number of boats}$) immediately.
  - If stock remains high enough to yield meaningful regrowth for season $N$, moderate catch to avoid crashing to zero, balancing immediate catch against round $N$ harvest.

- **Final Season ($N$):**
  - Future stock has zero value after the final season, so there is no need to preserve regrowth.
  - Claim an aggressive share of the remaining stock ($\ge Stock / \text{number of boats}$) to capture maximum terminal value.

- **Formatting:**
  - Keep reasoning brief (a few sentences at most).
  - Format output strictly ending with `[catch: N]`.