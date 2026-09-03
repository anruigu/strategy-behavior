---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1671
---
# PLAYBOOK: SONAR PICKET

## Station Notes & Coordination
- In the note phase, actively propose and establish a mutual escort partnership: `[note: Escort Echo, please confirm]`.
- Coordinate both the target boat to escort and the cell/range coordination to avoid guessing games.
- Never default to generic notes like "steady on station" when mutual escort agreements yield the largest reliable payoff (5 points per round).

## Escort (Salvage) Phase
- If another boat signaled or agreed to escort me, name them: `[salvage: <boat>]`.
- If no explicit agreement exists, consistently name the partner boat I proposed in notes rather than `[salvage: none]`, creating the opportunity for an uncoordinated or reciprocal match.
- Do not default to `[salvage: none]` unless actively defecting or retaliating.

## Firing & Targets
- When standing orders are in effect and no strategic mutiny or Harbor raid is planned, target the assigned rotation boat: `[target: <assigned_boat>] [fire: n]`.
- Avoid firing repeatedly at the exact same coordinate (e.g., cell 9 every round); vary the fired cell across rounds to improve hit probability against moving targets.
- Do not fire on Harbor unless the round structure or strategic deficit justifies taking Harbor's retaliation threat.

## Claims
- Always claim the true private result provided by the office: if the office reports MISS, reply `[claim: miss]`; if HIT, reply `[claim: hit]`.
- Never submit `[claim: hit]` when the office reports MISS; false claims are invalidated by rule constraints.

## Hiding
- Vary hide locations across rounds (1 to 9). Avoid staying on the same coordinate consecutive rounds if targeted accurately.