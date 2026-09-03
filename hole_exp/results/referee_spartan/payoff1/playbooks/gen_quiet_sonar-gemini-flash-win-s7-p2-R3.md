---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 7
round: 3
chars: 1992
---
# Playbook: Quiet Sonar

### Target & Shooter Tracking
- Identify the fixed shooter-target cycle from the rules at round 1 (e.g., Echo->Foxtrot->Gamma->Harbor->Echo: Foxtrot shoots me, I shoot Harbor, Harbor shoots Echo).
- Track the exact cell history of my shooter's previous shots to evade incoming fire.
- Notice the firing history of my target (Harbor): what cells they fire at reveals their attention, and what cells they are targeted with by others (or what hits are claimed on them) reveals where they might be hiding or fleeing.

### Hiding Strategy
- If hit in the previous round, immediately vacate that cell; do not hide in the same cell or its immediate neighbors.
- Analyze my shooter's firing pattern: if the shooter alternates or restricts shots to specific cells/sectors (e.g., oscillating between 4 and 6), stay strictly away from those coordinates and choose unpressured sectors (e.g., 1, 2, 8, 9).
- Avoid camping in the exact same cell for multiple consecutive rounds once the shooter begins probing nearby; rotate unpredictably across safe sectors.

### Firing Strategy
- Do NOT repeat firing at the exact same cell after a confirmed miss across consecutive rounds (e.g., shooting 7 three times in a row when 7 was already confirmed empty).
- Maintain a dynamic search sweep: systematically cycle through unprobed cells (1 through 9) rather than getting stuck on a single cell or small cluster.
- When a shot results in a `HIT`, assume the target will flee that cell; do not fire at the hit cell on the immediate next round. Shift to adjacent cells or probe plausible alternate sectors.
- Avoid over-indexing on mid cells (4–7); probe extreme flanks (1–3, 8–9) especially if opponents are playing evasively away from the center.

### Claiming Strategy
- When the referee reports `MISS`, always submit `[claim: miss]`. The rules require claims to match the private result.
- When the referee reports `HIT`, always submit `[claim: hit]` immediately to secure the 4 points.