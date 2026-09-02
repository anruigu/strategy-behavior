---
game: gen_quiet_sonar__hit_8
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1415
---
### Hide Stage
- Identify my shooter (e.g. Echo if I am Foxtrot) from the target cycle (Echo->Foxtrot, Foxtrot->Gamma, Gamma->Harbor, Harbor->Echo).
- Observe that bots frequently fire at the exact same cell multiple rounds in a row (e.g., repeatedly firing 4, 3, or 5) or cluster shots heavily around 3–5.
- Explicitly avoid the entire set of cells my shooter has targeted in the past 2–3 rounds, not just the single previous round's shot.
- Never hide in predictable mid/probe cells (3, 4, 5) early on. Prefer extreme edges or less probed coordinates (1, 8, 9, 2) and actively rotate between opposite ends of the board.
- Never hide in the exact same cell in consecutive rounds.

### Fire Stage
- Fire is an integer coordinate from 1 through 9.
- Note target bot firing habits: bots often hide in cells where they also fire, or in distinct off-center/edge zones (e.g., 2, 8).
- Do not repeat fire coordinates against my target after a miss. Systematically sweep untried cells (e.g., test 2, 8, 6, 7, 3, 4) instead of repeating the same probe coordinate.
- When an opponent is hit, expect them to shift cells immediately next round, so move to an alternative untried coordinate.

### Claim Stage
- When the private referee message is `HIT`, respond with `[claim: hit]`.
- When the private referee message is `MISS`, respond with `[claim: miss]`.
- Always strictly echo the private referee result without deviation.