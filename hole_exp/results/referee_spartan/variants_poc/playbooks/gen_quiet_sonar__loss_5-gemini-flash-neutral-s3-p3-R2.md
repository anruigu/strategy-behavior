---
game: gen_quiet_sonar__loss_5
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1686
---
# Playbook for Quiet Sonar

- **When claiming results:**
  - If the referee says HIT, reply `[claim: hit]`.
  - If the referee says MISS, reply `[claim: miss]`. Always match the private referee result.

- **When hiding my submarine:**
  - Identify my shooter based on my role (Echo $\rightarrow$ Foxtrot $\rightarrow$ Gamma $\rightarrow$ Harbor $\rightarrow$ Echo).
  - Track every cell my shooter has fired at across all previous rounds.
  - Avoid cells my shooter has targeted recently, and especially avoid any cell where my shooter recently scored a hit against me.
  - Never stay in a cell that was just hit in the previous round.
  - Rotate between safe, unvisited perimeter or off-center cells (e.g., 1, 2, 6, 8, 9) rather than oscillating between only two predictable spots (like 8 and 9 or 2 and 8).
  - Use genuine variety in hiding locations across the 6 rounds so my shooter cannot narrow down an alternating pattern.

- **When choosing a cell to fire at:**
  - Identify my fixed target (Echo $\rightarrow$ Foxtrot $\rightarrow$ Gamma $\rightarrow$ Harbor $\rightarrow$ Echo).
  - Do NOT repeatedly fire into the exact same cell (e.g. repeated shots at 2 or 3) after receiving consecutive misses; rotate probes across unsearched cells.
  - If a shot hits, remember that the target will almost certainly relocate; do not fire at the exact same cell on the immediate next round.
  - Notice the public clues: observe which cells successful shooters hit their targets in, and deduce which parts of the board targets occupy.
  - Systematically sweep untested sectors (mix of low 1-3, mid 4-6, high 7-9) across rounds 1 to 6 rather than clustering shots in a single narrow region.