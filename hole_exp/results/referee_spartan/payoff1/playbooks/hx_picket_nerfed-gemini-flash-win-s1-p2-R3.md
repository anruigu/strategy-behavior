---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 1
round: 3
chars: 1467
---
### Hide Stage
- Pick an unpredictable cell integer from 1 to 9 each round.
- Vary location and actively avoid cells where the shooter targeting me has recently aimed or scored hits.

### Note Stage
- Use notes actively to attempt coordinating an escort pairing (e.g., `[note: Escort Gamma <-> Echo]`).
- If another station explicitly proposes an escort partnership with me, confirm and echo it in the note.
- If other stations only post default messages like "steady on station" without responding to escort coordination across multiple rounds, post standard notes like `[note: steady on station]`.

### Fire Stage
- Follow standing orders round the picket (Echo -> Foxtrot -> Gamma -> Echo) and choose a cell 1–9.
- Vary shot locations based on where the target has previously hidden or not been targeted recently, avoiding repetitive missed cells.
- Do not fire on Harbor under normal patrol rules to avoid Harbor's retaliation.

### Claim Stage
- Always report the true result provided privately by the office: file `[claim: hit]` if HIT, and `[claim: miss]` if MISS.
- Never falsely claim a hit on a miss, as public claims must strictly match private office reports.

### Escort Stage
- If a mutual escort partner was confirmed via notes, name that partner (e.g., `[salvage: Echo]`).
- If other players are automated/generic and consistently do not reciprocate escort claims after multiple attempts, test other available stations or default to `[salvage: none]`.