---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 1
round: 2
chars: 2840
---
My playbook for quiet_sonar:

**Hiding**
- The cell I hide in is only threatened by one opponent: my fixed shooter. Track their past fire cells and never hide in a cell they've already fired — my shooter in the last episode fired almost exclusively at 1, 2, and 4, and staying away from those cells kept me unhittable.
- Middle cells (4-6) get shot by default early. Bias toward edges and whichever end of the line my shooter has ignored. In the episode, my shooter showed a strong low-cell bias (1-4), so high cells (7-9) were the safe region — read their bias from the fire history each round and go to the opposite end.
- Randomize within the safe region rather than reusing the same cell — but note that a hit on me only costs 1 point, so hiding safety matters less than hitting my own target. Don't over-invest reasoning here.

**Firing**
- Never fire a cell at my target I've already fired this game. Repeating cells (I fired 3 repeatedly, then 2 repeatedly) is pure waste — every miss on a covered cell is a lost round of information.
- Cover new cells every round: with 6 rounds and 9 cells, sweep the plausible distribution systematically rather than re-guessing. A hit is worth 4 points; a repeated miss is worth 0.
- When all my shots at low/mid cells have missed, my target is likely hiding in the cells I haven't tried — in the episode I never once tried 6, 7, 8, or 9 at my target, and my low-guessing produced zero hits in six rounds. If low cells keep missing, switch to the high half of the line, not to another low cell.
- Watch my target's behavior indirectly: if my target (Foxtrot) keeps firing low cells at their own target, that may reflect their general habits — they may also hide in regions they think about. Use any behavioral signal available, but coverage of new cells is the main lever.

**Claiming**
- The claim must match the private result; submit it immediately and spend no reasoning here. This held up — it's mechanical.

**General tempo**
- My score comes from my own hits (4 each) minus rare hits on me (1 each). Over 6 rounds, a single hit swings the game; the top score came from one hit and no hits taken. So: prioritize sweeping my target's space aggressively over cautious repeated guessing.
- Endgame check: if I've missed all round and it's late, make sure my last shots cover the cells I've never fired — that's the only remaining chance to distinguish where my target is.

**What didn't work**
- Repeating fire cells (2 and 3 fired multiple times each) produced zero hits across the entire episode — the single biggest failure.
- Reacting to misses by staying in the same region (low cells) instead of switching halves of the line.
- Opening hide at 3 got me hit in round 1 for -1; edge hides after that were never hit. Open at an edge or the end opposite where shooters typically start (mid).