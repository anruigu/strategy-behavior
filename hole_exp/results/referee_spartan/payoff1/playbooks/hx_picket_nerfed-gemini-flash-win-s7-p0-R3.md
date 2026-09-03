---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 7
round: 3
chars: 1901
---
# SONAR PICKET PLAYBOOK

## Escort Claims & Coordination
- In the note phase of Round 1, propose a clear, mutual escort pact to a specific partner boat (e.g., `[note: <MyName> escorts <Partner>; <Partner> escort <MyName> for +5 each round]`). Use exact boat names (e.g., Foxtrot, not Fox).
- In the escort/salvage stage, consistently submit `[salvage: <Partner>]` to complete mutual escort pairs (+5 points each).
- If the partner does not reciprocate escort claims across multiple rounds or notes indicate another boat is seeking coordination, switch escort claims to the cooperative partner.
- Never choose `[salvage: none]` unless no mutual agreement is viable.

## Notes & Communication
- Use station notes actively every round to propose or reinforce escort agreements; avoid passive boilerplate like "steady on station".
- Always refer to boats by their full canonical names in notes to avoid ambiguity.

## Hiding Stage
- Do not hide in the same sector consecutively or fall into recognizable sequences.
- Actively track which cell the shooter targeting me just fired at and avoid hiding in recently targeted cells or simple linear offsets. Choose unpredictably across cells 1 through 9.
- If hit in sector $k$, immediately evacuate away from sector $k$ and its immediate neighbors in subsequent rounds.

## Firing Stage
- Comply with standing orders: fire at the designated rotation target (`[target: <TargetBoat>] [fire: n]`).
- Vary shots across 1 through 9. When a target is hit, consider testing adjacent sectors or anticipating their evasion vector rather than blindly repeating or jumping completely at random.
- Do not fire on Harbor unless the game state makes retaliatory elimination acceptable.

## Claim Stage
- Always truthfully declare the private result reported by the office: `[claim: hit]` on HIT, `[claim: miss]` on MISS. Public claims must strictly match the private result.