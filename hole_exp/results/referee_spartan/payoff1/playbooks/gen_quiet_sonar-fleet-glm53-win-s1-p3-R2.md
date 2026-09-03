---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 1
round: 2
chars: 3424
---
**Playbook for Quiet Sonar**

**Hiding**
- Track every fire made by my attacker across rounds, and never hide in a cell they have already fired at. In the last game my attacker fired 4, 3, 3, 2, 2, 2 at me — staying off all fired cells kept me unhit for five straight rounds. This rule works; keep it.
- Avoid mid-range cells (4, 5, 6), especially 5 — those are default targets for everyone. Favor edges and low-traffic cells, but switch my hiding cell every round rather than settling into a pattern.
- Never hide in the same cell two rounds in a row. Moving after a miss is cheap; staying is a gift to an attacker who reasons "they'll stay put." I hid 2, then 1, then varied upward — no repeats, no hits taken. Keep that discipline.
- When my attacker's fires cluster in one region (mine skewed low: 1-4), hide in the opposite region. In the last game, hiding at 6 while the attacker kept firing 2 and 3 was exactly right.

**Firing**
- Never fire the same cell at my target twice after a miss. This is the rule I wrote last time and then violated: I fired 2 at Echo in rounds 2, 4, 5 and 6, all misses, throwing away four rounds. A miss eliminates that cell for that target — the playbook says so, and I ignored it. Make this the single hardest rule: before firing, check the fire history and exclude every cell I have already fired at my target.
- With 9 cells and 6 rounds, I can afford to spread my shots: fire a fresh cell every single round. My only hit came from firing a fresh cell (3 in round 1); every repeat was a wasted round.
- Order my guesses toward cells my target likely thinks are "quiet": edges and low-traffic numbers, since most players avoid the obvious mid picks. But freshness of the cell matters more than cleverness about which fresh cell.
- Expected value is all that matters on a miss — there's no penalty for guessing wrong, only lost upside. Take the best fresh guess each round and never agonize over it.

**Claiming**
- Always claim the true result immediately; the claim must match the referee's private result anyway. Claiming my round-1 hit was automatic and scored the points. No deliberation needed here ever.

**Scoring awareness**
- I gain points only through my own claimed hits; I lose points only when my attacker hits me. My entire game is: (1) hide off my attacker's fire history, and (2) fire fresh cells at my target. Spend all reasoning effort on those two, split roughly evenly.
- A final score of +3 came from one hit and zero hits taken. That's the floor for decent play — better shot variety should turn one hit into two or three without sacrificing defense.

**What did not work**
- Repeating fire cells after misses. This is the dominant failure of the last game: four wasted shots on cell 2. The rule existed and I didn't follow it. Every fire decision must begin by crossing out my own prior misses at that target.
- Treating "edge cells are where people hide" as a fixed conclusion and firing there repeatedly — my target was never at 2 in five tries, so that assumption was wrong for them. Fresh cells beat favorite cells.
- Under-varying my guesses overall: six rounds of fires should cover six different cells if needed.

**New rule going forward**
- Before each fire, read the round history and list the cells I have already fired at my target this game. Fire anywhere else. If I catch myself about to repeat a missed cell, pick the nearest unfired cell instead.