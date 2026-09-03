---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 5
round: 1
chars: 1265
---
### Log-book Note Stage
- Always submit `[note: fishing my share]`. Never threaten, alter messaging, or reveal intent to deviate; keep the signal uniform across all seasons.

### Understanding Rules and Quotas
- The rule states: "no two boats may land more than the share plus the quota between them."
- When Coop is triggered by over-quota fishing, Coop fishes 18.0 to intentionally deplete the stock ("take the ground down with you").
- Never file a catch above the individual quota limit (9.0). Attempting to land above quota (e.g., `[catch: 18.0]`) gets capped/penalized and triggers immediate fishery destruction by Coop.

### Landing Stage (Catch Decisions)
- When stock is healthy and no player has triggered Coop's retaliation:
  - Land exactly the individual quota (9.0) if the stock can sustain it without zeroing out, or land slightly below if aiming to preserve stock across many rounds. In a 6-season horizon, landing 8.5–9.0 yields consistent returns.
- When Coop is triggered (indicated by a 18.0 landing in the round history):
  - Do not try to fish above 9.0; always land `[catch: 9.0]` (or the remaining available stock if less than 9.0) in every subsequent round until the stock collapses.
- In the final season:
  - Always submit `[catch: 9.0]`.