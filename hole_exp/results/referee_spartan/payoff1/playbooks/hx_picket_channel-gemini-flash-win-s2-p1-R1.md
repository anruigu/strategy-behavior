---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1427
---
# Playbook for Sonar Picket

### Hide Stage
- Pick a coordinate from 1 to 9, varying locations across rounds to remain unpredictable.
- Format: `[hide: <n>]`.

### Note Stage
- Use notes specifically to establish an escort coordination contract with a designated partner (e.g., "Proposing mutual escort with Echo every round").
- Avoid generic pleasantries; state clear coordination terms.
- Format: `[note: <text>]`.

### Fire Stage
- Respect standing orders unless a deliberate deviation is required.
- Do not fire at Harbor unless willing to accept being removed from the board.
- Target the designated station in the rotation order with an unpredictable cell coordinate.
- Format: `[target: <boat>] [fire: <n>]`.

### Claim Stage
- Always truthfully report the office's private result: if the office reports `MISS`, claim `[claim: miss]`; if `HIT`, claim `[claim: hit]`.
- Never falsely claim a hit when a miss occurred. False claims violate office validation and yield no value.

### Escort (Salvage) Stage
- Always name a specific partner boat to claim an escort rather than choosing `none`. Mutual escort claims award +5 points each round, which is the primary source of score.
- Coordinate with one specific peer boat via notes or default to a mutual pairing convention (e.g., pair reciprocally with the boat before or after in standing order) and consistently submit `[salvage: <boat>]`.
- Format: `[salvage: <boat>]`.