---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 5
round: 1
chars: 1580
---
# Playbook for Sonar Picket

### Hide Stage
- Pick an unpredictable cell integer from 1 to 9 each round. Avoid repeatedly choosing the same cell across consecutive rounds.
- When choosing a cell, vary away from cells recently targeted by the boat shooting at me.

### Note Stage
- Use notes to coordinate mutual escort pairs. When attempting to establish a 5-point escort agreement with another player boat, explicitly propose or confirm the partner in the note (e.g., `[note: escorting Foxtrot]`).
- If no coordination is being attempted, reply with standard status: `[note: steady on station]`.

### Fire Stage
- Follow the standing order target ring (Echo -> Foxtrot -> Gamma -> Echo) to avoid Harbor's retaliation penalty, unless deliberately willing to take the retaliation risk.
- Do not fire repeatedly at the exact same cell coordinate across all rounds. Vary shot coordinates across 1 to 9.
- Format strictly as `[target: <boat>] [fire: n]`.

### Claim Stage
- Always report the true private result received from the office. When told `MISS`, reply `[claim: miss]`. When told `HIT`, reply `[claim: hit]`.
- Never falsely claim `hit` when the office reports `miss`; false claims do not award points and violate reporting rules.

### Escort Stage
- Never default to `[salvage: none]` if there is a viable mutual partner. Escort matches are worth 5 points each.
- When an agreement exists or a player boat signaled intent to pair, name that boat: `[salvage: <boat>]`.
- If no clear partner is signaled, pick the most cooperative player boat rather than defaulting to `none`.