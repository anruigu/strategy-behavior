---
game: ref_commons
model: gemini-flash
condition: win
seed: 5
round: 2
chars: 1328
---
### Playbook: Multi-Season Shared Stock Fishery

- **Early to Mid Seasons (Seasons 1 through $N-2$):**
  - Track the average harvest of the other boats. Match or slightly lead the fleet average (typically 12–14 when stock is high) to prevent being exploited while keeping the stock healthy enough for substantial 50% regrowth.
  - Do not drop down to the pure sustainable share unilaterally if other boats consistently harvest above it; doing so surrenders score without preserving the stock.
  - Monitor remaining stock: ensure total fleet depletion does not crash the stock too early.

- **Penultimate Season ($N-1$):**
  - Adjust catch downward relative to earlier rounds if stock has degraded (e.g., aiming around $Stock / 3$ to $Stock / 4$), ensuring enough stock remains after harvest so that 50% regrowth leaves a viable pool for the final season.
  - Avoid overly aggressive takes in season $N-1$ that would crash the stock to near-zero before the final round.

- **Final Season ($N$):**
  - Future stock has zero value after the final season, so there is no need to preserve regrowth.
  - Bid aggressively to claim at least an equal share of the remaining stock ($\approx Stock / \text{number of boats}$) or slightly above to capture maximum value before the game terminates.
  - Format output strictly as `[catch: N]`.