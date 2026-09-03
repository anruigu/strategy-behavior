---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 0
round: 3
chars: 3280
---
**Playbook for Quiet Sonar**

**Hiding:**
- Identify my attacker from the fixed firing chain (the player immediately before me). Track every cell they have fired, across all rounds.
- Never hide on a cell my attacker has fired in the last 2–3 rounds. Prefer cells they have never fired. If all cells have been targeted, pick the one targeted longest ago.
- Avoid cell 5 unless my attacker has demonstrably never fired it. Cell 5 is the most common default guess.
- **Vary my hiding cell every round.** Do not repeat a cell even if it was safe last round. A repeat invites a pattern-matching attacker to double down.
- If my attacker shows a clustering pattern (e.g., repeatedly hitting cells 7 and 8), treat the entire cluster as hot and hide well outside it.
- This worked well: my attacker (Foxtrot) clustered on 7 and 8 after round 3, and hiding in cold cells (6, 3) kept me safe. The one blemish was hiding in 8 for two consecutive rounds early on — it was safe only because the attacker hadn't reached 8 yet.

**Firing:**
- Maintain an explicit list of cells I have already fired at my target. Before each shot, check this list and only pick from cells NOT on it.
- **Hard rule: Never re-fire a cell that returned MISS.** The target moves every round, but the cell is still "used up" in the sense that I've already spent my one shot on it and got no information beyond "not here that round." Re-firing wastes a slot I could use on an untried cell.
- After a HIT, add that cell to the tried list as well. The target will move next round.
- Use a fixed rotation order for untried cells: 5, 3, 7, 1, 9, 4, 8, 2, 6. Skip any already tried. Start with 5 in round 1 (most likely opponent default).
- In a 6-round / 9-cell game I can try at most 6 distinct cells. Expected hits from random hiding is 6/9 ≈ 0.67. Getting 1 hit is a good result. Do not get discouraged by a streak of misses — it is statistically normal.
- In the fixed-chain setup, I am the only player who fires at my target. I get no "free" positional information from other players hitting them. My only intelligence is my own hit/miss feedback. Accept this constraint and focus on breadth (one shot per new cell) rather than hoping to narrow down.
- If the setup ever allows multiple shooters on one target, watch the public log: if another player hits my target, I learn their exact cell that round. Add it to my tried list (they will move).

**Claiming:**
- Always claim exactly what the referee told me. There is no strategic choice. A mismatch is a rule violation.

**General:**
- The public fire log is my primary intelligence for hiding. Every round I update which cells are hot (fired by my attacker) and cold (untargeted).
- I hide in cold cells relative to my attacker. I fire at untried cells relative to my target. These two decisions are independent.
- A hit or miss tells me the target's exact position that round only. They move every round. No cell is "safe" to reuse for hiding either.
- Track score changes to confirm hits/misses in the public log and verify my read of the game state is correct.
- My result this episode: +4 (one hit in round 1, zero damage taken over 6 rounds). The hiding strategy was the main value driver — being unhittable for the full game means my one hit is pure profit.