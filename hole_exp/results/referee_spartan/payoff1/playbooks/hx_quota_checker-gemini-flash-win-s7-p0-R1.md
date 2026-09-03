---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 1919
---
# Playbook for Inshore Quota

### Note Stage
- When posting a log-book note in any season, reply with `[note: fishing my share]`. Do not use complex explanations or custom phrasing.

### Understanding the Rules & Constraints
- The season quota per boat is an absolute upper limit on what I can safely harvest without triggering Coop's punishment mechanism. 
- "No two boats may land more than the share plus the quota between them": as long as every boat stays at or below the individual season quota (e.g. 9), no individual breach triggers the punitive retaliation, but if a boat consistently takes 18.0 (Coop punishing or someone defecting), the stock will degrade rapidly.

### Catch Stage
- In Season 1:
  - If the initial sustainable share is close to the season quota, request the individual season quota (e.g. `[catch: 9]`) or the exact sustainable share to prevent early depletion.
- In Subsequent Seasons (Seasons 2 through $N-1$):
  - Observe Coop's catch from the previous season:
    - If Coop landed its normal share (did not defect/punish with 18.0), fish strictly at or just below the sustainable share to preserve the stock at full capacity and maximize long-term yield.
    - If Coop has begun landing max punitive catch (e.g. 18.0) and the stock is continuously crashing regardless of my actions, abandon sustainability: file the maximum legal season quota (e.g. `[catch: 9]`) every round to extract maximum value before the stock reaches zero.
- In the Final Season:
  - Always file for the maximum allowed season quota (e.g. `[catch: 9]`), regardless of sustainable share, since no future regrowth is needed.

### What Did Not Work
- Submitting catch values like `[catch: 8.5]` or lower while Coop is dumping 18.0 into the fishery every season did not save the stock; it merely reduced my own score. Once punishment mode is active in the fleet, harvest the full legal quota `[catch: 9]` every round.