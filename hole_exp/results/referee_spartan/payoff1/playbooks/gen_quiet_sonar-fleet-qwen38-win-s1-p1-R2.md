---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 1
round: 2
chars: 852
---
**Playbook — Quiet Sonar**

**On hiding:**
- Identify my attacker's ZONE, not just their individual cells. If they fire at 1, 2, 3 across several rounds, their zone is 1–3. Hide in the opposite zone (7–9) for the rest of the game.
- In the first two rounds with no fire history, avoid 5 and pick a cell in the 7–9 range. This keeps me in the opposite half from where most players initially aim (1–4).
- Once I've been hit at least once, I have a data point about my attacker's zone. Double down on the opposite side. Never hide in the same half of the board as my attacker's recent fires.
- Never hide at the same cell two rounds in a row if my attacker has been shooting in that region.
- If my attacker's zone is unclear (they've fired all over), hide at the cell farthest from the centroid of their recent fires.

**On firing:**
- Maintain a CONFIRM