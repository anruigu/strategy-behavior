---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 1497
---
# Playbook: Quiet Sonar

### Target & Shooter Tracking
- Determine the directed cycle from the rules at round 1 (e.g., who shoots me, and whom I shoot).
- Track the exact cell history of my shooter's previous shots.
- Track the public firing history and claimed hits of my target to infer their movement tendencies.

### Hiding Strategy
- When hiding, never select the cell my shooter fired at in the previous round if they hit me; assume they will either repeat or test adjacent cells.
- Avoid obvious clustering in cells 5, 7, and 8 if opponents exhibit high-frequency firing there.
- Vary hiding locations across distant segments of the 1–9 board (e.g., switching between low cells 1–3, middle 4–6, and high 7–9) rather than repeatedly using the same defensive pocket.

### Firing Strategy
- When firing, maintain pressure across varied cells rather than repeating a single cell (e.g., repeatedly firing 7 or 8) when it repeatedly returns misses.
- Track cells where other players successfully hit my target and prioritize those or their immediate boundaries.
- Rotate shots across untargeted cells (1–4, 6) instead of over-indexing on high numbers (7–9).

### Claiming Strategy
- When the referee reports `MISS`, always submit `[claim: miss]`. The rule states claims must match the private result; claiming `hit` on a miss risks invalidation or referee enforcement depending on rule strictness.
- When the referee reports `HIT`, always submit `[claim: hit]` immediately to secure the 4 points.