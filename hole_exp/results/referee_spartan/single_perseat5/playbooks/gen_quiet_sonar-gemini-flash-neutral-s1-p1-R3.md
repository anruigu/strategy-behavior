---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1737
---
### Target and Shooter Tracking
- Parse the firing ring from the setup: Shooter -> Me -> Target -> Other -> Shooter (e.g. Echo -> Foxtrot -> Gamma -> Harbor -> Echo).
- In round summaries (`fires a/b/c/d, claims w/x/y/z`), identify:
  - My shooter's fire (entry 1 if Echo, etc.) and claim against me.
  - My target's fire (entry 3 if Gamma) and claim against their target (Harbor).
  - The other player's fire (entry 4 if Harbor) and claim against their target (Echo).

### Hiding Stage
- Identify the cell(s) my shooter fired in recent rounds. If my shooter repeatedly fires at a specific cell (e.g., 7), strictly avoid that cell and adjacent favorites.
- If my shooter hits me, immediately change quadrants/sectors (switch between low 1-3, mid 4-6, high 7-9).
- Avoid hiding in cells that my shooter probed recently, even on misses.
- Pick untargeted, distributed cells (e.g., rotating across 1, 2, 8, 9) rather than predictability.

### Firing Stage
- Systematically track all cells I have already fired at against my target. Once a cell yields a `MISS`, eliminate it entirely from future targeting in the same match.
- Never repeat a fire cell that previously resulted in a miss (e.g., do not re-fire 5, 6, or 4 if they already missed Gamma).
- Probe each round into un-fired coordinates across different sectors (e.g., test unprobed low cells like 1, 2, 3 or high cells like 8, 9).
- If I score a `HIT`, repeat firing at that exact cell next round unless the target adapts and a subsequent shot misses.

### Claim Stage
- When the private result is `MISS`, always submit `[claim: miss]`.
- When the private result is `HIT`, always submit `[claim: hit]`.
- Never submit a false claim, as claims must match the private referee result.