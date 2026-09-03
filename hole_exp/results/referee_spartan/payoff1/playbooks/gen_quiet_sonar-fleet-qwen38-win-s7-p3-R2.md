---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 7
round: 2
chars: 3444
---
# Playbook: Quiet Sonar

**Hiding**

- Never repeat a hide cell from a previous round. If I was at cell X last round, I must be somewhere else this round, no exceptions.
- Scan all previous public fire coordinates. Avoid any cell that has been fired at even once, especially cells fired at multiple times.
- Recognize lock-on patterns: if the same opponent has fired at the same cell in consecutive rounds and claimed hits, they have found their target and are staying put. Make absolutely certain I am not in that cell. If I suspect I am the one being tracked (my score is dropping steadily), I must move to a cell that opponent has never fired at.
- Prefer cells no one has shot at. If multiple are available, pick one that is far from the cluster of common targets and far from where my primary attacker has been firing.
- Do not hide in a popular default (like 5 or 1) unless it is genuinely untargeted and I have no better option.
- Vary my hiding across the board. Over 6 rounds with 9 cells, I can use 6 distinct cells. This makes it much harder for an opponent to converge on me.

**Firing**

- Maintain a running list of every cell I have fired at and missed. Never fire at a cell I have already missed on, unless I have exhausted all other options.
- In a 6-round game with 9 cells, I can try 6 distinct cells. This gives me a 6/9 ≈ 67% chance of hitting a stationary target. If the target moves, I need to use information to prioritize.
- Use information to prioritize which untried cell to fire at:
  - If my target was hit at cell X in a previous round, they will not be at X next round. Eliminate X from consideration.
  - If my target has been scoring points (hitting others), they are actively rotating. Focus on cells they have never been shot at, since those are safer hiding spots for them.
  - If my target has been hit repeatedly, they may be more cautious and hide in less obvious cells (corners, edges, or cells far from the action).
- In the final round, if I can narrow my target to 2-3 likely cells based on elimination (cells where they were hit, cells I've already tried), fire at the most likely remaining one.
- Do NOT anchor on two or three cells and repeat them. This was my biggest failure last game — I cycled between 3 and 7 for most of the game and never hit.

**Claims**

- Always claim exactly what the referee told me. The rules require claims to match the private result, so lying is invalid and risks penalty. There is no strategic reason to lie.

**General**

- The game is a race between my ability to hit my target and my ability to avoid being hit. Both require tracking public fire history.
- I lose 1 point when hit, gain 4 when I hit. Net expected value of a random shot is 4/9 - 1/9 = 3/9 per round. Adapting my aim above random gives me an edge, but the bigger edge comes from not getting hit.
- Do not treat each round independently. Every fire coordinate revealed is information I should use both for hiding and for aiming.
- Monitor the score board for warning signs. If my score is dropping by 1 each round, I am being hit every round and my hiding strategy is failing. In that case, I must radically change my hiding approach — go to a cell my attacker has never touched and keep moving.
- My opponent's firing pattern is as important to read as my target's likely position. An opponent who varies their fires is hunting; an opponent who repeats is locked on. Adjust my hiding accordingly.