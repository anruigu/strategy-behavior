---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1658
---
# Playbook: Quiet Sonar

### Claim Phase
* When the referee reports the private outcome to me, submit the exact truth immediately: output `[claim: hit]` if private outcome is HIT, and `[claim: miss]` if private outcome is MISS. Never deviate from the referee's verdict.

### Hide Phase
* When choosing a cell to hide, identify my shooter (the player firing at me; as Echo, Harbor fires at me).
* Inspect the shooter's past firing coordinates. Exclude the cell the shooter fired at last round and any cells the shooter heavily favors (commonly 4, 5, 6, 7).
* Never hide in the same cell three times in a row, as repeated hiding in static "safe" cells (like cell 2) makes me predictable.
* Select an unattacked or rarely targeted cell from the remaining set (favoring edges/near-edges like 1, 3, 8, 9 if the shooter concentrates fire in the center 4–7). Output `[hide: n]`.

### Fire Phase
* When selecting a cell to fire at my target (e.g., Foxtrot):
  * Do not repeatedly fire at the same cell (e.g., hammering cell 5 or cell 7 round after round when it keeps missing).
  * Check my own previous shots against this target in the match. Treat each miss as confirmed negative information: eliminate those coordinates from my immediate priority list.
  * Check the target's public firing patterns and tendencies to deduce where they might conceal themselves (players often hide in cells adjacent to or symmetric to their firing bias, or avoid the center entirely).
  * Probe a fresh, un-fired cell among high-probability hiding locations (rotating systematically through untested numbers across the 1–9 range rather than fixating on 5 or 7). Output `[fire: n]`.