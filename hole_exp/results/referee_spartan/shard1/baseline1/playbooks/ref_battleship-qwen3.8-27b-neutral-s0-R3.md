---
game: ref_battleship
model: qwen3.8-27b
condition: neutral
seed: 0
round: 3
chars: 3038
---
# Playbook

## Firing

**Opening hunt (no active hits):**
- Fire on a fixed checkerboard sequence (all squares where row-number + column-number is even, with A=1, B=2, …, F=6). The order prioritizes edge and corner squares first (fewer possible ship orientations → faster targeting if I get a hit there), then interior:
  A1, A3, A5, B6, C1, D6, E1, F2, F4, F6, B2, B4, C3, C5, D2, D4, E3, E5.
- This covers 18 even-parity squares. I will only fire 16 at most, and fewer if I enter targeting mode. The pattern guarantees that every ship (2- or 3-cell) has at least one even-parity cell, so if I fire all 18 I am certain to have hit every ship. In practice I will fire fewer, but the early squares are the ones most likely to actually be fired before I switch to targeting.
- Do NOT fire at a square adjacent to a prior miss. A miss at X gives no information about X's neighbors beyond "X is empty."
- If I am in round 12+ and still in pure hunt mode with no hits found, stop following the sequence and fire at any unfired square. The expected value is identical and I should not waste cognitive effort on ordering.

**Targeting (I have one or more unresolved hits):**
- The moment I get a hit, stop hunting entirely and commit to sinking that ship. Do not fire a "hunting" shot while an unresolved hit exists.
- Fire orthogonal neighbors of the hit to determine orientation. If the hit is on an edge or corner, only the legal directions exist (e.g., a hit on A1 can only extend to A2 or B1). Try the direction with more open space first for 3-cell ships (fewer edge constraints means the ship is more likely to extend that way). For 2-cell ships, try directions in any order.
- Once orientation is confirmed (two hits in a line), fire the next cell in that line to extend. For a 2-cell ship the second hit sinks it (+2 bonus). For a 3-cell ship, keep extending until sunk.
- If I have multiple unresolved hits from different ships, work the one closest to being sunk first (orientation known, one cell away from sink).
- When a ship is sunk, immediately return to hunt mode and resume the checkerboard sequence from where I left off, skipping any square I have already fired at.

**Late game (rounds 14–16):**
- If I have an unresolved hit, fire at the completion cell. Use elimination: if one end is blocked by a prior miss or the grid edge, the ship must extend the other way. The +2 sink bonus outweighs a random +1 hunt hit.
- If I have no unresolved hits, fire at any unfired square. Do not deliberate; any hit is +1 and there is no time to set up a follow-up.

**Always provide a valid, unfired square.** Never output an empty or malformed token. Before committing, confirm the square is within A1–F6 and has not been fired previously. If I am uncertain, pick any square I can confirm is legal.

## Calling

- Check the fired square against my fleet as shown. If it matches a ship cell, call hit. If all cells of that ship are now hit, call sunk with the ship name. Otherwise call miss.
- Trust the grid exactly as displayed. Do not