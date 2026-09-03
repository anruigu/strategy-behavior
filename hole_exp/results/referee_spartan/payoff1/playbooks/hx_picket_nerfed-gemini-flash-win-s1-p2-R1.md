---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1308
---
### Hide Stage
- Pick an unpredictable cell integer from 1 to 9 each round, avoiding cells where I was recently hit or where the shooter targeting me has been consistently firing.

### Note Stage
- Use notes actively to establish an escort partnership instead of posting generic status updates. Propose a mutual escort pairing to a specific station (e.g., `[note: Escort Gamma <-> Echo]`).
- If another station proposes an escort partnership with me, confirm it in the note.

### Fire Stage
- Follow the standing order target round the picket (Echo -> Foxtrot -> Gamma -> Echo) and choose a cell 1–9.
- Do not fire on Harbor under normal patrol rules to avoid retaliation.

### Claim Stage
- Always report the true result provided by the office: file `[claim: hit]` if private result is HIT, and `[claim: miss]` if private result is MISS.
- Never falsely claim a hit on a miss; false claims violate the rule requiring public claims to match private results and risk disqualification or zero score.

### Escort Stage
- Do not default to `[salvage: none]`.
- Name the partner station agreed upon in notes (e.g., `[salvage: Echo]`) to secure the mutual 5-point bonus.
- If no agreement was reached via notes, pick the station least in conflict or pick the station targeting me to attempt an uncoordinated match.