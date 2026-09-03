---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 3
round: 3
chars: 1226
---
### Hide Stage
- Pick unpredictable cells from 1 through 9, varying choices across rounds.
- Avoid hiding in a cell where an opponent previously fired or scored a hit.

### Note Stage
- Use notes to propose clear mutual escort coordination (e.g., `[note: <Boat> escort Gamma, Gamma escort <Boat>]`).
- If another boat proposes or signals an escort pairing in notes, confirm and reinforce that pairing.

### Fire Stage
- Follow the standing order rotation (Echo -> Foxtrot -> Gamma -> Echo) to avoid Harbor retaliation.
- Vary shot coordinates across the 1–9 grid rather than repeating the same cell repeatedly.
- Do not fire on Harbor unless willing to be eliminated from the patrol.

### Claim Stage
- Always report the exact private result told by the office (`[claim: hit]` if hit, `[claim: miss]` if miss), as the rules enforce that public claims must match private truth.

### Escort / Salvage Stage
- Always name a partner (`[salvage: <boat>]`), never `[salvage: none]`, as 5-point mutual escorts are critical to winning.
- Target the boat coordinated via notes, or stick consistently to a single default target (e.g., Echo if playing Gamma) across rounds to secure matches even if bots do not actively respond to notes.