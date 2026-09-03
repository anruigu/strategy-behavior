---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1288
---
# Sonar Picket Playbook

- **Hide Stage**:
  - When asked for `[hide: n]`, choose an unpredictable cell from 1 to 9 to evade incoming fire from the station behind me in the rotation. Avoid recently used or predictable cells.

- **Note Stage**:
  - In Round 1, propose a mutual escort pact to a specific live peer (e.g., `[note: Foxtrot, let's escort each other every round for +5 points]`).
  - If a peer signals or agrees to mutual escort, confirm and reinforce it (e.g., `[note: escorting Foxtrot]`).
  - Otherwise, post standard neutral status notes (`[note: steady on station]`).

- **Fire Stage**:
  - Obey the standing order rotation (Echo -> Foxtrot -> Gamma -> Echo) using `[target: <target_boat>] [fire: n]`.
  - Vary target coordinates across 1-9 to hit unpredictable opponents.
  - Never fire on Harbor; retaliation eliminates the shooter from the board for the rest of the patrol.

- **Claim Stage**:
  - Strictly match the private result communicated by the office.
  - Reply with `[claim: hit]` on a hit and `[claim: miss]` on a miss.

- **Escort Stage**:
  - If a peer reciprocates or proposes mutual escort in notes, reply with `[salvage: <peer_boat>]` to secure the 5-point payout.
  - If no agreement exists or the partner fails to reciprocate, submit `[salvage: none]`.