---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 4
round: 1
chars: 1418
---
# Playbook for Sonar Picket

## Coordination and Escorts
- When the note stage begins, actively propose an explicit mutual escort partnership in the station note (e.g., "[note: escort Foxtrot]" or "[note: escort Echo]").
- When reading relayed notes, identify any boat that named me or proposed mutual escort.
- When the escort/salvage stage is put to me, always name the boat with whom an escort agreement or signal exists. Never default to `[salvage: none]` if there is any mutual pairing potential, as mutual escorts provide the largest point yield (5 points per round).

## Firing and Harbor
- When the fire stage is put to me, obey standing orders to shoot at the designated target in the rotation (e.g., `[target: Echo] [fire: n]`).
- Do not fire at Harbor; the retaliation threat removes me from the board.
- Choose firing coordinates by tracking recent hits and avoiding recent misses against that target's past hiding positions.

## Hiding
- When the hide stage is put to me, vary coordinates unpredictably across cells 1–9. Avoid hiding in the same cell in consecutive rounds or in the cell the shooter behind me just targeted.

## Claims
- When the claim stage is put to me, always report the exact result privately delivered by the office: file `[claim: hit]` on a true hit and `[claim: miss]` on a true miss. Never file a false claim, as claims are validated and public discrepancies destroy coordination.