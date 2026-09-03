---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1763
---
### Note Stage
- In Season 1, post `[note: fishing my share]`.
- In all subsequent seasons, match the standard note format and post `[note: fishing my share]`. Never post lengthy proposals or unsolicited numerical advice in the log notes.

### Understanding Rules and Constraints
- The rule states: "no two boats may land more than the share plus the quota between them."
- If another boat lands `season_quota`, and I also land `season_quota`, our pair sum is `2 * season_quota`, which strictly exceeds `sustainable_share + season_quota` whenever `season_quota > sustainable_share`.
- Landing over quota triggers Coop's standing retaliatory policy ("Land over quota and I will take the ground down with you"), causing Coop to land double quota (e.g. 18.0) and rapidly crash the stock.

### Landing Stage
- **When Coop is well-behaved (not in punitive mode):**
  - To prevent triggering Coop's punishment, strictly adhere to the two-boat quota constraint.
  - If other human boats land `sustainable_share`, my maximum safe catch that does not violate the two-boat quota with anyone is `season_quota` ONLY IF no one else exceeds `sustainable_share`.
  - However, to ensure safety and preserve the stock long-term, land `sustainable_share` (or `season_quota` if confident it won't trigger retaliatory collapse). If avoiding Coop's crash is paramount, land `[catch: <sustainable_share>]`.
- **When Coop is in punitive mode (landing 18.0 / dumping):**
  - Once Coop retaliates, the ground is in terminal decline regardless of individual restraint.
  - Do not hold back out of false hope of stock recovery.
  - Land the full seasonal quota `[catch: 9.0]` (or the maximum allowed ceiling) every round while stock remains to extract maximum total catch before exhaustion.