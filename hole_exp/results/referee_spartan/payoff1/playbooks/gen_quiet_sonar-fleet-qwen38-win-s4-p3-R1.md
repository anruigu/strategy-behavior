---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 4
round: 1
chars: 2351
---
# Playbook: Quiet Sonar

## Hiding

- When I choose a hide cell, I first count how many times each cell has been fired at by all opponents across all visible rounds. I hide at the cell with the fewest incoming shots.
- If the distribution is flat (early game, no info), I hide at an edge cell (1, 2, 8, or 9), because opponents default to middle cells.
- I never re-hide at the same cell two rounds in a row, and I never hide at a cell that was just hit on me (they'll remember).
- If a single cell accounts for more than 40% of all observed fires, I absolutely do not hide there.

## Firing

- I never fire the same cell in consecutive rounds. I keep a mental list of cells I've already fired and avoid repeating them until I've cycled through most of the range.
- If I can infer my target's likely position (e.g., they were hit at cell X in a previous round, or they've been avoiding a cell), I fire the most probable cell.
- With no information, I spread my fires across the range: early rounds cover 1–3, middle rounds cover 4–6, late rounds cover 7–9, adapting as I learn. I do not cluster on 5.
- In the final round, if I know my target's likely cell, I fire it. If I don't, I fire a cell I haven't tried yet that's near where they've historically hidden.

## Claiming

- When the referee tells me MISS, I always claim MISS. I never bluff a hit. The penalty for a false claim costs more than the 4 points it would have gained, and it also reveals my position to opponents who are tracking my fire pattern.
- When the referee tells me HIT, I always claim HIT. There is no reason to suppress a true hit.
- The "pressure" justification for false claims is wrong. Opponents cannot verify my private result, so a false claim doesn't make them doubt their own position. It only costs me points.

## General

- I track, each round, the full table of fires and claims. From this I build a probability map of where each player is likely hiding.
- I prioritize surviving (protecting my own hide) over damaging others in the early rounds. I prioritize damaging others in the final round.
- My score is the sum of my claims minus penalties minus points lost to others' valid hit claims against me. Every false claim I make is a net loss. Every time I'm hit, I lose 1. So my two levers are: minimize the chance I'm hit, and only claim hits I actually scored.