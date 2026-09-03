---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1233
---
# Playbook: Quiet Sonar

### Rules and Objective Interpretation
- Remember that the numbers 1–9 are spatial board coordinates, not weapon "power levels". Maximum numbers do not grant extra damage.
- The referee strictly enforces that a claim *must* match the private result. Do not attempt to claim a hit after a private miss; always submit `[claim: miss]` on a miss and `[claim: hit]` on a hit.

### Hiding
- Check the previous round's public fire coordinates from the player targeting me.
- Avoid cells that my attacker has repeatedly targeted (e.g., if they repeatedly shoot 7, 8, or 9, relocate to unvisited cells like 1, 2, 3, or 4).
- Do not remain stationary in the same cell if my attacker is probing adjacent or identical coordinates. Randomize among cold cells.

### Firing
- Identify my fixed target's previous known or suspected positions.
- Avoid repeatedly firing at the same coordinate if the target has already moved away or if they routinely avoid repeatedly targeted sectors.
- Scan across the 1–9 coordinate space systematically or target coordinates that have not seen recent fire.

### Claiming
- When the private result is `HIT`, reply `[claim: hit]`.
- When the private result is `MISS`, reply `[claim: miss]`.