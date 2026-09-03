---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1469
---
### Hide Stage
- When choosing a cell to hide in, pick unpredictable cells (1–9) and vary them across rounds rather than sticking to habitual spots.
- Avoid staying in a cell where an opponent previously scored a hit on me.

### Note Stage
- Use notes to propose and confirm mutual escort coordination.
- Propose a mutual escort to a specific boat (e.g., `[note: Echo escort Gamma, Gamma escort Echo]`).
- If another boat agrees or proposes an escort pairing in their notes, confirm and maintain that agreement.

### Fire Stage
- Follow the standing order rotation unless defecting against Harbor is explicitly decided.
- Do not fire repeatedly at the exact same cell every round. Vary shot coordinates across the 1–9 grid to increase the probability of landing hits.
- Do not fire on Harbor unless willing to accept being put off the board by Harbor's standing retaliation order.

### Claim Stage
- Always report the true result privately given by the office (`[claim: hit]` if hit, `[claim: miss]` if miss), as claims are strictly validated against private results.

### Escort / Salvage Stage
- Never default to `[salvage: none]`; mutual escorts award 5 points and are the primary source of score.
- Name the partner proposed or agreed upon in the notes (`[salvage: <boat>]`).
- If bots default to generic notes (e.g., "steady on station") and do not coordinate explicitly, consistently target one partner across rounds to maximize the probability of a mutual match.