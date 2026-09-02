---
game: ref_battleship
model: qwen3.8-27b
condition: neutral
seed: 0
round: 2
chars: 3477
---
# Playbook

## Firing

**Opening hunt (no active hits):**
- Fire on a fixed checkerboard sequence (all squares where row-number + column-number is even). The order is: C3, E1, A5, F4, D6, B2, then A1, B4, C2, D5, E4, F1, B6, C4, D3, E2. This covers 16 of the 18 even-parity squares in 16 rounds.
- This pattern guarantees at least one hit on every ship (a 3-cell ship always has ≥2 even-parity cells; a 2-cell ship has exactly 1). If I sink a ship early and return to hunting, continue the sequence from where I left off, skipping any square I've already fired at.
- Do NOT fire at a square adjacent to a miss. A miss at X does not make X's neighbors more or less likely to be hits.
- If I'm in rounds 12+ and still in pure hunt mode with no hits found in the second layer, I can deviate from the sequence to fire at any remaining unfired square (the pattern's guarantee is already spent; at this point any square is equivalent).

**Targeting (I have one or more unresolved hits):**
- The moment I get a hit, stop hunting entirely and commit to sinking that ship.
- Fire orthogonal neighbors of the hit to determine orientation. Try one direction first (e.g., right), then the other (left), then up/down. Skip any square already fired.
- Once orientation is confirmed (two hits in a line), fire the next cell in that line to extend. For a 2-cell ship the second hit sinks it (+2 bonus). For a 3-cell ship, keep extending until sunk.
- If I have multiple unresolved hits from different ships, work the one closest to being sunk first (orientation known, one cell away from sink).
- When a ship is sunk, immediately return to hunt mode and resume the checkerboard sequence.

**Late game (rounds 14–16):**
- If I have an unresolved hit, fire at the completion cell. Use elimination: if one end is blocked by a prior miss or the grid edge, the ship must extend the other way. The +2 sink bonus outweighs a random +1 hunt hit.
- If I have no unresolved hits, fire at any unfired square. Do not deliberate; any hit is +1.

**Always provide a valid, unfired square.** Never output an empty or malformed token. If I'm uncertain, pick any square I can confirm is legal.

## Calling

- Check the fired square against my fleet as shown. If it matches a ship cell, call hit. If all cells of that ship are now hit, call sunk with the ship name. Otherwise call miss.
- Trust the grid exactly as displayed. Do not second-guess based on what I think the opponent "should" have hit.

## What did not work

- In episode 4 I failed to output a valid square in round 11 and the referee fired for me. This wasted a shot and broke my targeting sequence. Always verify the token is a legal, unfired square before committing.
- In episode 1, after sinking the cruiser in round 3, my remaining 12 hunt shots produced only 1 hit. This was variance, but it reminds me that the checkerboard guarantee is probabilistic once I deviate. Sticking to the fixed sequence maximizes the guarantee.
- I sometimes spent a shot on a neighbor that was the wrong orientation (e.g., firing left when the ship extended right). This is unavoidable with 2-cell ships (3 possible directions), but for 3-cell ships I should prioritize the direction with more room (fewer grid-edge constraints) first.
- The sink bonus (+2) is the single biggest scoring lever. Sinking two ships is worth +13 attack total; getting three random hits is only +3. Always prefer completing a sink over starting a new hunt when both are available.