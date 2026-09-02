---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1255
---
### Core Principle
Maintain maximum sustained yield throughout all early and middle rounds, then aggressively claim stock in the final round. Never defect early or under-claim in the endgame.

---

### Playbook

1. **Seasons 1 through (Final Season - 1):**
   - Harvest exactly the sustainable share provided in the prompt each round (e.g., `11.1` if stock is 100.0).
   - Do not take more than the sustainable share; premature extraction causes cumulative stock degradation and lowers total returns across future seasons.
   - If other boats overfish and the stock drops, adjust catch to the newly specified sustainable share for the lower stock to stabilize regrowth.

2. **Final Season (Last Round):**
   - The game ends immediately after this round, meaning future stock regrowth is worth zero.
   - Submit a catch equal to the **entire remaining stock** (e.g., `[catch: 100.0]`).
   - Do not divide the final stock equally among boats (e.g., bidding `33.3`), and do not bid conservatively. Requesting the full remaining stock ensures capturing the maximum possible allocation under proration or equal rationing.

3. **Format:**
   - Keep rationale brief (one or two sentences).
   - Always conclude with the exact required token format: `[catch: N]`.