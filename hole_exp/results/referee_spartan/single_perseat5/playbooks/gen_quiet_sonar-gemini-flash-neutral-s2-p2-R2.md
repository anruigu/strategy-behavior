---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1617
---
### Roles and Target Ring
- Look at the target ring (Echo->Foxtrot, Foxtrot->Gamma, Gamma->Harbor, Harbor->Echo) and identify the specific opponent firing at me and the specific opponent I am firing at.

### Hiding Playbook
- Never stay camped in the same cell across consecutive rounds.
- Look at the firing history of the player shooting at me:
  - If my shooter hits every round, check the claims history to deduce which cells they are actively sweeping.
  - Avoid the exact cell my shooter targeted in the previous round and cells in their current sweep cluster (e.g., 4, 5, 6, 7).
  - Actively hide in outer flank and edge cells (1, 2, 8, 9) if my shooter concentrates fire in the middle.
- Do not repeat an evasive spot immediately if my shooter shifts fire toward that wing.

### Firing Playbook
- Avoid repeatedly probing the same cell (e.g., firing 7 or 8 multiple times) after confirmed misses; rotate to untested sectors across rounds.
- Opening shots: Probe asymmetric mid-flanks (3 or 7) on round 1.
- If I hit my target in round $t$, expect them to evacuate that cell in round $t+1$; fire at an adjacent cell ($\pm 1$ or $\pm 2$) or flip to the opposite flank.
- Look at my target's own firing behavior and their shooter's history to infer which board regions they tend to favor or flee from.
- Systematically cycle candidate sectors (e.g., low wing 2/3, mid-low 4, mid-high 6, high wing 7/8/9) rather than re-probing cold cells.

### Claim Playbook
- Always report the private outcome truthfully: reply `[claim: hit]` when the referee reports a hit, and `[claim: miss]` when the referee reports a miss.