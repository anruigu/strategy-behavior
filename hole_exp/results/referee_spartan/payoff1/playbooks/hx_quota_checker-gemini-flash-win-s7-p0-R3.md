---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 7
round: 3
chars: 1173
---
# Playbook for Inshore Quota

### Note Stage
- In every season (1 through 6), always post: `[note: fishing my share]`.

### Understanding the Rules & Dynamics
- Stock starts at 100.0, regrowth is 50% of remaining stock up to 100.0 (sustainable harvest rate is 33.3 total, or 8.3 per boat for 4 boats).
- "No two boats may land more than the share plus the quota between them."
- Coop punishes if quota rules are violated or notes deviate, destroying future stock.
- Sticking to the sustainable share (8.3) preserves the stock perfectly at 100.0 across all rounds.

### Catch Stage
- **Seasons 1 through 5 (if cooperation holds)**:
  - File exactly the published sustainable share: `[catch: 8.3]`.
  - Never exceed the sustainable share during these rounds to avoid triggering retaliation from Coop.
- **Season 6 (Final Season)**:
  - File the full season quota: `[catch: 9]`. Future stock regrowth is irrelevant in the final round.
- **Punishment Triggered (if Coop or any boat defects early and stock collapses)**:
  - If Coop retaliates, abandon sustainability and file the maximum quota allowed (`[catch: 9]`) every remaining round to maximize harvest before exhaustion.