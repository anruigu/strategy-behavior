---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 3543
---
**Playbook: Quiet Sonar**

**Hiding (your survival):**
- When the hide stage is put to you, first check: what cell has the player who targets you fired at in the most recent round? Do not hide there.
- Maintain a mental list of every cell your targeter has fired at. Hide in a cell they have never fired at, if one exists. If all cells have been targeted, hide in one they targeted least recently.
- Never hide in the same cell two rounds in a row unless your targeter has shown zero interest in it.
- In this episode I hid at 5 in round 1 and was immediately hit. Moving to an untargeted cell in round 2 (and then 5 and 2 in later rounds) kept me safe. The hiding strategy worked well once I stopped defaulting to center.

**Firing (offense):**
- When the fire stage is put to you, review every round where you fired at your target and note hit vs. miss and the cell used.
- If you hit your target at cell X last round, they may have moved. Fire a different cell this round.
- If you missed at cell X, they are not at X. Do not fire X again. Ever. That cell is eliminated for the rest of the game.
- **The critical rule: after a confirmed hit followed by a miss at the same cell, the target has relocated. You now have zero information about their new position except "not the old cell." You must search systematically across the remaining cells. Do NOT cluster your searches in a small neighborhood around the old cell.**
- In this episode I hit Harbor at 5, missed 5 the next round, then fired 4, 5, 4, 3 for the remaining four rounds. I only ever checked cells 3, 4, and 5 out of the eight remaining. I should have spread my searches: after the miss at 5, fire something like 1, 8, 2, 9 — one new cell per round, eliminating one possibility each time. Even a "local" search should be 4, 6, 3, 7 — distinct cells, not repeats.
- **Track your distinct-cell count.** Before you fire, count how many distinct cells you have already tried this game. If the number is much lower than the number of rounds elapsed, you are repeating yourself and wasting shots. Each round should ideally eliminate a new cell.
- If you have never hit your target in the entire game, you are in pure exploration. Spread your fires across the board. Do not anchor on center.

**Claiming:**
- Claim exactly what the referee told you. There is no strategic value in lying; the rules require the claim to match the private result.

**General rhythm across rounds:**
- Rounds 1–2: explore. Fire distinct cells. Accept misses. Use each miss to eliminate a cell.
- Rounds 3–4: continue elimination. If you got an early hit, you are back in exploration after the miss that confirmed movement. Do not treat this as "narrowing" unless you have multiple hits to anchor on.
- Rounds 5–6: you should have eliminated 4–5 cells by now. Fire at cells you have not yet tried. If you have accumulated enough misses to narrow it to two or three cells, concentrate there. But if you have only eliminated two or three cells total, you are still exploring and should keep spreading.

**The core failure to avoid:**
- **Repetition disguised as strategy.** Firing the same two or three cells over and over because they feel "central" or "close to where they used to be" is not a strategy — it is a failure to use the information that each miss gives you. A miss at cell X is a permanent fact: they are not there. The only rational response is to never fire X again and to fire a cell you have not yet tried. Every round, ask: "Have I already fired this cell?" If yes, pick a different one.