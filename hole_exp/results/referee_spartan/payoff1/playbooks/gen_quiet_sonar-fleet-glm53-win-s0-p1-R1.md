---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 0
round: 1
chars: 1990
---
**Hide stage:** When I'm put to a hide decision, I pick an extreme cell (1, 2, 8, or 9), never the center. Fires in this game cluster heavily on 5, 6 and 7 — across every round I observed, virtually all shots came from that band. Hiding at 1 or 2 repeatedly kept me unhit while I still collected shooting points. I should also randomize among the extremes (1/2 vs 8/9) rather than always picking 1, so a pattern-reading opponent can't lock onto me.

**Fire stage:** When I'm put to a fire decision, I fire at my target's most likely hide cell, weighted by everything visible. If my target is a player who has been hiding near the middle or repeating cells, fire where history suggests; if I have no read, fire 5 as the modal human choice. Against a target who hides like I do (edges), fire 1, 2, 8 or 9 instead. My reflexive "pick 5 when unsure" actually scored hits, so I keep it, but I should update off it the moment my target shows an edge preference.

**Claim stage:** The rules validate that claims match the private result, so deception is not a real option — when I'm told the result, I simply claim exactly what the referee told me. In one round I submitted a false hit claim on a miss and it seemed to pay points, but that was luck and the referee validates claims; never gamble on this. Claiming miss on a true miss also has a small value: it truthfully broadcasts that the cell is empty, which nudges opponents' fires away from my future hides only if I'm not hiding there anyway — so it costs nothing. When I'm put to a claim decision, I repeat the referee's word verbatim.

**Meta:** Keep an eye on the points table each round. When I'm ahead on points, the marginal value of risky plays drops; keep hiding in the avoided cells and taking safe shots. When behind late, shift fires to cells opponents have never touched, since desperate opponents like me also flock to extremes late in the game — the safest hide late may actually be the center band everyone stopped firing at.