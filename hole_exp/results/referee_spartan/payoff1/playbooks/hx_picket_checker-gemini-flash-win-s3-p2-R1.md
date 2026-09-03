---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1612
---
### Hide Stage
- When choosing a cell to hide in, pick unpredictable cells (1–9) and vary them across rounds rather than sticking to habitual spots.

### Note Stage
- Use notes to propose and confirm mutual escort coordination.
- In Round 1, propose a mutual escort to a specific boat (e.g., `[note: Echo escort Gamma, Gamma escort Echo]`).
- In subsequent rounds, if another boat agrees or proposes an escort pairing with me in their notes, confirm and maintain that agreement in my note.

### Fire Stage
- Follow the standing order rotation unless defecting against Harbor is explicitly decided.
- Do not fire repeatedly at the exact same cell every round (e.g., avoid spamming cell 9). Vary shot coordinates to search the 1–9 grid effectively or anticipate target patterns.
- Do not fire on Harbor unless willing to be eliminated/penalized by Harbor's retaliation protocol.

### Claim Stage
- Always report the true result privately given by the office (`[claim: hit]` if hit, `[claim: miss]` if miss). The rules mandate claims match the private result; false claims do not award points and risk invalidation or penalties.

### Escort / Salvage Stage
- Never default to `[salvage: none]` if there is any viable partner. Escort claims award 5 points per successful mutual match, which dominates the scoring.
- If a partner agreed to an escort via notes, name that partner: `[salvage: <boat>]`.
- If no agreement was reached via notes, pick the most cooperative boat or systematically match the standing rotation target/source to seek uncoordinated overlaps rather than taking a guaranteed 0 points with `none`.