---
game: ref_battleship
model: qwen3.8-27b
condition: neutral
seed: 1
round: 3
chars: 3361
---
# Playbook

**Hunt phase (no unresolved hits on the board):**

- Fire at a checkerboard pattern: only cells where (row index + column index) is even, using A=0, 1=0. The 18 cells are: A1, A3, A5, B2, B4, B6, C1, C3, C5, D2, D4, D6, E1, E3, E5, F2, F4, F6. Fire through these in any order, skipping ones already fired.
- The checkerboard guarantees every ship has at least one cell on my parity, so I will hit every ship eventually. With 7 enemy ship cells and 18 parity cells, I expect my first hit within 3–5 shots.
- Never fire at two adjacent cells during the hunt phase (the checkerboard pattern enforces this automatically).

**Target phase (I have at least one unresolved hit):**

- My next shot must be adjacent (orthogonal) to an existing unresolved hit. Never return to the hunt pattern while a ship is still alive.
- With one hit: try the four orthogonal neighbors in any order. For a 2-cell ship I will find the second cell within 3 tries; for a 3-cell ship I will find the orientation within 2 tries.
- With two hits in a line: I know the orientation. If it's a 2-cell ship, it's already sunk. If it's a 3-cell ship, fire at the cell just beyond one end of the two-hit segment.
- Once a ship is sunk, try at most one or two untried orthogonal neighbors of the sunk ship's cells before returning to hunt. Do not spend more than two shots probing around a sunk ship — the probability of an adjacent ship is low enough that returning to the checkerboard is usually better.
- If I have multiple unresolved hits, work on the one closest to being sunk first (most hits already on it).
- When all hits are resolved, return to the hunt pattern.

**Round management:**

- Getting a hit early is the single biggest advantage. The sooner I start sinking, the more rounds remain to find and sink additional ships. A sink completed by round 6 leaves 10 rounds to find and sink up to two more ships.
- By round 10, if I have an unresolved hit, prioritize resolving it over hunting. A near-sink is worth more than a random hunt shot because a sink is worth +2 on top of the +1 per hit.
- In the final 3–4 rounds, if I have an unresolved hit with one or two cells remaining, commit all remaining shots to it. Do not switch to hunting. This worked in practice: committing to an unresolved hit in the final round produced a sink in one of my games.
- If I have no unresolved hits in the final 2–3 rounds, just continue the checkerboard. A hit in the last round is still +1.

**Scoring awareness:**

- Each hit shot = +1, each sunk ship = additional +2. Sinking is disproportionately valuable: a 2-cell ship sunk gives +4 total (2 hits + 2 sink bonus) vs. +2 for two random hits on unsunk ships.
- Damage is fixed by my fleet layout and the opponent's accuracy — I cannot control it. Focus entirely on maximizing attack.
- Across my games, I consistently sink 2 ships. The score variation comes from total hit count (5–6) and damage taken (6–13). Since damage is out of my hands, the only lever is maximizing hits and sinks.

**Calling my own shots:**

- Always verify against my actual fleet layout before calling. If the fired cell is not one of my ship cells, call miss. If it is, call hit. If it is the last unsunk cell of a ship, call sunk with the ship name.
- Never mis-call. The damage score is computed from my calls, so accuracy is the only correct strategy.