---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 1
round: 3
chars: 2384
---
# Playbook for Quiet Sonar

**Hiding:**
- Identify who fires at me specifically (my attacker). Track every cell my attacker has fired at, round by round. Hide in a cell my attacker has NOT yet fired at this round, and ideally has not fired at frequently.
- Do NOT use general game-wide fire statistics to choose my hide cell. Only my attacker's shots matter for my survival.
- Keep a running list of every cell I have hidden at this game. Never repeat a cell from that list. If I am about to pick a cell I've already used, stop and pick a different one.
- If my attacker has a visible pattern (e.g., cycling through low numbers), hide outside that range.
- Prefer cells far from the center of the board (1, 2, 8, 9) when safe, since most attackers probe center first.

**Firing:**
- My fixed search order is: 5, 1, 9, 3, 7, 2, 8, 4, 6. I follow this order every game. If a cell in the order has already been fired at (miss or hit), I skip it and move to the next untried cell in the order.
- Before each fire decision, explicitly list: (a) every cell I have already fired at this game, (b) the next untried cell in my search order. Fire at (b).
- Never fire at a cell I have already fired at. This is non-negotiable. A repeated cell gives zero new information and wastes my only shot of the round.
- If I ever get a hit, my target was at that cell that round. Next round, resume my search order from the next untried cell. The target may have moved.
- Do NOT deviate from the search order based on intuition, "spreading," or "covering the center." The order already handles all of that.

**Claiming:**
- Always claim exactly what the referee told me. No exceptions, no strategic deviation.

**General:**
- Before each hide decision, explicitly list: (a) cells my attacker has fired at, (b) cells I have already hidden at this game, (c) safe untried cells. Pick from (c).
- Before each fire decision, explicitly list: (a) cells I have already fired at, (b) next cell in search order not in (a). Fire at (b).
- If I find myself about to repeat a previous action (same fire cell or same hide cell), stop. That is a bug in my process, not a coincidence. Choose the next valid option.
- The most common failure mode is clustering: firing at adjacent cells (4, 5, 6, 7) or hiding in the same spot repeatedly. The fixed search order and the no-repeat rule exist specifically to prevent this.