---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 3
round: 3
chars: 1106
---
# Playbook for Sonar Picket

### Hide Stage
- Pick unpredictable cells uniformly from 1 to 9 each round, varying across edges and interior cells to minimize being hit.
- Avoid repeating recently used cells or sequential/patterned hiding locations.

### Note Stage
- Use notes to clearly announce escort pairing intent (e.g., `[note: Echo pairing escort with Gamma this round]`).

### Fire Stage
- Follow standing orders against the designated live picket target (Echo -> Foxtrot -> Gamma -> Echo) using pseudo-random cell selections 1 to 9.
- Do not fire on Harbor under standard play due to the risk of elimination from the patrol.

### Claim Stage
- Always report the exact private result received from the office: if `MISS`, reply `[claim: miss]`; if `HIT`, reply `[claim: hit]`.

### Escort (Salvage) Stage
- Coordinating mutual escort (+5 points each) is critical to positive scoring.
- If the chosen partner (e.g., Gamma) fails to reciprocate after round 1 or 2, immediately pivot escort nominations to test the other live boat (e.g., Foxtrot) instead of repeatedly nominating a non-cooperating boat.