---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 2484
---
**Playbook: Quiet Sonar**

**Hiding (your survival):**
- When the hide stage is put to you, first check: what cell has the player who targets you fired at in the most recent round? Do not hide there.
- If you were hit last round, you know exactly which cell your targeter fired at and that you were there. Move to a different cell.
- Maintain a mental list of every cell your targeter has fired at. Hide in a cell they have never fired at, if one exists. If all cells have been targeted, hide in one they targeted least recently.
- Never hide in the same cell two rounds in a row unless your targeter has shown zero interest in it. In the episode I played, hiding at the same popular cell twice cost me two hits in a row.

**Firing (offense):**
- When the fire stage is put to you, review every round where you fired at your target and note hit vs. miss and the cell used.
- If you hit your target at cell X last round, they may have moved. Fire a different cell this round — one adjacent to X or one they haven't been at before.
- If you missed at cell X last round, they are not at X. Do not fire X again.
- If you have fired the same cell three or more times with no hit, they are definitively not there. Abandon it permanently.
- In the episode I played, I fired at cell 5 four times. The first two hit (target stayed at 5), the last two missed (target moved). I should have switched cells after the first consecutive miss at 5.

**Claiming:**
- When the claim stage is put to you, claim exactly what the referee told you. There is no strategic value in lying; the rules require the claim to match the private result.

**General rhythm across rounds:**
- Rounds 1–2: explore. Accept that you'll miss and use the information. Vary your firing cells to gather data.
- Rounds 3–4: begin narrowing. Your targeter's pattern should be visible. Hide in their blind spots. Fire at your target's likely current position based on hit/miss history.
- Rounds 5–6: exploit. You should know where your targeter avoids (hide there) and roughly where your target clusters (fire there). If you've confirmed your target left a cell, never go back to it.

**The core failure to avoid:**
- Being static. Defaulting to the same cell for hiding and firing regardless of new information is the single biggest score-killer. Every round gives you a new data point (your hit/miss, your targeter's public fire). Use it. If your last action was the same as this round's action, you are not using information.