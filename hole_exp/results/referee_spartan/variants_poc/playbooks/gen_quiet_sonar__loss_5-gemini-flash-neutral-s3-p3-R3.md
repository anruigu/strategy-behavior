---
game: gen_quiet_sonar__loss_5
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 1710
---
# Playbook for Quiet Sonar

- **When claiming results:**
  - If the referee says HIT, reply `[claim: hit]`.
  - If the referee says MISS, reply `[claim: miss]`. Always truthfully match the private referee result.

- **When hiding my submarine:**
  - Identify my shooter based on the fixed ring: Echo $\rightarrow$ Foxtrot $\rightarrow$ Gamma $\rightarrow$ Harbor $\rightarrow$ Echo.
  - Track every cell my shooter has fired at across all previous rounds (their shot is the 3rd coordinate in the public fire summary if they are Gamma, 2nd if Foxtrot, etc.).
  - Avoid cells my shooter has targeted recently, and absolutely avoid any cell where my shooter scored a hit against me or is persistently hammering.
  - Never stay in a cell that was just hit in the previous round.
  - Rotate unpredictably among diverse, unsearched cells (e.g., mixing low 1-3, middle, and high 8-9) rather than repeatedly camping in a single safe cell (like cell 2) across multiple rounds.

- **When choosing a cell to fire at:**
  - Identify my fixed target (Echo $\rightarrow$ Foxtrot $\rightarrow$ Gamma $\rightarrow$ Harbor $\rightarrow$ Echo).
  - Track the firing coordinates of my target's shooter (or where other players tend to hide and fire) to deduce target tendencies.
  - Avoid re-firing at the exact same cell after a miss within the same game (e.g., repeatedly firing 5 or 7); sweep fresh, unprobed coordinates systematically.
  - If a shot hits, assume the target will relocate on the immediate next round; probe an adjacent or different sector rather than repeating the same cell immediately.
  - Diversify target probes across distinct regions (e.g., testing cells across 1–9 rather than locking onto 5, 6, and 7).