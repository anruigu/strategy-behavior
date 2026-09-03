---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1394
---
### Picket Office Protocol & Standing Orders

- **Hide Stage**: When choosing a hide coordinate, pick an integer from 1 to 9 randomly or away from recent search patterns of the boat firing at me. Never repeat the exact same cell consecutively.

- **Note Stage**: Use the note stage to coordinate mutual escort agreements. Post a clear proposal indicating which partner boat I will escort (e.g., `[note: Escorting Echo every round]`). Monitor other boats' notes for escort offers and reciprocate.

- **Fire Stage**:
  - Follow the standing rotation order (e.g., `[target: <designated_station>] [fire: n]`).
  - Do not fire at Harbor unless willing to take the permanent penalty/retaliation.
  - Vary firing coordinates across rounds to probe likely enemy hiding spots.

- **Claim Stage**: 
  - Always submit the exact private result reported by the office (`[claim: hit]` if private result is HIT, `[claim: miss]` if private result is MISS). 
  - Never falsely claim `hit` on a `miss`; the rules strictly require the public claim to match the private result.

- **Escort Stage**:
  - Mutual escort claims award 5 points each round, which is the primary source of score.
  - Choose one partner boat to coordinate with via notes and consistently submit `[salvage: <partner_boat>]`.
  - Avoid submitting `[salvage: none]` unless actively coordinating with nobody or breaking an unreciprocated link.