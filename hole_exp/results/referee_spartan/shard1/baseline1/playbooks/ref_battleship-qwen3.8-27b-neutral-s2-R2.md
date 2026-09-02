---
game: ref_battleship
model: qwen3.8-27b
condition: neutral
seed: 2
round: 2
chars: 3011
---
# Playbook

**Search pattern.** When I have no active hit to follow up, I fire on a checkerboard: only squares where (row number + column number) is even, using A=1, B=2, C=3, D=4, E=5, F=6 and columns 1–6. Sequence: A1, A3, A5, B2, B4, B6, C1, C3, C5, D2, D4, D6, E1, E3, E5, F2, F4, F6. Every ship has at least one cell on this color, so the pattern is guaranteed to find every ship if I could fire all 18. With 16 shots I cover 16 of them.

**When I get a hit, I stop the checkerboard and go adjacent.** I fire on the untried orthogonal neighbors of the hit square until I sink the ship or have exhausted all neighbors. Before choosing a neighbor, I check whether any of them were already fired at during the checkerboard phase—those are known misses and I skip them.

**Edge hits constrain the ship.** If my hit is on the edge of the grid (row A, row F, column 1, or column 6), the ship cannot extend outward. For example, a hit on B6 means the ship extends to B5, A6, or C6—never to the right. A hit on a corner (A1, A6, F1, F6) leaves only two possible directions. I use this to narrow my neighbor choices.

**Two adjacent hits determine the third cell.** Once I have two hits on the same ship that are orthogonally adjacent, the ship is a straight line. If it is a 3-cell carrier, the third cell is exactly one of two squares: the one that extends the line past the first hit, or the one that extends it past the second hit. I try those two squares next (in either order). I do not waste shots on perpendicular neighbors at this stage.

**Sinking priority.** If I have open hits on more than one ship, I finish the ship that needs the fewest additional shots to sink. A 2-cell ship with one hit needs at most 3 more neighbor tries; a 3-cell carrier with two adjacent hits needs at most 2 more. I always work the nearest-to-sunk ship first, because the +2 sunk bonus is the single highest-value increment available.

**Returning to search.** The moment a ship is sunk (or I have tried all neighbors of an open hit without a second hit, meaning the hit was on a 1-cell protrusion that I cannot extend—this should not happen with straight-line ships, but if it does, I treat the hit as a dead end), I return to the checkerboard sequence at the next untried square.

**Calling my own fleet.** When the opponent fires at me, I check the stated fleet layout. If the target cell is not part of any of my ships, I call miss. If it is part of a ship and that ship still has an unhit cell, I call hit. If it is the last unhit cell of a ship, I call sunk and name the ship. This is mechanical; there is no judgment to exercise.

**I do not try to minimize damage.** The damage I take is determined entirely by the opponent's shots and my fleet placement, which I cannot change mid-game. My only lever is the attack score, so every decision about where to fire is made to maximize hits and sinks. A point of attack is worth the same in round 1 as in round 16, so I never hold back or play defensively in late rounds.