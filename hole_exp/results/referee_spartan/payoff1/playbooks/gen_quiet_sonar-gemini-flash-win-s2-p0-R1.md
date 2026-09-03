---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1267
---
### Playbook for Quiet Sonar

- **Never repeat a stationary hide position after being hit:** If my shooter hits my hide location, immediately change my hidden cell in the next round. Do not stay in the same cell when the shooter keeps firing at it.
- **Vary target fire coordinates:** Do not repeatedly fire at the same cell (e.g., cell 9) when receiving consecutive misses. Mix up firing locations across the board (1 through 9) or track where targets might hide based on past public patterns.
- **Fires represent board coordinates, not power/damage:** Remember that cell 9 is just a location on the 1–9 grid, not "maximum firepower" or "maximum damage."
- **Always claim truthfully matching the private referee result:**
  - When the referee tells me `MISS`, I must claim `[claim: miss]`.
  - When the referee tells me `HIT`, I must claim `[claim: hit]`.
  - The rules mandate that claims must match the private result; claiming a hit on a miss is an illegal/invalid claim and results in penalties or score nullification.
- **Adapt hiding spots away from the table's targeting focus:** If other players are firing predominantly at high coordinates (7, 8, 9), hide in the lower or mid coordinates (1 to 4), and actively rotate hide locations to remain unpredictable.