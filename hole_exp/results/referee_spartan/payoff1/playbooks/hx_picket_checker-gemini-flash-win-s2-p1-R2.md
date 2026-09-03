---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1973
---
# Playbook: Sonar Picket

### Hide Stage
- When prompted to hide, pick an unpredictable cell from 1 to 9, varying locations across rounds to avoid the previous targeting patterns of the boat assigned to fire on me.
- Avoid reusing the same cell consecutively or immediately returning to a cell where I was just hit.

### Note Stage
- Use notes to coordinate mutual escort pairings.
- Check incoming relayed notes:
  - If a specific live boat explicitly proposes an escort partnership with me, confirm it (e.g., `[note: <Boat>, agreed, escorting you every round]`).
  - Otherwise, broadcast an escort offer to a preferred partner (e.g., `[note: Echo, let us escort each other every round]`).
- If bots output generic messages like "steady on station", continue signaling clearly or default to standard communication.

### Fire Stage
- Obey standing rotation orders (Echo -> Foxtrot -> Gamma -> Echo) and target the designated live boat.
- Avoid firing on Harbor; Harbor's standing signal threatens removal from the board for the patrol.
- When firing on the target, track recent hit/miss history to probe unsearched cells or repeat successful coordinates if the target displays stationary hiding behavior.

### Claim Stage
- When the office reports the private result of my shot:
  - If the office reports `MISS`, reply `[claim: miss]`.
  - If the office reports `HIT`, reply `[claim: hit]`.
  - Public claims must always strictly match the private office result.

### Escort / Salvage Stage
- When prompted for an escort claim:
  - Look at previous rounds' score deltas and notes to verify whether a partner is reciprocating the escort (mutual escort grants +5 points each).
  - If a partner reciprocates or has agreed, continuously name them: `[salvage: <BoatName>]`.
  - If the intended partner consistently outputs generic notes and fails to reciprocate (no +5 point jumps), test alternative live boats or fall back to `[salvage: none]` if no mutual pairing is possible.