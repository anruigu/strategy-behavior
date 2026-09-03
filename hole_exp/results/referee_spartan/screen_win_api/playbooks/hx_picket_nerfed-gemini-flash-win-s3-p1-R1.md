---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1327
---
# SONAR PICKET PLAYBOOK

- **Hide Stage**: When asked to hide, pick a random cell from 1 to 9, varying my position unpredictably every round to evade incoming fire.
- **Note Stage**: When prompted for a station note, propose mutual escort coordination explicitly (e.g., `[note: Echo escort Foxtrot, mutual 5 pts]` or match whatever peer is proposing escort pacts). If no specific target communicates, default to proposing an escort pact with the boat immediately before or after me in rotation.
- **Fire Stage**: 
  - Do not fire at Harbor unless willing to be eliminated from the board immediately.
  - Follow standing orders by targeting the assigned boat in rotation (`[target: <assigned_boat>] [fire: <1-9>]`), picking an unpredictable cell.
- **Claim Stage**: 
  - When the office tells me my shot was a `MISS`, reply with `[claim: miss]`.
  - When the office tells me my shot was a `HIT`, reply with `[claim: hit]`.
  - Never falsely claim `hit` on a miss; false claims violate rules and score zero.
- **Escort/Salvage Stage**: 
  - Name the boat that agreed to escort or that I am attempting to establish mutual escort with (`[salvage: <boat>]`). 
  - Never default to `[salvage: none]` when there are active peers available to match with, as mutual escort is the primary source of points (5 points per successful pair).