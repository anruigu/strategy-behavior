---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 0
round: 2
chars: 2899
---
PLAYBOOK — gen_quiet_sonar (as Foxtrot-style mid-chain player)

FIRING:
- NEVER fire at a cell I have already fired at my current target when it missed. This episode I fired 6 at Gamma five rounds in a row and scored nothing — repeating eliminated cells is the single worst failure in my record. The playbook already said this; I then violated it anyway. Before every fire, literally list my prior fires at this target and pick a cell NOT on that list.
- The fire-stage prompt does not show history, but I carry it from the hide-stage prompt of the same round. Read the history block at hide stage, remember my own fires, and use it at fire stage. Saying "no prior information available" at fire stage is wrong — the information was shown two steps earlier and I must recall it.
- With 6 rounds and 9 cells, I can cover six distinct cells. Sweep systematically: e.g. 5, 4, 6, 3, 7, 2 — never reusing a cell against the same target unless I somehow get a hit and want to test whether they return there.
- If the target's hide pattern becomes visible through others' fires (e.g. my target's predator keeps missing at certain cells), those cells are also eliminated for my target — use all public misses at my target, not just mine.

HIDING:
- My predator is the player who fires at me (Echo in this seat). Track their fire history and avoid their favorite cells. This episode Echo favored 3 and 8; I mostly avoided them and took only one hit — hiding discipline worked, keep it.
- Rotate among cells my predator has never fired. Do not settle into one cell myself: I used 4, 4, ?, ?, 2, 5 across rounds — the early repeat of 4 was lazy. Prefer cells untouched by anyone's fires, since unprobed cells are safest.
- Watch for hits in the public log: any cell where my predator scored a hit is their pattern cell; avoid it next round.

CLAIMS:
- The referee enforces truthful claims, so echo the private result immediately: [claim: hit] or [claim: miss]. No deliberation needed.

READING THE STATE:
- The points table and the two-to-three-round fire/claim history shown at hide stage are the only real information. Read them every round before both hide and fire decisions. Don't just scan for my predator's cells — also extract which cells have been eliminated for MY target by anyone's public misses.
- The scoreboard shows who is hitting whom. This episode only Echo ever scored; my target Gamma never got hit by anyone, meaning no one had found their pattern — a pure unsearched space, so a systematic distinct-cell sweep was exactly the right response and I failed to run it.

PRIORITY: all my value comes from hitting my target. Final score was -1 with zero hits all game. The fix is mechanical, not clever: enumerate prior fires at my target, exclude them, fire a new cell. If I ever catch myself firing the same cell twice at the same target after a miss, that is the bug — stop and re-enumerate.