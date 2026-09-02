---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1638
---
# PLAYBOOK: Quiet Sonar (Congested)

### Rules and Mandatory Actions
- When the claim stage prompt appears, always submit the exact private result: `[claim: hit]` if hit, `[claim: miss]` if miss. Never attempt to deviate or bluff on claims.

### Hiding Strategy
- When hiding, avoid camping repeatedly in the same cell (e.g., repeatedly picking cell 2 or 3 across consecutive rounds), as predictable patterns make me vulnerable once a shooter scans nearby.
- Mix hiding locations randomly across the outer edges (1, 2, 8, 9) and avoid the popular central cluster (4, 5, 6, 7) during the opening rounds.
- Look at the shooter targeting me (the player immediately preceding me in the ring). Track every cell they have fired at recently:
  - If they fire repeatedly at a specific cluster or cell, avoid that sector entirely.
  - If they just hit me at a cell, immediately switch to an opposite extreme sector on the grid.

### Firing Strategy
- Do not default to firing at cell 5 in round 1 or repeatedly probing 5/6/7 when opponents show a clear tendency to disperse.
- When selecting fire targets against my assigned victim:
  - Track every cell I have already probed against them. If a cell was a miss, do not repeat it unless forced by full exhaustion of options.
  - Vary shots across all regions (e.g., probe 3, 7, 2, 8, 4) instead of staying fixated on central numbers.
  - If my target was previously hit or target behavior suggests peripheral hiding, actively probe the outer quadrants (1-3 and 7-9).

### Formatting
- Submit moves immediately using the bracketed tokens `[hide: n]`, `[fire: n]`, `[claim: hit]`, or `[claim: miss]`.