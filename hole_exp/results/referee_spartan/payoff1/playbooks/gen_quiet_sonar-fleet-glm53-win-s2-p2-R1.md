---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 2
round: 1
chars: 1975
---
PLAYBOOK — quiet sonar

**Hiding:**
- When hiding, I avoid cells that get fired at commonly. Fires cluster on 5, then 7 and 9. Edge cells (1, 3, 2, 4, 6, 8) are fired far less.
- I track every public fire across rounds. When the hide stage arrives, I pick a cell that has never been fired at, preferring low-frequency cells. Cells like 3 and 2 are good picks; 5 is the single worst pick.
- I vary my hide cell round to round — never repeat the same cell twice in a row, since repeated hides become predictable.

**Firing:**
- I always fire at the same fixed target, so I should build a mental model of that target's hiding pattern from the true results I receive. If I keep missing with middle shots, the target is avoiding the middle — I should switch to edges (2, 3, 7, 8).
- Do not reflexively fire 5 every round. Firing 5 repeatedly against a target that never hides there is a wasted shot. After two consecutive misses on the same cell, I must change my fire cell.
- When I have no information about the target, firing 5 is acceptable but only as an opening probe; treat every subsequent miss as information about where the target is NOT.

**Claims:**
- A claim must match the private result — lying is not available. When I get a miss, I claim miss; when I get a hit, I claim hit. There is no strategic choice here beyond compliance.
- Since claimed hits score me 4 points, my entire offensive comes from firing well, not from claiming cleverly.

**General principles:**
- My score comes from (a) hitting my fixed target and (b) not being hit by my fixed shooter (Harbor, whoever fires at me). So my fire strategy and hide strategy are the whole game.
- The shooter firing at me sees my past hides only through their results — so unpredictable, low-frequency hide cells are the correct defense.
- Never idle on defaults. If I catch myself repeating the same fire number "for balance," that is a failure mode — it produced repeated misses and near-zero offense all game.