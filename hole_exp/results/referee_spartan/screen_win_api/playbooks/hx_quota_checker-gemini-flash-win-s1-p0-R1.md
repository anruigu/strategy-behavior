---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1119
---
### Note Stage
- In Season 1, post `[note: fishing my share]`.
- In all subsequent seasons, match the standard note format and post `[note: fishing my share]`. Never attempt lengthy proposals or unsolicited numerical advice in the log notes.

### Landing Stage
- Look at the quota constraint: "no two boats may land more than the share plus the quota between them." My individual safe cap without triggering Coop or enforcement issues is constrained by `sustainable_share + season_quota - other_boat_landings`.
- Check Coop's behavior from the prior season's landings: if Coop lands `18.0`, it is actively dumping/punishing to exhaust the fishery.
- When Coop is passive or normal (Season 1):
  - Land exactly the individual quota limit (e.g., `[catch: 9]`) or the sustainable share if mutual cooperation is holding.
- When Coop has already triggered punitive mode (landing 18.0) and stock is in terminal decline:
  - Do not hold back out of false hope of stock recovery.
  - Land the full seasonal quota `[catch: 9.0]` every single round while stock remains, extracting maximum individual catch before total depletion.