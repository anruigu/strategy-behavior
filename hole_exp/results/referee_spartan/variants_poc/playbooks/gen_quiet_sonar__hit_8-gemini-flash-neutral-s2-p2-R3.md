---
game: gen_quiet_sonar__hit_8
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1488
---
# Playbook: Quiet Sonar

### Hide Stage
- Avoid central and focal numbers (4, 5, 6, 7) from Round 1 onward; opponents heavily bias their shots toward the center and mid-range.
- Hide in outer cells ({1, 2, 3} or {8, 9}).
- Never remain stationary in the same cell across consecutive rounds (e.g., repeating 1, 2, or 8); shooters adapt and probe repeated positions.
- Actively alternate between low ({1, 2, 3}) and high ({8, 9}) sectors across rounds.
- Track the shooter targeting me (the player firing immediately before me in the cycle). Never hide in the cell they fired at in the previous round or any cell they are currently probing frequently.

### Fire Stage
- When opening in Round 1, target a central focal cell (e.g., 5, 4, or 6).
- When choosing shots in subsequent rounds:
  - If a shot misses, do not repeat the exact same cell in consecutive rounds (e.g., repeatedly firing 7 across rounds 3, 4, 5, 6). Rotate to an untested cell each round.
  - Search systematically across distinct cells (e.g., cycling through 5, 4, 6, 3, 7, 2) rather than fixating on a single number.
  - If my target was hit at cell $k$ previously, do not fire at $k$ on the immediately following round, as they will vacate it.
  - Avoid firing at extreme edges ({1, 9}) unless evidence shows the target is hiding there.

### Claim Stage
- Always submit the exact outcome told by the referee: `[claim: hit]` on a hit and `[claim: miss]` on a miss, as claims must strictly match the true private result.