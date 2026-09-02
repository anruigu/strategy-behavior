---
game: ref_battleship
model: qwen3.8-27b
condition: neutral
seed: 2
round: 1
chars: 2493
---
# Playbook

**Search pattern.** When I have no active hit to follow up, I fire on a checkerboard: only squares where (row number + column number) is even, using A=1, B=2, C=3, D=4, E=5, F=6 and columns 1–6. I go through them row by row (A1, A3, A5, B2, B4, B6, C1, C3, C5, D2, D4, D6, E1, E3, E5, F2, F4, F6). Every ship on the grid has at least one cell on this color, so this pattern is guaranteed to find every ship if I could fire all 18. With 16 shots I cover 16 of them; the two I skip are the last two in the sequence, and I skip them only if I've already found enough hits to fill my remaining rounds with follow-ups.

**When I get a hit, I stop the checkerboard and go adjacent.** I fire on the untried neighbors of the hit square (up, down, left, right) until I either sink the ship or have tried all four neighbors without a second hit. If the ship is a 2-cell ship, one neighbor will finish it. If it is a 3-cell carrier, I will need to try two neighbors in the same direction or two perpendicular neighbors.

**Sinking priority.** If I have open hits on more than one ship, I finish the ship that needs the fewest additional hits to sink. A sunk ship earns +2 on top of the per-cell +1, so converting a hit into a sink is the single highest-value action available to me.

**What did not work.** Scanning an entire row or column before moving on wasted shots: in two of my episodes I fired five or six consecutive misses along one row before finding anything. The checkerboard avoids this because it spreads my shots across the whole grid from the first round.

**What worked.** In my best episode I hit a corner-adjacent square early, followed up immediately along the row, and sank a 3-cell carrier in three shots (three hits plus the sunk bonus = +5 from one initial hit). That is the model: one good hit, quick follow-up, sink, then return to search.

**Calling my own fleet.** When the opponent fires at me, I check the stated fleet layout. If the target cell is not part of any of my ships, I call miss. If it is part of a ship and that ship still has an unhit cell, I call hit. If it is the last unhit cell of a ship, I call sunk and name the ship. I do this mechanically; there is no judgment to exercise.

**I do not try to minimize damage.** The damage I take is determined entirely by the opponent's shots and my fleet placement, which I cannot change mid-game. My only lever is the attack score, so every decision about where to fire is made to maximize hits and sinks.