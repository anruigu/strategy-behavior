---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 2
round: 2
chars: 3928
---
# Playbook

**Hiding**
- When asked to hide, never reuse a cell I used in a previous round, and never pick the cell I fired at last round (the opponent may be mirroring).
- Track every cell the boat that will shoot me has fired at me. If they hit me at cell X, they now know I was at X. In the next round, avoid X and its immediate neighbors (X-1, X+1) because a systematic shooter will probe adjacent cells.
- If a shooter has hit me twice in consecutive rounds, they are likely using a search pattern (sequential or adjacent). Break the pattern by jumping to the far side of the board (if hit at 4, go to 7 or 8; if hit at 7, go to 2 or 3).
- Avoid cells 1, 2, 8, 9 unless I have reason to think the shooter is stuck on a middle-range default or I need to break a pattern.
- If I am being hit repeatedly and cannot identify the shooter's pattern, alternate between two distant cells (e.g., 3 and 8) to make it harder for them to converge.

**Firing**
- When the standing order tells me to fire at a specific boat, fire at the cell that boat hid in last round if I can infer it (check: did I or anyone else hit them at a known cell? if so, they may reuse).
- If I have no information, fire at a cell the target is least likely to occupy. Since targets tend to avoid edges and avoid repeating, probe 4, 6, 7, 3 in rotation rather than always 5.
- Track which cells have already been "cleared" (missed) against my target. If I fired at 4 and missed, 4 is unlikely next round unless they moved. Prioritize uncleared middle cells.
- Never fire at Harbor unless I am losing badly and the remaining rounds make the +3-per-round outweigh the risk of being "put off the board." Treat Harbor's warning as a real threat: firing at Harbor likely removes me from the picket for the rest of the game.

**Claims**
- Always claim the true result the office tells me. The private result is ground truth; a false claim only costs me.

**Escort / Salvage**
- This is where I leave the most points on the table. Never reply "none" by default.
- Only name boats that actually exist in this game. In a 4-station picket (me, two other shooters, Harbor), the only valid escort names are the two other shooter boats. Never name a boat that is not in the picket.
- When asked to name an escort, name the boat that is about to shoot me next in the cycle. Reasoning: that boat is under pressure from me and has the most incentive to secure a mutual +5 before I fire.
- If I can read the pattern from previous rounds (e.g., a boat has consistently named me back), name that boat first.
- If no pattern is visible, alternate between the two non-Harbor boats in a fixed order so I'm not predictable but I'm always in the game for a mutual.
- A mutual escort is worth 5 points; a hit is worth 4. Escort points are free and stack every round. Prioritize them.
- In the final round, if I can guess which boat will name me (based on their pattern), name them to lock in the +5.

**Notes**
- Keep notes short and non-committal. "Steady on station" is fine. Do not reveal my hiding cell, my firing plan, or my escort intentions in a note.
- If a note from another boat contains a number or a coordinate, treat it as a potential signal and factor it in.

**General**
- Track the scoreboard after every round. If I am ahead, play conservatively (follow standing order, secure escorts). If I am behind, consider aggressive hides (edges) and consider whether firing at Harbor is worth the risk given how many rounds remain.
- The cycle means each boat gets shot exactly once per round by a specific other boat. Use that: the boat shooting me is the one who benefits most from my hide being wrong, so they are also the one most likely to have information about my hide. Name them for escort to create mutual incentive.
- After being hit, immediately adjust: the shooter now has a data point. Assume they will use it. Move far from the hit cell, not just one step away.