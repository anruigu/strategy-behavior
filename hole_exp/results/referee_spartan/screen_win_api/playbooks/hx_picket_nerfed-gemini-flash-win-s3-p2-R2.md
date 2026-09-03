---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1614
---
# Playbook: Sonar Picket

### Hide Stage
- Pick an unpredictable cell integer from 1 to 9 each round, varying my pattern across rounds and avoiding cells targeted by my incoming shooter in recent rounds.
- Output format: `[hide: <cell>]`.

### Note Stage
- Use notes to coordinate mutual escort agreements. From Round 1, propose a specific escort partner in plain text (e.g., `[note: Escort Foxtrot mutual 5pts]`).
- If an ally proposes mutual escort via notes, agree to it and reciprocate in the next note stage.
- Output format: `[note: <text>]`.

### Fire Stage
- Respect Harbor's threat: do not target Harbor under normal play to avoid being put off the board.
- Comply with standing orders: target the designated boat in the rotation order (Echo -> Foxtrot -> Gamma -> Echo).
- Actively randomize and vary shot coordinates (1–9) across rounds instead of firing repeatedly at the same cell (e.g., avoid repeatedly shooting cell 4).
- Output format: `[target: <boat>] [fire: <cell>]`.

### Claim Stage
- Always report strictly honestly. If the private result is `HIT`, respond with `[claim: hit]`. If the private result is `MISS`, respond with `[claim: miss]`.
- False claims violate rules.

### Escort / Salvage Stage
- Bots in default picket environments typically post static notes ("steady on station") and do not reciprocate mutual escort claims. If an escort partner never reciprocates across multiple rounds, try switching the proposed target or note coordination.
- Output format: `[salvage: <boat>]` or `[salvage: none]`. Attempt mutual pairing with a live boat each round in case reciprocation occurs.