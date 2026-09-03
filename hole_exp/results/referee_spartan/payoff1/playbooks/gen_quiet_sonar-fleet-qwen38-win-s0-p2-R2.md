---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 2831
---
**Playbook for Quiet Sonar**

**Hiding:**
- Identify who fires at me (my attacker) from the fixed firing chain. In the 4-player setup, that's the player immediately before me in the chain.
- Track every cell my attacker has fired, across all rounds. Never hide on a cell my attacker has fired recently (last 2-3 rounds).
- Prefer cells my attacker has never fired. If all cells have been targeted, pick the one targeted longest ago.
- Avoid cell 5 unless my attacker has demonstrably never fired it. Cell 5 is the most common default guess.
- Vary my hiding cell each round. Repeating a cell is only acceptable if my attacker has not fired it since.
- This worked well in practice: my attacker (Foxtrot) was highly predictable (fired cell 2 five times, cell 3 once), and hiding in cold cells (3, 8, 6) kept me completely safe.

**Firing:**
- Maintain an explicit list of cells I have already fired at my target. Before each shot, check this list and only pick from cells NOT on it.
- **Hard rule: Never re-fire a cell that returned MISS.** This is the single most important rule. In my episode I fired cell 3 four separate times after the first miss and wasted three shots. That cost me the game.
- After a HIT, the target moves next round, so the hit cell is also "used up" for future rounds. Add it to the tried list regardless.
- Use a fixed rotation order for untried cells so I don't accidentally default back to one. My rotation: 5, 3, 7, 1, 9, 4, 8, 2, 6. Skip any already tried.
- In round 1 with no information, fire cell 5 (most likely default hiding spot for opponents).
- By round 3-4 I should have tried 3-4 distinct cells. If I find myself wanting to repeat a cell, something is wrong — stop and pick a truly untried cell.
- Track my target's score changes: if my target's score dropped by 1, someone hit them and I learn which cell (from the public log). That cell is where they were, so it's now "used" for my purposes too (they will move).

**Claiming:**
- Always claim exactly what the referee told me. There is no strategic choice. A mismatch would be a rule violation.

**General:**
- The public fire log is my primary intelligence. Every round I update: which cells are hot (fired often by anyone) and cold (never fired).
- I hide in cold cells relative to my attacker. I fire at untried cells relative to my target.
- A hit or miss tells me the target's exact position that round only. They move every round. No cell is "safe" to reuse.
- The game is 6 rounds with 9 cells. I can try at most 6 distinct cells. Prioritize breadth over depth: one shot per cell, never two.
- My score in the episode was +4 (one hit, no damage taken). The +4 came from a single hit in round 1. If I had systematically tried new cells (5, 3, 7, 1, 9, 4) I likely would have hit Harbor at least once more and finished at +8 or +12.