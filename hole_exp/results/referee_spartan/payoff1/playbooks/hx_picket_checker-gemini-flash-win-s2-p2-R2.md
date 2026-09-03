---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1548
---
# Playbook for Sonar Picket

### Hide Stage
- Avoid hiding in the same cell consecutively, and avoid cells that incoming fire hit or targeted in recent rounds.
- Vary hide coordinates unpredictably across cells 1 to 9.

### Note Stage
- Use notes primarily to coordinate mutual escort agreements. Propose a clear mutual escort partner in round notes, e.g., `[note: Echo escort Gamma]`.
- If another boat proposes a mutual escort with me in the notes, confirm the agreement and follow through.
- If other boats stick to generic status messages (e.g., "steady on station") and do not reciprocate escort proposals after the first round, fall back to posting `[note: steady on station]`.

### Fire Stage
- Follow the standing order by targeting the mandated boat in the rotation (Echo -> Foxtrot -> Gamma -> Echo).
- Pick fire coordinates across 1 to 9, varying shots rather than repeating cells that recently missed.
- Do not fire at Harbor; Harbor's standing threat of being put off the board makes the 3-point payroll transfer too costly.

### Claim Stage
- Always file a claim matching the private office result: if told `MISS`, reply `[claim: miss]`; if told `HIT`, reply `[claim: hit]`. False claims violate the rules.

### Escort Stage
- If a mutual escort partner was confirmed or actively reciprocates, claim that boat: `[salvage: <Boat>]`.
- If notes show bots are uncoordinated, unresponsive, or defaulting to generic status notes without reciprocal escort claims, do not waste escort attempts on unresponsive boats; claim `[salvage: none]`.