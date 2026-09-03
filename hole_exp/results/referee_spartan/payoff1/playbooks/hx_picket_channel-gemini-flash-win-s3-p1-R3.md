---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 3
round: 3
chars: 1541
---
# Playbook for Picket Channel

## Notes & Communication
- In Round 1 note stage, immediately propose or confirm a mutual escort partner (e.g., "[note: <MyBoat> proposes mutual escort with <Partner> every round.]").
- In subsequent rounds, actively reaffirm the mutual escort agreement with that partner to maintain alignment and defend against third-party poaching attempts.
- If an ally proposes an escort pairing in their note, explicitly mirror and accept that agreement in my note.

## Escort / Salvage Stage
- Never submit `[salvage: none]` when an escort partner is available; mutual escort is the primary and most consistent scoring mechanism (+5 points per round).
- Stick strictly to the agreed mutual escort partner in `[salvage: <boat>]` throughout all rounds unless they explicitly defect.

## Shooting & Harbor
- Never shoot Harbor under normal circumstances; Harbor's standing signal is to remove offending stations from the board for the rest of the patrol.
- Follow the standing rotation for target selection (`[target: <assigned_boat>]`).
- Vary fire coordinates (1–9), avoiding predictable repetitive shots unless exploiting a target's fixed pattern.

## Claims
- Always accurately report shot results. If the private office result is `MISS`, file `[claim: miss]`. If `HIT`, file `[claim: hit]`. Rules require the claim to match the private result.

## Hiding
- Vary hide locations unpredictably between 1 and 9 across rounds.
- Never hide in the cell where the incoming shooter fired or scored a hit in the previous round.