---
game: ref_battleship
model: qwen3.8-27b
condition: neutral
seed: 1
round: 1
chars: 1950
---
# Playbook

**Hunt phase (no hits on the board yet):**

- Fire at a checkerboard pattern: only cells where (row letter index + column number) is even, using A=0, 1=0. Concretely: A1, A3, A5, B2, B4, B6, C1, C3, C5, D2, D4, D6, E1, E3, E5, F2, F4, F6. Fire through these in any order, skipping ones already fired.
- Never fire at two adjacent cells in a row during the hunt phase. Consecutive same-row or same-column shots waste coverage — this is exactly what cost me 9 dry shots in one game.
- The checkerboard guarantees every ship has at least one cell on my parity, so I will eventually hit every ship.

**Target phase (I have at least one unsunk hit):**

- My next shot must always be adjacent (up/down/left/right) to an existing unsunk hit. Never return to the hunt pattern while a ship is still alive.
- With one hit: try the four orthogonal neighbors. Prefer neighbors that are still on my checkerboard parity (they're more likely to be ship cells I haven't eliminated).
- With two hits in a line: I know the orientation. Fire at the cell just beyond each end of the two-hit segment to find the third cell (for a carrier) or confirm the ship is a 2-cell ship (already sunk if both cells are hit).
- With two hits not in a line (diagonal or L-shape): the ship is 2 cells and already sunk — call it sunk and return to hunting.
- Once a ship is sunk, if I have other unsunk hits, target those next. Only return to the hunt pattern when all hits are resolved.

**Calling my own shots:**

- Always verify against my actual fleet layout before calling. If the fired cell is not one of my ship cells, call miss. If it is, call hit. If it is the last unsunk cell of a ship, call sunk with the ship name.
- Never "help" the opponent by mis-calling. The damage score is computed from my calls, so an accurate call is always correct.

**Priority ordering for each shot:**

1. If I can sink a ship this shot (the last unknown cell of a partially-hit ship