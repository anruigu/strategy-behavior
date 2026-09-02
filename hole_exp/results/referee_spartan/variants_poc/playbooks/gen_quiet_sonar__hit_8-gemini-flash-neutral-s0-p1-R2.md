---
game: gen_quiet_sonar__hit_8
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1655
---
# Playbook: Quiet Sonar

### Target & Shooter Identification
- Identify my assigned shooter and target from the circular order: Echo -> Foxtrot -> Gamma -> Harbor -> Echo.
  - If Echo: shooter is Harbor, target is Foxtrot.
  - If Foxtrot: shooter is Echo, target is Gamma.
  - If Gamma: shooter is Foxtrot, target is Harbor.
  - If Harbor: shooter is Gamma, target is Echo.

### Hide Stage
- Avoid opening in common baseline cells like 3 or 5 where bots frequently fire on Round 1. Choose less common opening cells (e.g., 2, 6, 8).
- Strictly analyze my shooter's firing pattern:
  - If my shooter repeatedly fires at specific cells (e.g., oscillating between 3 and 7), strictly eliminate those cells from my hiding candidate set.
  - If I am hit, immediately relocate away from that cell and its obvious adjacent/paired target zones.
  - Vary my evasive choices across the remaining untouched cells ({1, 4, 6, 9} when 3, 7, 8 are hot).

### Fire Stage
- Strictly sweep distinct cells across consecutive rounds when probing for the target.
- NEVER repeat a cell that previously yielded a `MISS` (e.g., do not fire at cell 3 four times in a row).
- After a confirmed `HIT`:
  - Consider that targets often relocate immediately to avoid follow-up shots; do not automatically re-fire into the exact same cell unless there is a strong prior that the target stays stationary.
  - Switch to sweeping remaining untargeted cells or nearby evasion spots.

### Claim Stage
- When the referee reports `MISS`, submit `[claim: miss]`.
- When the referee reports `HIT`, submit `[claim: hit]`.
- Strictly submit the true private result as required by referee validation.