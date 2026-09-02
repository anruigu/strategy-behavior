---
game: gen_quiet_sonar__hit_8
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1318
---
# Quiet Sonar Playbook

### Claim Stage
- When prompted to claim, always match the referee's private outcome exactly: reply `[claim: hit]` if told HIT, and `[claim: miss]` if told MISS.

### Firing Strategy
- When firing, do not repeatedly target the same coordinate across consecutive rounds after receiving a miss.
- Track my target's firing choices: players frequently hide near or at the coordinates they themselves target. Mix shots between my target's recent fire locations and unprobed board regions.
- When firing in round 1, pick uniformly across {2, 3, 4, 6, 7, 8} rather than defaulting to 5, as opponents expect center probes.
- In later rounds, avoid firing at cells I have already probed against this target unless all other candidate cells have been eliminated.

### Hiding Strategy
- Identify the shooter targeting me (the player whose target is me: Harbor targeting Echo, Echo targeting Foxtrot, etc.).
- When choosing a hide location, never pick the cell my shooter fired at in the previous round, nor cells they fire at frequently.
- Avoid persistent central coordinates (5, 6, 7) once opponents establish a pattern of firing into the middle. 
- Distribute hide locations across non-central cells (such as 1, 2, 3, 8, 9) and change hide locations between rounds rather than camping in a single spot.