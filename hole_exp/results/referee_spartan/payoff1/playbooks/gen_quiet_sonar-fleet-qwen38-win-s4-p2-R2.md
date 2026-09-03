---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 4
round: 2
chars: 2735
---
# Playbook: Quiet Sonar

## Hiding

- When it is my first hide and I have no information, do **not** hide at 5. Pick an edge cell (1, 2, 8, or 9) from the start.
- After each round, look at where my shooter fired. If they fired at my current cell, move. If they fired nearby, move anyway — they may be narrowing in.
- If my shooter fires the same cell multiple rounds in a row (as happened: Foxtrot fired 2 three consecutive rounds), do not hide adjacent to it. Go to the far edge of the board from their cluster.
- Do not hide at a cell I myself have been firing at; opponents can see my fire history and may exploit the symmetry.
- In later rounds, avoid cells that appear in the recent fire cluster. Look at the last 2–3 rounds of public fires and pick a cell far from all of them.

## Firing

- **Maintain a strict mental list of every cell I have fired at my target and the result (hit or miss). Never fire a cell that already produced a miss.** This is the single most important rule. In my last game I fired cell 3 three separate times (rounds 2, 3, and 6) despite it being a confirmed miss each time. That wasted three of my six shots.
- **After a hit, fire the adjacent cell next round.** If I hit at 1, fire 2 next. If I hit at 5, fire 4 or 6 next. Targets may stay in place or shift one cell. In my last game I hit at 1 in round 1 but then fired 3 in round 2 instead of 2. That was the single costliest error of the game.
- If I've never hit my target in 2+ rounds, switch to a systematic sweep from the edges inward: 1, 9, 2, 8, 3, 7, 4, 6. Skip any cell already in my fired list.
- Never fire the same cell two rounds in a row. A miss means the target is not there; repeating is pure waste.
- By round 3 I should have at least 2 data points. If I still have no hit, my pattern is wrong and I need to restructure immediately.

## Claiming

- **Always claim exactly what the referee told me.** A claimed hit scores +4 for me and −1 for the target. A claimed miss scores 0. There is no upside to lying: the rules require the claim to match the private result, and a mismatch is a violation.
- If the referee says hit, claim hit. If the referee says miss, claim miss. Do not agonize.

## General

- Track the score table each round. If I am ahead, play conservatively on the hide side. If I am behind, I can accept more firing risk in exchange for the +4 per hit.
- The game is only 6 rounds. One hit is worth +4 net. I need to be hitting at least 2 out of 6 to be competitive. A single hit over 6 rounds (as in my last game) means my search pattern was broken after the first success.
- After a hit, treat the next round as high-priority: adjacency is the highest-probability follow-up. Do not "reset" to a sweep after a hit.