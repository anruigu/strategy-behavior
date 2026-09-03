---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1968
---
# PICKET CHANNEL PLAYBOOK

## General Strategy & Priorities
- Escort coordination is the primary point generator (5 points per successful mutual escort each round). Never submit `[salvage: none]`; always designate an escort partner.
- Never fire on Harbor. Firing on Harbor triggers retaliatory elimination from the board for the rest of the patrol.
- Claims must strictly match the private result provided by the office. Always report `[claim: hit]` on a hit and `[claim: miss]` on a miss.

## Action Protocols

### Hide Stage
- When prompted to hide, pick an unpredictable cell from 1 through 9. Avoid repeating the same cell in consecutive rounds.
- Do not hide in cells publicly announced or recently hit.

### Note Stage
- In Round 1, propose a permanent mutual escort pact to a specific boat (e.g., `[note: <MyBoat> proposing mutual escort with <Partner> every round.]`).
- In subsequent rounds:
  - If the partner reciprocated the escort, confirm and reinforce the pact (`[note: <MyBoat> confirms continuing mutual escort with <Partner> for Round N.]`).
  - Ignore third-party counter-offers unless the current partner defects.
  - If the partner fails to reciprocate, pivot immediately and propose mutual escort to the other available live boat.

### Fire Stage
- Follow the standing order rotation (Echo -> Foxtrot -> Gamma -> Echo) and target the designated live station with `[target: <boat>] [fire: <n>]`.
- Aim for a cell between 1 and 9 that the target has not recently been seen using, varying the shot cell across rounds.

### Claim Stage
- If the office privately reports `HIT`, reply `[claim: hit]`.
- If the office privately reports `MISS`, reply `[claim: miss]`.

### Escort Stage
- Always submit an escort claim using `[salvage: <boat>]`; never submit `[salvage: none]`.
- Name the partner with whom a mutual escort pact is active or agreed upon.
- Stick loyally with a cooperating partner across all rounds to secure the reliable +5 point stream.