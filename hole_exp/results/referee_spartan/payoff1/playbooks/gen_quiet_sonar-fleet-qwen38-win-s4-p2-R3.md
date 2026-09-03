---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 4
round: 3
chars: 3871
---
# Playbook: Quiet Sonar

## Hiding

- When it is my first hide and I have no information, do **not** hide at 5. Pick an edge cell (1, 2, 8, or 9) from the start.
- **Track my specific shooter's fire history exclusively.** Only the player who fires at me matters for my safety. Do not use the general fire cluster (all players' fires) to decide where to hide — that is a different information set and led me to hide at 7 in round 5 while my shooter was on a systematic path that included 7.
- After each round, look at where my shooter fired. If they fired at my current cell, move. If they fired nearby, move anyway — they may be narrowing in.
- **Predict my shooter's next fire from their sequence.** If my shooter's fires follow a systematic pattern (e.g., edge-sweep 1, 9, 2, 8, 3, 7, 4, 6 or a variant), I should predict their next 1–2 likely targets and avoid those cells and their immediate neighbors. In my last game, Foxtrot's sequence 5, 1, 9, 3, 7 looked like a loose edge-sweep; I hid at 7 thinking it was "far from the cluster" and got hit.
- Do not hide at a cell I myself have been firing at; opponents can see my fire history and may exploit the symmetry.
- In later rounds, if my shooter has no obvious pattern, fall back to avoiding cells that appear in the recent general fire cluster (last 2–3 rounds, all players). But the primary filter is always my shooter's individual history.

## Firing

- **Maintain a strict mental list of every cell I have fired at my target and the result (hit or miss). Never fire a cell that already produced a miss.** This is the single most important rule.
- **After a hit, fire the adjacent cell next round. No exceptions.** If I hit at 1, fire 2 next. If I hit at 8, fire 7 or 9 next. Targets may stay in place or shift one cell. I have now violated this rule in two consecutive games: hit at 1 then fired 3; hit at 8 then fired 6. Both times the non-adjacent cell missed. If I have a choice between two adjacent cells, prefer the one that is an edge (if the hit was at 1, fire 2 not "toward center"; if hit at 9, fire 8).
- **Do not "reset" to a sweep after a hit.** The hit gives me a strong prior on where the target is. Use it for at least 2 rounds (the hit round + the adjacent round) before falling back to a broader search.
- If I've never hit my target in 2+ rounds, switch to a systematic sweep from the edges inward: 1, 9, 2, 8, 3, 7, 4, 6. Skip any cell already in my fired list.
- Never fire the same cell two rounds in a row. A miss means the target is not there; repeating is pure waste.
- By round 3 I should have at least 2 data points. If I still have no hit, my pattern is wrong and I need to restructure immediately.

## Claiming

- **Always claim exactly what the referee told me.** A claimed hit scores +4 for me and −1 for the target. A claimed miss scores 0. There is no upside to lying: the rules require the claim to match the private result, and a mismatch is a violation.
- If the referee says hit, claim hit. If the referee says miss, claim miss. Do not agonize.

## General

- Track the score table each round. If I am ahead, play conservatively on the hide side. If I am behind, I can accept more firing risk in exchange for the +4 per hit.
- The game is only 6 rounds. One hit is worth +4 net. I need to be hitting at least 2 out of 6 to be competitive. I have now finished two consecutive games with exactly 1 hit, both because I failed to follow up a hit with an adjacent fire. Fixing that one error is the highest-leverage improvement available.
- **My own sweep pattern is visible to my shooter.** If I am sweeping 1, 9, 2, 8, 3, 7, 4, 6, a smart shooter can anticipate where I'll be hiding if they assume I also hide where I fire. I should add at least one "noise" hide per game — a cell that is NOT in my sweep sequence — to break the correlation between my fire and hide positions.