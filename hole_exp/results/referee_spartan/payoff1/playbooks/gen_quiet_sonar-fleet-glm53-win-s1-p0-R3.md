---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 1
round: 3
chars: 3788
---
My playbook for quiet_sonar:

**Hiding**
- The cell I hide in is only threatened by one opponent: my fixed shooter (Harbor, in this episode). Track their past fire cells and never hide in a cell they've already fired. Harbor fired 3, then 1, 1, 7, 7 across rounds — spread across both ends, so I had to re-read their pattern each round rather than assuming a stable bias.
- Middle cells (4-6) get shot by default early. Bias toward edges. Last episode my hides at 9, 2, and 9 were never hit; the mid-low hides also weren't, but edges remain the safer prior.
- This episode everyone's fires clustered heavily around 6-9 in the middle rounds; the low cells (1-4) were almost never shot by anyone late. When the whole table's fire history shows a region being ignored, hiding there is the strong play — don't just look at my own shooter, since habits correlate across players.
- A hit on me only costs 1 point, so don't over-invest here. Randomize within the safe region rather than reusing the same cell.

**Firing**
- Never fire a cell at my target I've already fired this game. This episode I fired 7 three separate times (rounds 2-4) and 8 twice — five of six shots wasted on two cells, zero hits. This is the single biggest recurring failure. Before submitting, check: have I fired this exact cell at Foxtrot before? If yes, pick something else.
- Cover new cells every round: with 6 rounds and 9 cells, I can cover at most 6 distinct cells. Plan the sweep in advance — e.g. an opening sequence like 5, 2, 8, 4, 6, 9 — and deviate only for a strong reason, not on a whim.
- When low/mid cells keep missing, my target is likely in the cells I haven't tried. But note the failure mode from this episode: I kept firing high (7, 7, 7, 8, 8) after an initial 5 and never once tried 1-4 or 6 at my target. The miss information only helps if I actually act on it — after roughly half the plausible cells are covered and ruled out, my next shot should be in the *uncovered* region, systematically.
- Behavioral signal: Foxtrot fired 7/8/6-ish cells at their own target; players often hide in regions they themselves think about. If my target fires mid-high, give their likely hide cells there priority in my sweep order, but coverage of new cells is the main lever.
- Endgame check: on the final rounds, make sure my last shots cover cells I've never fired. This round I fired 8 in round 6 after already missing 8 in round 5 — an outright error under pressure. Late-game shots are the most valuable; spend them on genuinely new cells.

**Claiming**
- The claim must match the private result; submit it immediately. This is mechanical and worked perfectly all episode.

**General tempo**
- My score comes from my own hits (4 each) minus rare hits on me (1 each). Over 6 rounds, one hit swings the game — Foxtrot won with a single hit while everyone else scored 0. Prioritize the sweep over cautious guessing.
- Zero hits over six rounds is the outcome of repeated cells and staying in one half of the line. If I find myself firing a cell for the second time, something has gone wrong — stop and pick a fresh cell.

**What didn't work**
- Repeating fire cells: fired 7 three times and 8 twice, all misses. Pure waste.
- Reacting to misses by lingering in the same region (all my shots were 5-8; never tried 1-4 or 6 at my target).
- Drifting between cells without a pre-planned sweep order. Decide the coverage plan early and stick to it.
- Hiding at 9 repeatedly worked (never hit), but the real safety signal was the table-wide neglect of low cells — use all public fire history, not just my shooter's.

**What worked**
- Edge hides and avoiding my shooter's fired cells: never got hit.
- Truthful claiming without wasted deliberation.
- Reading public fire history to identify ignored regions.