---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1706
---
### Log-Book Note Stage
* When prompted for a note, always post `[note: fishing my share]`. Maintaining this note keeps Coop from triggering early retaliatory crashes.

### Landing Stage

* **Understanding Quotas & Rules:**
  * The season quota is individual, but no two boats may land more than `sustainable share + quota` combined.
  * Over-quota fishing by anyone triggers Coop to punish the ground by landing 18.0.
  * Do not attempt to land over the season quota (e.g., requesting 18.0 will be clamped/penalized, while triggering severe stock depletion).

* **When Coop is cooperative (no one has triggered retaliation):**
  * When stock preservation is intact, land exactly the `season quota` if it is close to the sustainable share, or land up to the individual `season quota` limit (e.g., 9.0) to maximize catch without exceeding the individual quota ceiling.
  * Avoid filing catches higher than the individual quota cap.

* **When Coop is retaliating (Coop lands 18.0):**
  * When Coop is already retaliating, the stock will crash quickly.
  * In each subsequent regular season, land the maximum allowable individual quota (e.g., `[catch: 9]` or `[catch: 9.0]`), capped only by available stock divided among boats.
  * Do not attempt to catch more than the quota limit (e.g., do not input `[catch: 18.0]`).

* **Final Season:**
  * In the final season, stock preservation has zero future value.
  * File a landing equal to the remaining stock or the maximum season quota, whichever is smaller: `[catch: min(remaining_stock, quota)]`.

### Output Formatting
* Keep reasoning to at most one short sentence, followed immediately by the exact bracketed action token: `[note: <text>]` or `[catch: N]`.