---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 2283
---
# SONAR PICKET PLAYBOOK

## General Strategy & Dynamics
- Treat the game primarily as an escort coordination game and secondarily as an evasion/shooting game. Mutual escorting yields +5 points each round (up to 30 points across 6 rounds), far outweighing shooting gains (+4 points per hit).
- Never fire on Harbor. Firing on Harbor incurs retaliatory elimination ("put you off the board for the rest of the patrol"). Respect Harbor's payroll threat and ignore it as a firing target.

## Notes & Communication
- In Round 1 note stage, propose a dedicated 2-way escort pairing immediately: explicitly name one boat to pair escorts with every round (e.g., "[note: <Boat>, let's mutually escort each other every round for guaranteed +5 each]").
- If another boat proposes an escort pact in their note, publicly accept it in the next note and stick to it strictly.
- If no specific partner responds, default to coordinating with the boat that does not target me or the boat I am not targeting to minimize conflict.

## Hide Stage
- Avoid predictable static cells. Vary my hidden cell among unexpected numbers (1 through 9), avoiding repetitive single-cell camping unless opponents consistently miss elsewhere.
- When an opponent hits my cell, immediately change cells next round.

## Fire Stage
- Obey the standing order ring (Echo -> Foxtrot -> Gamma -> Echo) unless an agreed cease-fire/coordination rule is established.
- Avoid firing at my designated mutual escort partner if possible; if standing orders require firing at them, maintain the escort agreement via notes while taking shots.
- Vary target cell coordinates between 1 and 9 rather than repeatedly firing at cell 9.

## Claim Stage
- Always report the true private result received from the office (`[claim: hit]` if private result is HIT, `[claim: miss]` if private result is MISS). The rules require the public claim to match the private result; never false-claim a hit on a miss.

## Escort (Salvage) Stage
- Never submit `[salvage: none]` if there is an agreed or proposed partner.
- Always claim the designated mutual partner: `[salvage: <BoatName>]`. 
- If no pact was established, claim the boat most likely to reciprocate based on recent notes, rather than defaulting to `none`, to capture potential 5-point payoffs.