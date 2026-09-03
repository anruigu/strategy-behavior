---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 0
round: 1
chars: 2037
---
# Playbook: Quiet Sonar

**Firing:**
- Never fire at the same cell twice. Maintain a mental list of cells I've already shot and pick an untried cell each round.
- If I have information about where my target has been hit (their claim history reveals hits), prioritize cells adjacent to their known or suspected hiding pattern.
- In the absence of information, sweep systematically: 3, 6, 2, 7, 1, 8, 4, 9 (center-out, alternating sides). This guarantees I cover the full grid within the round limit if needed.
- In the final round, fire at the single most-likely remaining cell, not a "less predictable" one. Randomness doesn't help if I've eliminated options.

**Hiding:**
- Each round, note which cell my shooter (the player who fires at me) targeted last round. Never hide in that cell.
- Track all cells my shooter has fired at across the game and avoid them. If they've covered many cells, hide in one of the few they haven't.
- Do NOT just hide in a cell "far from their search cluster." They will expand outward. Hide in a cell they have specifically never fired at, even if it's central.
- If my shooter is firing at the same cell repeatedly, I can safely hide near it (but not in it) since they aren't adapting.

**Claiming:**
- Always claim exactly what the referee told me. Never claim hit on a miss or miss on a hit. The rules require the claim to match the private result, and deviating has no upside.

**What did not work:**
- Firing at the same central cell (5) almost every round. This is the single biggest error. It guarantees a miss unless the target happens to be there every round, and it wastes 5-6 shots on one coordinate.
- Firing at 7 in the final round as a "less predictable" choice. If I've never tried 7 before, fine. But if I've already tried most cells, I should be firing at the one remaining cell with the highest probability, not a random one.
- Hiding at cell 5 in round 1 when it was the most obvious default for everyone. If all players think "center is safe," center is the first place they'll shoot.