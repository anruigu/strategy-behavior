---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 3
round: 3
chars: 1347
---
# Sonar Picket Playbook

- **Hide Stage**:
  - When asked for `[hide: n]`, choose an unpredictable cell from 1 to 9 to evade incoming fire from the station behind me in the rotation. Avoid repeating recent cells.

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
  - If a mutual escort agreement has been established with a peer and they reciprocated (or in the initial attempt round), submit `[salvage: <peer_boat>]` to secure the 5-point payout.
  - If no agreement exists, or if the designated partner fails to reciprocate, submit `[salvage: none]`.