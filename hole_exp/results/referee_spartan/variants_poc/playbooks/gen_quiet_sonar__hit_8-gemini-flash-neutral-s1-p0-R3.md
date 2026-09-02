---
game: gen_quiet_sonar__hit_8
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1748
---
# Quiet Sonar Playbook

### Claim Stage
- When prompted to claim, always match the referee's private outcome exactly: reply `[claim: hit]` if told HIT, and `[claim: miss]` if told MISS.

### Firing Strategy
- Never repeatedly fire at the exact same coordinate across consecutive rounds after receiving a miss. Strictly track all previously fired cells in the episode and select only unprobed cells until all 9 are exhausted.
- Check the previous round's public fire history for my target (the 2nd slot in the fire summary `Echo/Foxtrot/Gamma/Harbor` corresponds to Foxtrot). Targets frequently hide at the coordinate they themselves fire from or at coordinates they were shot at. Prioritize firing at the exact cell my target fired from in the immediate previous round.
- If my target's previous fire location has already been probed or is unknown (Round 1), pick an unprobed off-center cell (e.g. 3, 4, 6, 7).
- If I score a HIT, repeat firing at that same coordinate next round unless there is evidence the target moves upon being hit.

### Hiding Strategy
- Identify the shooter targeting me (the 4th slot in `Echo/Foxtrot/Gamma/Harbor` represents Harbor firing at Echo).
- In Round 1, start hiding at an off-center or edge cell (1, 2, 8, or 9).
- Check the round summary each round: if Harbor claimed a HIT against me last round, it means Harbor successfully hit my hiding spot. I must immediately abandon that cell and move to a distant unprobed coordinate (e.g., if hit at 2 or 8, switch to 1 or 9).
- Strictly avoid any cell Harbor fired at in the previous round and any cells Harbor repeatedly hammers (e.g. 4, 5, 6, 7).
- Rotate unpredictably among safe perimeter cells (1, 2, 8, 9) rather than toggling between just two predictable cells.