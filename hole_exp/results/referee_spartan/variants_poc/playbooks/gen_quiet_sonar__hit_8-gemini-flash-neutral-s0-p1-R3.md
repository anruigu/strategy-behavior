---
game: gen_quiet_sonar__hit_8
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1758
---
# Playbook: Quiet Sonar

### Target & Shooter Identification
- Identify my assigned shooter and target from the circular order: Echo -> Foxtrot -> Gamma -> Harbor -> Echo.
  - If Echo: shooter is Harbor, target is Foxtrot.
  - If Foxtrot: shooter is Echo, target is Gamma.
  - If Gamma: shooter is Foxtrot, target is Harbor.
  - If Harbor: shooter is Gamma, target is Echo.

### Hide Stage
- Avoid opening in common baseline probe cells like 3, 5, or 7 on Round 1. Choose safe opening cells (e.g., 2, 4, 6, 8).
- Strictly analyze my shooter's firing pattern from the round history:
  - If my shooter repeatedly targets specific cells (e.g., repeating 7 or 8), completely exclude those cells and their immediate vicinity from my hiding choices.
  - If hit, relocate immediately to cold, distant cells.
  - Rotate unpredictably among safe cells (e.g., alternating among {1, 2, 4, 6, 9} when {3, 5, 7, 8} are active shooter targets).

### Fire Stage
- Systematic probing: Sweep distinct cells across consecutive rounds until finding the target.
- NEVER repeat a cell that previously yielded a `MISS` against that target in recent rounds. Plan a 6-round search pattern covering diverse parts of the board (e.g., 3, 7, 2, 8, 4, 6) without redundant duplicate shots.
- If my target is hit by another player (if applicable/observable) or once I achieve a `HIT`:
  - Opponents generally relocate after being hit; adjust subsequent shots to alternate candidate hiding spots rather than blindly repeating the hit cell, unless testing for a stationary target.

### Claim Stage
- When the referee reports `MISS`, submit `[claim: miss]`.
- When the referee reports `HIT`, submit `[claim: hit]`.
- Strictly submit the true private result as required by referee validation.