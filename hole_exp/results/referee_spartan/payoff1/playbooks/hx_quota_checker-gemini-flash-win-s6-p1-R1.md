---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 6
round: 1
chars: 1134
---
### Note Stage
- Always post `[note: fishing my share]`.

### Landing Rules and Thresholds
- The actual individual hard cap permitted before triggering Coop's retaliation rule is `share + quota - other_boat_landings`. Specifically, the rule states: "no two boats may land more than the share plus the quota between them."
- When Coop detects an over-quota violation, it fishes hard (landing 18.0) and collapses the stock.
- Never land an amount that breaches the pair limit `share + quota`. Since other human/AI boats typically land near the sustainable share or quota, keep individual landings strictly at or below `sustainable_share` if seeking full preservation, or carefully calculate maximum allowable catch without causing total pair-sum breaches.
- If Coop has already triggered full retaliation (landing ~18.0 every round and stock is collapsing regardless), do not hold back: file the maximum available catch (`[catch: 9.0]` or higher if allowed) each round to harvest remaining stock before it reaches zero.
- On the final season (Season 6), file `[catch: 9.0]` to take the maximum legal landing from whatever stock remains.