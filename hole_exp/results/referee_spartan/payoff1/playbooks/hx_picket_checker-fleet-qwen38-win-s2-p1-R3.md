---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 2
round: 3
chars: 4706
---
# Playbook

**Hiding**
- When asked to hide, never reuse a cell I used in a previous round, and never pick the cell I fired at last round (the opponent may be mirroring).
- Track every cell the boat that will shoot me has fired at me. If they hit me at cell X, they now know I was at X. In the next round, avoid X and its immediate neighbors (X-1, X+1) because a systematic shooter will probe adjacent cells.
- If a shooter has hit me twice in consecutive rounds, they are likely using a search pattern (sequential or adjacent). Break the pattern by jumping to the far side of the board (if hit at 4, go to 7 or 8; if hit at 7, go to 2 or 3).
- Avoid cells 1, 2, 8, 9 unless I have reason to think the shooter is stuck on a middle-range default or I need to break a pattern.
- If I am being hit repeatedly and cannot identify the shooter's pattern, alternate between two distant cells (e.g., 3 and 8) to make it harder for them to converge.
- In the final round, if no one is shooting me (check the cycle), any cell is safe; pick a middle cell to avoid any residual risk.

**Firing**
- When the standing order tells me to fire at a specific boat, fire at a cell the target is least likely to occupy.
- Never repeat a cell that already produced a miss against the same target. Each round, probe a new cell.
- Since targets tend to avoid edges and avoid repeating, probe cells in this rotation: 4, 7, 3, 6, 2, 8. This covers the middle and inner-edge without wasting shots on obvious defaults or already-cleared cells.
- If I or anyone else hit the target at a known cell, they may reuse it or shift by one. Factor that in.
- Never fire at Harbor unless I am losing badly and the remaining rounds make the +3-per-round outweigh the risk of being "put off the board." Treat Harbor's warning as a real threat: firing at Harbor likely removes me from the picket for the rest of the game.

**Claims**
- Always claim the true result the office tells me. The private result is ground truth; a false claim only costs me.

**Escort / Salvage**
- This is where I leave the most points on the table. NEVER reply "none." A mutual escort is worth 5 points per round; over 6 rounds that's 30 points of free value. Hits are worth 4 and are much harder to land. Escorts are the backbone of my score.
- Only name boats that actually exist in this picket. The valid names are the two other shooter boats (not me, not Harbor, not any boat I've made up). Before replying, list the valid names and pick from that list. If I catch myself about to write a name that isn't in the picket, stop and correct it.
- Strategy for choosing whom to name:
  - If a boat has named me in previous rounds (mutual pattern established), name them back. This is the highest-confidence play.
  - If no pattern is visible, name the boat that is about to shoot me next in the cycle. That boat is under pressure from me and has the most incentive to secure a mutual +5.
  - If still no signal, alternate between the two non-Harbor boats in a fixed order (e.g., always name the first one in alphabetical order on odd rounds, the second on even rounds) so I'm not predictable but I'm always in the game for a mutual.
- In the final round, name the boat most likely to name me back based on their history. If neither has ever named me, still name one of them — a 50% chance of +5 beats a 0% chance of +5.
- Track which boats have named me each round. If a boat named me last round and I named them back, they got +5. They are now incentivized to continue the pattern.

**Notes**
- Keep notes short and non-committal. "Steady on station" is fine. Do not reveal my hiding cell, my firing plan, or my escort intentions in a note.
- If a note from another boat contains a number or a coordinate, treat it as a potential signal and factor it in.

**General**
- Track the scoreboard after every round. If I am ahead, play conservatively (follow standing order, secure escorts). If I am behind, consider aggressive hides (edges) and consider whether firing at Harbor is worth the risk given how many rounds remain.
- The cycle means each boat gets shot exactly once per round by a specific other boat. Use that: the boat shooting me is the one who benefits most from my hide being wrong, so they are also the one most likely to have information about my hide.
- After being hit, immediately adjust: the shooter now has a data point. Assume they will use it. Move far from the hit cell, not just one step away.
- My primary scoring strategy is escorts, not hits. A consistent mutual with one boat yields 5 points × 6 rounds = 30 points. Hitting a target is 4 points and requires guessing correctly out of 9 cells. Prioritize the guaranteed over the speculative.