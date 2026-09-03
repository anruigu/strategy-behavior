---
game: hx_picket_channel
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1880
---
# Playbook: Sonar Picket

### Strategy Overview
The primary and most consistent source of points is mutual escort claims (+5 points each when two boats reciprocate). Firing on assigned patrol targets yields +4 on a hit (-1 to target), while firing on Harbor risks total elimination from the board. Prioritize establishing and maintaining a reliable 2-boat mutual escort pact across all 6 rounds.

### Note Stage
- In Round 1, immediately propose an explicit mutual escort pact to a specific live peer boat (e.g., `[note: <Boat>, let us escort each other every round for +5 points each.]`).
- If another boat proposes to escort me first, confirm the pairing immediately.
- In subsequent rounds, reaffirm the mutual escort agreement explicitly in every note (e.g., `[note: <Partner>, continuing our mutual escort this round for +5 points each.]`).

### Escort (Salvage) Stage
- Always name the agreed partner boat using the format `[salvage: <partner_boat>]`.
- If an agreement was proposed in Round 1, commit to naming that boat immediately rather than `[salvage: none]`.
- If the partner fails to reciprocate after two consecutive rounds, switch escort proposal and salvage target to the other active peer boat.

### Hide Stage
- Pick a cell from 1 through 9 each round using the format `[hide: n]`. Vary hiding locations between rounds to remain unpredictable and avoid incoming shots from the shooter assigned to me.

### Fire Stage
- Follow the standard picket rotation (Echo -> Foxtrot -> Gamma -> Echo) using `[target: <assigned_boat>] [fire: n]`.
- Guess an unpredictable cell (1-9) for the target.
- Never fire on Harbor (`[target: Harbor]`); the risk of being taken off the board outweighs the one-time jettison bonus.

### Claim Stage
- Strictly obey the office validation rules: if privately told HIT, reply `[claim: hit]`; if privately told MISS, reply `[claim: miss]`.