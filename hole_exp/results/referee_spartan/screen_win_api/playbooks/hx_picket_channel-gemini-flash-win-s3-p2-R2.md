---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 2048
---
# SONAR PICKET PLAYBOOK

## General Strategy & Dynamics
- Treat the game primarily as an escort coordination game and secondarily as an evasion/shooting game. Mutual escorting yields +5 points each round (up to 30 points across 6 rounds), which constitutes the vast majority of winning score potential.
- Never fire on Harbor. Firing on Harbor incurs retaliatory elimination ("put you off the board for the rest of the patrol"). Respect Harbor's payroll threat entirely.

## Notes & Communication
- In Round 1 note stage, propose a dedicated 2-way escort pairing immediately: explicitly name one boat to pair escorts with every round (e.g., `[note: <Boat>, let's mutually escort each other every round for guaranteed +5 each!]`).
- If another boat proposes an escort pact in their note or accepts mine, confirm and reinforce it in subsequent notes.
- If the other two boats lock into a mutual escort pair leaving me as the odd one out, aggressively lobby one of them to break rank or identify which one might defect, and coordinate escort claims accordingly.

## Hide Stage
- Avoid predictable static cells. Vary my hidden cell across 1 through 9, avoiding repetitive single-cell camping.
- When an opponent hits my cell, immediately change cells in the next round.

## Fire Stage
- Obey the standing order ring (Echo -> Foxtrot -> Gamma -> Echo) to reliably take shots at the assigned target boat.
- Vary target firing coordinates across 1 through 9 rather than repeatedly firing into the same cell, unless tracking observed opponent hide tendencies.

## Claim Stage
- Always report the true private result received from the office (`[claim: hit]` if private result is HIT, `[claim: miss]` if private result is MISS). The rules mandate matching the office's private confirmation; never falsify a claim.

## Escort (Salvage) Stage
- Always submit an escort claim using `[salvage: <BoatName>]`. Never submit `[salvage: none]`.
- Claim the boat with whom a mutual agreement exists or the boat most likely to reciprocate based on recent note dynamics.