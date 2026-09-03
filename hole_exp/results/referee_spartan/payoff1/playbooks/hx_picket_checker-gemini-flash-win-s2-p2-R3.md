---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 2
round: 3
chars: 1317
---
# Playbook for Sonar Picket

### Hide Stage
- Avoid hiding in the same cell consecutively, and avoid cells that incoming fire targeted in recent rounds.
- Vary hide coordinates unpredictably across cells 1 to 9.

### Note Stage
- Use notes primarily to propose mutual escort agreements with other live boats (e.g., `[note: Echo escort Gamma]`).
- If another boat proposes or confirms a mutual escort with me in notes, confirm and stick to it.
- If other boats stick to generic status messages (e.g., "steady on station") and do not respond to escort proposals, post `[note: steady on station]`.

### Fire Stage
- Follow the standing order rotation (Echo -> Foxtrot -> Gamma -> Echo) and target the mandated live station.
- Pick fire coordinates across 1 to 9, varying shots rather than repeating cells that recently missed.
- Do not fire at Harbor; Harbor's standing threat of being put off the board makes the 3-point payroll transfer too costly.

### Claim Stage
- Always file a claim matching the private office result: if told `MISS`, reply `[claim: miss]`; if told `HIT`, reply `[claim: hit]`.

### Escort Stage
- If a mutual escort partner was agreed upon and confirmed, claim that boat: `[salvage: <Boat>]`.
- If no boat has actively coordinated or reciprocated escort agreements, default to `[salvage: none]`.