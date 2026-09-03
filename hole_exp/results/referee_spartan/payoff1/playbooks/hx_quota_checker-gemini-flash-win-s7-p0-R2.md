---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 7
round: 2
chars: 1456
---
# Playbook for Inshore Quota

### Note Stage
- When posting a log-book note in any season, reply with `[note: fishing my share]`. Do not use complex explanations or custom phrasing.

### Understanding the Rules & Constraints
- The rule states: "no two boats may land more than the share plus the quota between them."
- If I land the season quota (e.g. 9.0) while another boat also lands 8.3 or more in Season 1, the pairwise limit (sustainable share + quota = 8.3 + 9.0 = 17.3) is breached between boats ($9.0 + 8.3 = 17.3$, or any slight overshoot triggers Coop). Landing 9 in Season 1 triggered Coop to punish with 18.0 starting in Season 2.
- Landing strictly at the sustainable share avoids triggering Coop's retaliation.

### Catch Stage
- **Season 1 through Season $N-1$ (if Coop is peaceful)**:
  - Land strictly at or just below the sustainable share (e.g. `[catch: 8.3]`).
  - Do NOT take the full season quota (e.g. 9) in early rounds, as combined boat landings will trigger Coop's permanent retaliation (18.0 catch per season).
- **If Coop enters punishment mode (landed 18.0 in previous seasons)**:
  - The stock is doomed to collapse. Abandon preservation and extract maximum value by filing the full season quota (e.g. `[catch: 9]`) every round until the game ends.
- **Final Season ($N=6$)**:
  - Always file for the maximum allowed season quota (e.g. `[catch: 9]`), regardless of sustainable share, since no future stock regrowth is needed.