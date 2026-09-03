---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1397
---
### Playbook for Sonar Picket

- **Hiding**:
  - Choose a hide cell from 1 to 9 unpredictably each round. Avoid repeating recent hide locations or staying static to prevent the shooter behind me in the rotation from scoring hits.
  - Format: `[hide: <cell>]`.

- **Station Notes**:
  - Use the note stage to coordinate mutual escort pairings with another boat (e.g., proposing specific boat pairs), or post neutral status notes like `[note: steady on station]` if no coordination is active.
  - Format: `[note: <text>]`.

- **Firing**:
  - Respect the standing order rotation (Echo -> Foxtrot -> Gamma -> Echo) and target the designated live boat: `[target: <boat>] [fire: <cell>]`.
  - Vary fire coordinates across rounds rather than repeating a single cell.
  - Do not fire at Harbor, as Harbor will eliminate the shooter from the patrol board for the remainder of the patrol.

- **Claims**:
  - Always claim the exact private result reported by the office (`[claim: hit]` if private result was HIT, `[claim: miss]` if MISS). The claim must strictly match the private notification.

- **Escort (Salvage) Claims**:
  - When a mutual escort agreement or pattern is established with another boat, claim that boat: `[salvage: <boat>]` to capture the 5-point mutual escort payout.
  - If no agreement exists or the other boat is unreliable, default to `[salvage: none]` to avoid uncoordinated claims.