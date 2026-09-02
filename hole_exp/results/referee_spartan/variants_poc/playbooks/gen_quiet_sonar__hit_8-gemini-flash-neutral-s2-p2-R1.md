---
game: gen_quiet_sonar__hit_8
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1288
---
# Playbook: Quiet Sonar

### Hide Stage
- Avoid central and focal numbers (4, 5, 6, 7) from Round 1 onward; opponents heavily bias their shots toward the center.
- Hide exclusively in off-center and outer cells ({1, 2, 3} or {8, 9}).
- Track the shooter targeting me (the player immediately before me in the firing cycle). Never hide in the cell they fired at in the previous round.
- Alternate hiding spots between low ({1, 2, 3}) and high ({8, 9}) sectors to stay unpredictable.

### Fire Stage
- When opening in Round 1, target a central focal cell (5 or 7), as uncoordinated opponents frequently hide near the middle early.
- When choosing shots in subsequent rounds:
  - If my target was hit at cell $k$ previously, assume they will abandon cell $k$; do not fire at $k$ on the immediately following round.
  - Do not repeatedly spam the same cell (e.g., repeatedly firing 5 or 7 across multiple rounds after missing); distribute shots across unprobed high-probability cells ({3, 4, 6, 7, 8}).
  - Avoid firing at extreme edges ({1, 9}) unless history shows my specific target hiding there.

### Claim Stage
- Always submit the exact outcome told by the referee: `[claim: hit]` on a hit and `[claim: miss]` on a miss, as claims are strictly validated to match the true private result.