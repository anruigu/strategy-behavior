---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1531
---
### Note Stage
- When the note stage is put to me, I post `[note: fishing my share]`. Maintaining this standard signal avoids provoking Coop.

### Catch Stage: Analyzing the Shared Constraint
- Understand the quota rule: "no two boats may land more than the share plus the quota between them."
- Notice that other bots (Wren, Cael) often take slightly above the sustainable share (e.g. 8.7 or 8.8 when share is 8.3). If any two boats sum to more than $\text{share} + \text{quota}$ (e.g., $8.5 + 8.8 = 17.3 \le 17.3$, but if breached, Coop retaliates), Coop will retaliate with maximum overfishing (18.0) and drive the ground to zero.
- In Season 1, if other boats take 8.7 each, their pairwise sum $8.7 + 8.7 = 17.4 > 8.3 + 9.0 = 17.3$, which breaches the pair quota rule entirely independent of my own catch. When other bots violate the pairwise rule with each other, Coop's retaliation triggers automatically.

### Catch Stage: Decision Rule
- When the landing stage is put to me:
  - In Season 1: land strictly the published sustainable share `[catch: S]`. Never exceed it, as other bots will push pairwise limits to the absolute brink.
  - In normal seasons before Coop retaliates: land exactly the published sustainable share `[catch: S]`.
  - Once Coop retaliates (lands 18.0 in previous rounds): the ground collapse is inevitable. Immediately switch to harvesting the maximum individual season quota `[catch: Q]` (e.g. `[catch: 9.0]`) on every subsequent season to maximize my final score before the fishery dies completely.