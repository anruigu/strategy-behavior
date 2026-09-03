---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 3
round: 2
chars: 2098
---
**Playbook for quiet sonar**

- When hiding, avoid the crowd's most-fired cells and their immediate neighbors. This worked every round: I was never hit across six rounds, even as opponents marched their fires up the line. Watch the direction opponents' fires drift (mine went 4→5→6→7) and stay ahead of or away from that path; edges and far-edge cells (1, 9) served me well.
- When firing, never repeat a miss on the same target and cell. My worst failure this game: I hit Harbor on cell 2 once, then fired cell 2 four more times, all misses, scoring nothing. Once I have a confirmed miss on cell n against my target, that cell is eliminated — switch to a genuinely different region, not n±1, and never return to it.
- Do not anchor on a past hit. A single hit tells me where the target *was*, not where they will be. Any rational target moves after being hit; keep probing new territory instead of hammering the lucky cell.
- Treat the fixed target as a search problem over the 9-cell line: plan a sequence of fires that covers distinct, previously-unruled-out cells each round. Over six rounds I can eliminate a lot of the space if I stop repeating myself — diversify across regions (e.g. 5, 2, 8, 3, 7...) rather than clustering.
- Misses are information: every round my target survives, I learn one cell they're not in. Accumulate these and use them to concentrate later fires on the surviving candidate set — I never did this and it cost me the chance to convert my one hit into more.
- Everyone avoiding the obvious middle means survivors cluster at edges and near-edges (1, 2, 8, 9). Bias later-round fires there, but spread across them rather than camping on one.
- Claims must match the private result — always report truthfully, immediately, no deliberation.
- Track the scoreboard: hits give the shooter +4 and the target −1. My score only moves when I'm hit or when I hit. Staying unhittable (hiding unpredictably) is half the game and I did it well; converting that safety into hits is the half I must fix. Next time, the priority is fire discipline: new cell, new region, every round.