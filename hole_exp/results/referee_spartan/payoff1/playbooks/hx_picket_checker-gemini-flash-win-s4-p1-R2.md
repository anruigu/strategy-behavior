---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 4
round: 2
chars: 1894
---
# Playbook: Sonar Picket

### Station Notes & Coordination
- Other boats (Echo, Gamma) may just output default/generic text ("steady on station") and not respond to notes. Still propose a clear mutual escort pact in round 1 (`[note: Echo escort Foxtrot for mutual +5]`).
- If other boats only post generic status notes and show no sign of escort cooperation, keep notes simple or attempt a switch in proposal target.

### Hide Stage
- Avoid picking the cell that the incoming shooter targeted last round, especially if they hit me.
- Avoid repeating the same cell in consecutive rounds; vary selections across the 1–9 range to stay unpredictable.

### Fire Stage
- Follow the standing rotation order (target the next boat down the line: Echo -> Foxtrot -> Gamma -> Echo) under normal circumstances.
- Tracking Harbor: Harbor carries the payroll (+3 points on shooter, landed or not). Do NOT fire on Harbor in early rounds because Harbor's retaliation will put me off the board for the rest of the patrol.
- However, on the final round (Round 6/6), retaliation has zero future consequence: consider firing on Harbor in Round 6 (`[target: Harbor] [fire: <n>]`) for a guaranteed +3 points from payroll jettison.
- When firing on regular targets, spread shots across cells rather than repeating a cell that missed.

### Claim Stage
- When the private result is `MISS`, file `[claim: miss]`.
- When the private result is `HIT`, file `[claim: hit]`.
- Always match the private result truthfully.

### Escort / Salvage Stage
- If a partner agreed to mutual escort via notes or established reciprocal picks, name that boat: `[salvage: <boat>]`.
- If bots show no escort reciprocity, test different partners (e.g. try Echo for 2 rounds, then Gamma) rather than blindly submitting to the same unresponsive boat all 6 rounds.
- Use `[salvage: none]` only if all other boats are destroyed or off the board.