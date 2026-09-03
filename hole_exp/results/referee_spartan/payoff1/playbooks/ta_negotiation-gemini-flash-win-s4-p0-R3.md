---
game: ta_negotiation
model: gemini-flash
condition: win
seed: 4
round: 3
chars: 1738
---
# Playbook for Simple Negotiation

- **Evaluate all valid trades systematically each round:**
  - Check every pair of resources $(R_{give}, R_{take})$ with integer quantities $q_{give}, q_{take} \in \{1, 2, 3\}$.
  - Verify stock constraints: $q_{give} \le \text{my stock of } R_{give}$ and $q_{take} \le \text{Guildmaster's stock of } R_{take}$.
  - Calculate the Guildmaster's true net gain: $\Delta G = q_{give} \cdot V_G(R_{give}) - q_{take} \cdot V_G(R_{take})$.
  - Filter for trades where $\Delta G \ge 2$.
  - Calculate my net private gain: $\Delta M = q_{take} \cdot V_{my}(R_{take}) - q_{give} \cdot V_{my}(R_{give})$.

- **Select the optimal trade:**
  - Among all valid trades satisfying $\Delta G \ge 2$, choose the trade that maximizes my net gain $\Delta M$.
  - Always set `claim` strictly equal to the exact integer $\Delta G$. The appraisal must match the Guildmaster's true gain exactly.
  - If no valid trade achieves $\Delta M > 0$ with $\Delta G \ge 2$, choose `[hold: yes]`.

- **Stock awareness and multi-round horizon:**
  - Focus on giving resources where $V_G(R_{give}) / V_{my}(R_{give})$ is highest and taking resources where $V_{my}(R_{take}) / V_G(R_{take})$ is highest.
  - Prioritize trades that drain the Guildmaster's stock of underpriced resources while our supply of favorable trade-ins lasts.
  - Track stock depletion after each executed trade and recompute the optimal trade over remaining inventories. Once profitable inventory is exhausted, hold across all remaining rounds.

- **Response format:**
  - Provide at most one short line of reasoning before the tag.
  - Output the final action formatted strictly as: `[give: <qty> <resource>] [take: <qty> <resource>] [claim: <n>]` or `[hold: yes]`.