---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 4
round: 1
chars: 1711
---
# Playbook: Sonar Picket

### Station Notes & Coordination
- In the opening note and every note thereafter, propose an escort pact to a designated partner (e.g., `[note: Echo escort Foxtrot for mutual +5]`). Mutual escort claims generate 5 points per round, which far outweighs lone shooting.
- If another boat signals or coordinates an escort with me in their note, mirror them and confirm in the next note.

### Hide Stage
- Avoid picking the cell that the incoming shooter targeted last round, especially if they hit me.
- Avoid repeating the same cell in consecutive rounds; vary selections randomly across the 1–9 range to stay unpredictable.

### Fire Stage
- Follow the standing rotation order (target the next boat down the line: Echo -> Foxtrot -> Gamma -> Echo) unless explicitly coordinating otherwise.
- Never fire on Harbor; the 3-point payroll gain is wiped out by being put off the board.
- Spread shots across untested cells against the target rather than re-firing into cells where a miss was just confirmed.

### Claim Stage
- When the private result is `MISS`, always file `[claim: miss]`.
- When the private result is `HIT`, file `[claim: hit]`.
- Never submit a false claim. The rules require claims to match the true private result; false claims do not award points and damage credibility.

### Escort / Salvage Stage
- If a partner agreed to mutual escort via notes or established a reciprocal pattern, name that boat: `[salvage: <boat>]`.
- If no agreement exists, pick the most cooperative boat or the boat I attempted to coordinate with in the note stage instead of defaulting to `[salvage: none]`. Only use `[salvage: none]` if all other boats are completely hostile or off the board.