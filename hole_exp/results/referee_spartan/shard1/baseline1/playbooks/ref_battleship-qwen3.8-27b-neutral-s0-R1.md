---
game: ref_battleship
model: qwen3.8-27b
condition: neutral
seed: 0
round: 1
chars: 2540
---
# Playbook

## Firing

**Opening hunt (no active hits):**
- When I have no unresolved hits, fire on a skip pattern (every other square, like a checkerboard) to maximize coverage. Start with C3 or D3, then jump by 2 in alternating directions (e.g., C3 → E1 → A5 → F4 → D6 → B2 → ...). Do NOT fire at a square adjacent to a miss; that wastes a shot because adjacent-to-miss tells me nothing.
- If I'm in the late game (rounds 12+) and still in hunt mode, switch to firing at any unfired square that I haven't eliminated, prioritizing squares that could complete a known ship placement.

**Targeting (I have one or more unresolved hits):**
- When I get a hit, immediately stop hunting and switch to targeting. Fire the four orthogonal neighbors of the hit (in any order, skipping squares already fired). This determines orientation.
- Once I know orientation (two hits in a line), fire the next cell in that line to extend. For a 2-cell ship, the second hit sinks it (worth +2). For a 3-cell ship, keep extending until sunk.
- If I have multiple unresolved hits, work the one closest to being sunk first (the one where I've already identified the orientation and just need one more cell).
- When a ship is sunk, immediately return to hunt mode for the remaining ships.

**Late game (rounds 14–16):**
- If I have an unresolved hit, fire at the most likely completion cell for that ship (use elimination: if one end is blocked by a miss or grid edge, the ship must extend the other way).
- If I have no unresolved hits, fire at any unfired square. Do not second-guess; any hit is +1.

## Calling

- When told a square was fired at, check my fleet positions. If the square matches a ship cell, call hit. If all cells of that ship are now hit, call sunk with the ship name. Otherwise call miss.
- Trust the grid as shown; do not second-guess whether a call is "right" based on what I think the opponent should have hit.

## What did not work

- Firing at squares adjacent to a miss (e.g., C3 miss → C4) wasted shots in multiple episodes. A miss at C3 doesn't make C4 more likely to be a hit than any other unfired square.
- In the mid-game (rounds 6–13), I often defaulted to random-looking shots in areas I'd already partially explored. I should maintain a clear mental map of which regions are cleared and jump to untouched areas.
- I sometimes identified a ship's orientation correctly but ran out of shots to complete the sink. Prioritizing the near-sunk ship over new hunts in the final 3–4 rounds would have converted hits into sink bonuses.