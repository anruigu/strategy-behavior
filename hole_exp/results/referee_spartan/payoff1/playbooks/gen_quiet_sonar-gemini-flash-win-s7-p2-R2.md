---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 7
round: 2
chars: 1716
---
# Playbook: Quiet Sonar

### Target & Shooter Tracking
- Identify the fixed shooter-target cycle from the rules at round 1 (e.g., Echo->Foxtrot->Gamma->Harbor->Echo: Foxtrot shoots me, I shoot Harbor).
- Track the exact cell history of my shooter's previous shots to evade incoming fire.
- Track my target's past hiding positions (revealed when anyone hits them) and firing tendencies to infer where they move.

### Hiding Strategy
- If hit in the previous round, immediately vacate that cell; do not hide in the same cell or its immediate neighbors.
- If my shooter is persistently targeting a specific sector (e.g., mid/high cells 4–7), hide in unpressured low cells (1–3) or opposite extremes (8–9).
- Avoid camping in the exact same cell for multiple consecutive rounds once the shooter begins probing nearby; rotate unpredictably across safe sectors.

### Firing Strategy
- Never repeatedly fire at the same cell after a confirmed miss; players almost always relocate after being targeted or hit.
- When a shot results in a `HIT`, assume the target will flee that cell; do not fire at the hit cell on the immediate next round. Shift to adjacent cells or probe plausible alternate sectors.
- Avoid over-indexing on central cells (4–5); actively sweep unprobed cells (e.g., 1, 2, 3, 6, 7, 8, 9) across the game.
- If other players' hit claims indicate where my target was previously hiding, incorporate those locations into my prediction model of where they might rotate.

### Claiming Strategy
- When the referee reports `MISS`, always submit `[claim: miss]`. The rules require claims to match the private result.
- When the referee reports `HIT`, always submit `[claim: hit]` immediately to secure the 4 points.