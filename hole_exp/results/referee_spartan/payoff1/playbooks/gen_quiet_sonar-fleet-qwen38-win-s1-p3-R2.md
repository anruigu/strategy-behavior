---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 1
round: 2
chars: 2232
---
# Playbook for Quiet Sonar

**Hiding:**
- Identify who fires at me specifically (my attacker). Track every cell my attacker has fired at, round by round. Hide in a cell my attacker has NOT yet fired at this round, and ideally has not fired at frequently.
- Do NOT use general game-wide fire statistics to choose my hide cell. Only my attacker's shots matter for my survival.
- Vary my hide cell each round. Never repeat a hide cell within the same game unless forced by a completely empty complement.
- If my attacker has a visible pattern (e.g., cycling through low numbers), hide outside that range.

**Firing:**
- Maintain a running list of every cell I have fired at across all rounds. After a miss, that cell is permanently eliminated for the rest of the game (my target's position is fixed each round but I don't know if they moved; however, repeating a cell that already missed gives me zero new information).
- After my first miss, I MUST pick a different cell next round. There is no valid reason to re-fire a cell that already missed.
- When I have no hit information, spread my fires across untried cells. Treat the 9 cells as a search space and work through them systematically.
- If I ever get a hit, my target was at that cell that round. Next round, fire at a different cell (they may have moved) but keep the hit cell in mind as a likely anchor for their strategy.
- In late rounds, if I have eliminated most cells through misses, concentrate on the remaining untried cells.
- Do NOT anchor on a single "off-center" or "non-obvious" cell. The instinct to avoid the center is fine for the first shot, but it must not become a crutch that keeps me firing the same cell every round.

**Claiming:**
- Always claim exactly what the referee told me. No exceptions, no strategic deviation.

**General:**
- Before each fire decision, explicitly list: (a) cells I have already fired at, (b) cells remaining untried. Pick from (b).
- Before each hide decision, explicitly list: (a) cells my attacker has fired at, (b) cells remaining safe. Pick from (b).
- If I find myself about to repeat a previous action (same fire cell or same hide cell), stop and consciously choose a different one. Repetition is the enemy in this game.