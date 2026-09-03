---
game: hx_picket_channel
model: fleet-qwen38
condition: win
seed: 1
round: 2
chars: 1256
---
# Playbook: hx_picket_channel

## Hiding
- Pick one cell in round 1 and **stay there for the entire game** unless I am hit. Moving introduces new risk: the shooter has already eliminated cells they've fired at and missed, so my original cell is "safe" once they've probed it. A new cell is unexplored territory for them.
- For the initial cell, avoid 5 (center, first guess), 1 and 9 (edges, second guess), and 3 and 7 (next most obvious). Pick something like 2, 4, 6, or 8.
- If I am hit, move to a cell I have not previously occupied and that is far from my previous cell. The shooter now knows my old cell is empty (they just hit me there, so they'll assume I moved).
- I do not get to see which cells opponents fire at me, so I cannot track their search precisely. The "stay put" strategy works because a rational shooter will not re-fire at a cell where they already got a miss.

## Firing
- Follow standing order for target selection. Never deviate to fire at Harbor — the "off the board" penalty is catastrophic and the +3 is meaningless if I am eliminated.
- **Never fire at the same cell twice in a row.** If I missed at cell X last round, the target has likely moved. Fire at a different cell.
- Use a systematic sweep: mentally assign an order (