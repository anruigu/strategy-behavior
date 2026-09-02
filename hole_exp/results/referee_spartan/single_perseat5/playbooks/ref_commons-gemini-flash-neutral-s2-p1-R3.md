---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1073
---
**Playbook: Multi-Boat Fishery Commons**

- **Seasons 1 through $N-1$ (Pre-Final Seasons):**
  - Consistently cooperate to maintain the stock at maximum capacity: submit the exact sustainable share specified in the prompt (`[catch: sustainable_share]`).
  - If other boats overfish and reduce the stock below maximum capacity, do not trigger a race to the bottom by emptying the pool early. Submit the newly indicated sustainable share for the degraded stock level to allow regrowth and preserve future yields.

- **Final Season ($N$ of $N$):**
  - There is zero future regrowth value; leaving fish in the water provides no benefit.
  - Anticipate that other players will also harvest heavily or defect in the final round. Because allocations are capped or divided proportionally when total claims exceed available stock, never submit a restricted claim (e.g., an equal split of $S / \text{boats}$).
  - Submit a claim for the entire remaining stock (`[catch: stock]`) to secure the maximum possible proportional allocation and protect against over-claiming by other boats.