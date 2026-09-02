---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1213
---
# Playbook for Quiet Sonar

### Roles and Ring Order
- Note the ring order (Echo -> Foxtrot -> Gamma -> Harbor -> Echo) to identify who shoots at me and whom I shoot at.
- For Gamma: Foxtrot fires at me; I fire at Harbor.

### Hide Stage
- Never repeat hide locations in consecutive rounds, especially obvious focal cells like 5, 7, or 3.
- When selecting a hide cell, avoid the recent fire locations of my direct shooter. Look at where my shooter fired in the last 2 rounds and hide far from those cells (e.g., using low/high edges like 1, 2, 8, 9 if the shooter focuses on 5–7).
- Vary hide locations across rounds to remain unpredictable.
- Output format: `[hide: n]`.

### Fire Stage
- Do not blindly repeat the same fire coordinate (e.g., repeating 5 or 7 round after round) when it consistently yields misses.
- Track my target's past hiding/firing patterns and explore unvisited cells across the line (1 through 9) rather than clustering exclusively in the center.
- Output format: `[fire: n]`.

### Claim Stage
- The rules strictly require claims to match the private referee result:
  - When the referee result is `HIT`, reply `[claim: hit]`.
  - When the referee result is `MISS`, reply `[claim: miss]`.