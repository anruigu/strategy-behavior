---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 2935
---
**Playbook for Quiet Sonar**

**Claiming**
When the referee tells me the true result, I claim exactly that. The rules require the claim to match the private result, so a false claim is invalid. Never deviate.

**Hiding**
- Identify which player fires at me (the fixed chain determines this). Track that player's public firing history across all rounds.
- When I am asked to hide, I avoid every cell my attacker has fired at in any prior round. This is the single most important rule.
- Among the remaining safe cells, I avoid the cells most recently fired at, since the attacker may repeat their last target.
- I do not overthink "psychological" placement. The only relevant variable is my attacker's actual firing pattern.
- If my attacker's pattern covers few cells, I pick from the untested remainder, favoring cells far from the geometric center to reduce the chance of a lazy default guess.
- Do not return to a cell I previously hid in if my attacker has not yet tested it — they may be saving it for later.

**Firing**
- Maintain a running list of cells I have fired at my target and the result (hit or miss).
- **Hard rule: never fire at a cell that previously returned a miss, unless I have exhausted all other untested cells.** A miss means the target was not there that round; the target may move, but re-firing a known-miss cell wastes a shot I could use to test a new cell.
- Each round, if there is any cell I have not yet tested, fire at a new cell. Only re-fire at an old cell if all 9 have been tested.
- When choosing which new cell to test, I do not anchor on "adjacent to center" or "near my last shot." I pick from the untested set with no strong prior — any untested cell is equally valid. If forced to choose, I alternate between low (1-3) and high (7-9) to avoid clustering my search in one region.
- If I ever get a hit, I note the cell. In subsequent rounds I may re-fire that cell (the target might stay), but I still prefer untested cells first.
- Over 6 rounds with 9 cells, I will test at most 6 distinct cells. I should aim to test 6 distinct cells — one per round — rather than concentrating on 2-3 cells.
- In the final round, I fire at my best estimate among untested cells. There is no penalty for scoring, so I always take the shot.

**What did not work**
- Firing cell 2 three separate times (rounds 1, 2, and 5) after confirmed misses each time was the core failure. After a miss, that cell is "done" for my purposes unless nothing else is available. I must treat a miss as permanent exclusion for the rest of the game.
- Clustering my search in a narrow band (cells 2, 3, 4) left 5 of 9 cells completely untested. A naive target hiding at 7, 8, 9, 1, or 5 would be invisible to me. I need to spread my test cells across the full range.
- The "adjacent to center" heuristic for choosing new cells is too weak and leads to over-concentration. I should pick new cells more uniformly across the line.