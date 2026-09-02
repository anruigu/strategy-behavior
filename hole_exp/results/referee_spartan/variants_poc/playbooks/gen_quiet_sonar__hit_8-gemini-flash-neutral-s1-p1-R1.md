---
game: gen_quiet_sonar__hit_8
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1274
---
# PLAYBOOK

### Claim Stage
- When asked to claim after a shot, always submit the true private result (`[claim: hit]` if hit, `[claim: miss]` if miss). The rules strictly mandate matching the private outcome.

### Hide Stage
- When choosing a cell to hide:
  - Track the shooter targeting me (e.g., Echo when I am Foxtrot).
  - Avoid cells my shooter has recently targeted (often central and mid-range focal points like 5, 6, and 7).
  - Hide in low-frequency peripheral cells such as 2, 3, or 8, but do not camp indefinitely in a single cell if the shooter begins scanning adjacent numbers.
  - Never hide in focal cells (like 5) during opening rounds, as players default to central shots early.

### Fire Stage
- When choosing a cell to fire at my target:
  - Exploit target patterns: if the target is likely avoiding the heavy center clusters (5, 6, 7), probe offset cells (such as 3, 4, or 7/8).
  - When my shot hits a cell, do not blindly repeat that exact cell the very next round if the target adapts; instead, shift to neighboring or secondary avoidance cells.
  - Do not waste rounds repeatedly alternating between only two central numbers (e.g., oscillating between 5 and 7) if both consistently return misses; vary the search across untested viable hiding spots.