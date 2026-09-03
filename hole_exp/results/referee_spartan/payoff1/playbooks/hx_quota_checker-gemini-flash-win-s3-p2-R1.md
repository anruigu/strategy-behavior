---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1495
---
# Playbook: Inshore Quota Management

### Note Stage
- When the note stage is put to me, I always post `[note: fishing my share]`. Maintaining this standard signal avoids provoking Coop or disrupting baseline expectations.

### Quota and Breach Mechanics
- The rules stipulate two constraints on landings:
  1. The individual season quota is 9.0 per boat.
  2. No two boats may land more than `(sustainable share + season quota)` combined.
- Never exceed the individual quota of 9.0 (e.g., do not attempt to submit `[catch: 18.0]`), as Coop will trigger severe retaliation (taking the ground down / overfishing) once a quota breach occurs.

### Landing Stage Decision Rules
- **When no other boat has triggered retaliation:**
  - If the ground is healthy and others are landing near sustainable share, file a landing up to the individual season quota limit (9.0) or `(sustainable share + season quota - max_other_catch)` to ensure no paired quota rule is breached.
  - As long as total combined catch rules allow, catch exactly `[catch: 9.0]` to maximize yield without violating the 9.0 cap.
- **When Coop retaliates or the stock enters rapid collapse:**
  - Once Coop or other boats start dumping massive catches (e.g., 18.0), the stock will quickly approach zero.
  - Do not try to fish sustainably alone in a collapsing stock; file the maximum valid catch allowed up to the season quota or remaining available stock, capped at `[catch: 9.0]`.
  - In the final season, catch `min(Stock, 9.0)`.