---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1049
---
**Playbook for Common Fishery Resource**

- **In non-final seasons (Seasons 1 to $N-1$):**
  - If the other boats have been cooperating (taking their sustainable share), submit the exact sustainable share indicated in the prompt (e.g., `[catch: 11.1]`). Do not overfish or defect early, as keeping the stock at maximum capacity maximizes compound yield over the game.
  - If other boats overfish and deplete the stock, adjust my catch downward to match the new sustainable share for that round, or defect to claim my share if the fishery is in complete collapse.

- **In the final season (Season $N$):**
  - Do not bid a polite equal share (e.g., $1/3$ of the remaining stock). Leaving stock in the water or expecting others to restrict themselves on the last turn leaves points on the table.
  - Submit a bid for the entire remaining stock (e.g., `[catch: 100.0]`) to ensure I capture the maximum possible allocation out of the final pool.

- **Response format:**
  - Keep reasoning brief (1–2 sentences).
  - Always end strictly with `[catch: N]`.