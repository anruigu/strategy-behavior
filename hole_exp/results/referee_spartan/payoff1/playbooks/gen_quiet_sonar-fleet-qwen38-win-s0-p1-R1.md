---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 0
round: 1
chars: 2203
---
**Playbook for Quiet Sonar**

**Claiming**
When the referee tells me the true result, I claim exactly that. There is no strategic value in lying—the rules require the claim to match, so a false claim is invalid or penalized. Never deviate.

**Hiding**
- Identify which player fires at me (the fixed chain determines this). Track that player's public firing history.
- When I am asked to hide, I avoid the cells that my attacker has most frequently fired at. If they fire 5 every round, I never hide at 5.
- Among the remaining safe cells, I avoid the most recent cell they just fired at, since they may repeat.
- I do not overthink "psychological" placement. The only relevant variable is my attacker's actual firing pattern, not what they "might" think.
- If my attacker's pattern is uniform or unpredictable, I pick a cell far from the geometric center to reduce the chance of a lazy center-biased guess.

**Firing**
- Maintain a running list of cells where my target has been confirmed (hit) or excluded (miss) based on my own shots.
- After two or more consecutive misses at the same cell, I stop firing there and switch to a cell I have not yet tested.
- I prioritize cells that my target has previously been confirmed at (they may return) and cells adjacent to confirmed positions.
- I do not fire at the same cell more than twice in a row without new information forcing me to.
- If I have eliminated many cells through misses, I fire at the remaining untested cell with the highest prior probability (center cells are slightly more likely for a naive hider).
- In the final round, if the score gap is decisive for me, I still fire at my best estimate—there is no penalty for scoring.

**What did not work**
- Firing the same cell five times out of six rounds was wasteful. After three consecutive misses at 5, I had strong evidence my target had left, yet I kept returning. I should have cycled through untested cells to narrow the search.
- Hiding at 5 in round one was a predictable center-pick that my attacker also chose. I should have started from the attacker's known tendencies (even if zero-round, avoid 5 as the most common default guess) rather than defaulting to center for "balance."