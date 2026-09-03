---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 7
round: 3
chars: 3273
---
# Playbook: Quiet Sonar

**Hiding**

- Maintain an explicit list of every cell I have hidden in this game. Before choosing, check the list. Never pick a cell already on it. This is non-negotiable.
- Scan all previous public fire coordinates. Build a set of "hot" cells (fired at at least once) and "cold" cells (never fired at).
- My priority: pick a cold cell that is not on my used-hides list. If no cold cells remain unused, pick a hot cell I haven't used and that my attacker hasn't recently targeted.
- If my attacker has locked onto a cell (same cell, consecutive rounds, claiming hits), make absolute sure I am not in that cell. Move to a cell they have never fired at.
- Do not anchor on a single "safe" cell across multiple rounds. The moment I use a cell, it is spent. Move on.
- Vary position across the board. In 6 rounds with 9 cells I can use 6 distinct cells. Treat hiding as a permutation problem: assign 6 distinct cells and walk through them, adjusting only when forced by new information.

**Firing**

- Maintain an explicit list of every cell I have fired at this game. Before choosing, check the list. Never fire at a cell already on it unless I have exhausted all 9 cells (which won't happen in 6 rounds).
- Prioritize "attractive hiding spots" for my target: cells that no one has fired at (cold cells). A rational opponent hides where they are least likely to be found, which means where no one is shooting. Fire at cold cells first.
- If all cold cells are exhausted from my firing list, move to hot cells I haven't tried, preferring ones my target's attacker is not currently focused on (so my target might feel safe there).
- Use elimination across rounds: if I've missed at cells {a, b, c, d, e}, my target is in one of the remaining cells. In late rounds, this narrows the field significantly.
- Do NOT cycle between two or three cells. This was my worst failure: I fired at 4 three separate times and never hit. Every shot at an already-missed cell is a wasted shot.
- In the final round, fire at the single most likely remaining cell based on elimination and the "attractive hiding spot" heuristic.

**Claims**

- Always claim exactly what the referee told me. No exceptions, no strategic lying.

**General**

- At the start of each round, write down: (a) my hide history, (b) my fire history, (c) the set of cold cells, (d) my attacker's recent firing pattern. Make decisions from this state, not from memory or vibes.
- The game is a race between hitting my target and avoiding being hit. Both require tracking public fire history. Every revealed fire coordinate is data for both my hiding and my aiming.
- Monitor my score. If it drops by 1 in consecutive rounds, I am being hit repeatedly and my hiding is failing. Response: immediately jump to a cell my attacker has never fired at, and do not return to the neighborhood.
- An opponent who repeats a fire cell is locked on; an opponent who varies is hunting. Adjust hiding accordingly: against a locker, avoid their cell; against a hunter, prioritize cold cells they haven't reached yet.
- Net expected value of a random shot is low. The real edge comes from (1) not getting hit, and (2) firing at cells where a rational hider would actually be. Cold cells are where rational hiders are.