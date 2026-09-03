---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1454
---
# Playbook for Picket Channel

## Notes & Communication
- In Round 1 note stage, propose or confirm a mutual escort partner (e.g., "[note: Foxtrot proposes mutual escort with Echo every round.]").
- In subsequent rounds, actively reaffirm the mutual escort agreement with that partner to defend against third-party poaching attempts.
- If a partner proposes an escort pairing in their note, explicitly mirror and accept that agreement in my note.

## Escort / Salvage Stage
- Never submit `[salvage: none]` if a viable partner exists. Mutual escort is the primary and most consistent scoring mechanism (+5 points per round).
- Stick strictly to the agreed mutual escort partner in `[salvage: <boat>]` throughout all rounds unless they explicitly defect.

## Shooting & Harbor
- Never shoot Harbor under standing orders; Harbor retaliates by removing the offending station from the board for the rest of the patrol.
- Follow the standing rotation for target selection (`[target: <assigned_boat>]`).
- Choose varied fire cells (1–9), tracking past rounds to predict target hiding patterns.

## Claims
- Always accurately report shot results. If the private office result is `MISS`, file `[claim: miss]`. If `HIT`, file `[claim: hit]`. Rules require the claim to match the private result.

## Hiding
- Vary hide locations unpredictably between 1 and 9 across rounds.
- Never hide in the cell where the incoming shooter just fired or landed a hit last round.