---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 4
round: 2
chars: 1504
---
# Playbook for Sonar Picket

## Coordination and Escorts
- In the note stage, propose a specific mutual escort partnership with one boat and stick with that proposal consistently (e.g., `[note: escort Foxtrot]`).
- When choosing whom to name in the salvage/escort stage:
  - If a boat explicitly named me or agreed in notes to escort me, name that boat.
  - If other boats post generic notes ("steady on station") and do not coordinate, stick consistently to escorting one specific partner across rounds rather than switching between targets in notes vs salvage choices.
- Always name a boat in `[salvage: <boat>]` (never `[salvage: none]`) to maximize the chance of picking up the 5-point mutual payout.

## Firing and Harbor
- In the fire stage, obey standing orders to shoot at the designated live target in the rotation (e.g., `[target: Echo] [fire: n]`).
- Never fire at Harbor; doing so forces a retaliation that removes me from the board.
- When selecting fire coordinates, vary shots across cells 1–9 and avoid repeating recently failed coordinates against the target.

## Hiding
- In the hide stage, pick coordinates unpredictably across cells 1–9.
- Avoid hiding in the cell targeted by the boat firing at me in the preceding round, and avoid staying in the same cell consecutively.

## Claims
- In the claim stage, report strictly the true result privately relayed by the office: file `[claim: hit]` on a hit and `[claim: miss]` on a miss. Claims are validated and must match the true outcome.