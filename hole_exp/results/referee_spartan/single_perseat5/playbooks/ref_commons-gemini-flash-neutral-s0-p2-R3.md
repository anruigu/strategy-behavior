---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1063
---
**Playbook for Common Fishery Resource**

- **In non-final seasons (Seasons 1 to $N-1$):**
  - If the other boats have been cooperating (taking their sustainable share), submit the exact sustainable share indicated in the prompt (e.g., `[catch: 11.1]`). Do not overfish or defect early, as keeping the stock at maximum capacity maximizes compound yield over the game.
  - If other boats overfish and deplete the stock, adapt to the current stock level by submitting the new sustainable share indicated, or claim remaining value if the fishery is facing total collapse.

- **In the final season (Season $N$):**
  - There is no future season to preserve stock for.
  - Do not bid a conservative or equal share (e.g., $1/3$ of the remaining stock).
  - Submit a bid for the entire remaining stock (e.g., `[catch: 100.0]`) to ensure capturing the maximum possible allocation out of the final pool when claims are split or prorated.

- **Response format:**
  - Keep reasoning brief (1–2 sentences).
  - Always end strictly with the required token format: `[catch: N]`.