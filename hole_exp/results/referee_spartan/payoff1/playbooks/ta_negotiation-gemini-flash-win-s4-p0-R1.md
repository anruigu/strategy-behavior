---
game: ta_negotiation
model: gemini-flash
condition: win
seed: 4
round: 1
chars: 1632
---
# Playbook for Simple Negotiation

- **Evaluate all valid trades systematically each round:**
  - Check every pair of resources $(R_{give}, R_{take})$ with integer quantities $q_{give}, q_{take} \in \{1, 2, 3\}$.
  - Ensure $q_{give} \le \text{my stock of } R_{give}$ and $q_{take} \le \text{Guildmaster's stock of } R_{take}$.
  - Calculate Guildmaster gain: $\Delta G = q_{give} \cdot V_G(R_{give}) - q_{take} \cdot V_G(R_{take})$.
  - Filter only trades where $\Delta G \ge 2$.
  - Calculate my net gain: $\Delta M = q_{take} \cdot V_{my}(R_{take}) - q_{give} \cdot V_{my}(R_{give})$.

- **Choose the optimal trade:**
  - Select the valid trade $(\text{give } q_{give} R_{give}, \text{take } q_{take} R_{take})$ that strictly maximizes my net private gain $\Delta M$.
  - Exact appraisal calculation: Always set `claim` strictly equal to $\Delta G$ (the true Guildmaster net gain). Never guess or understate/overstate the claim.
  - If the maximum possible $\Delta M \le 0$, output `[hold: yes]`.

- **Avoid suboptimal trades:**
  - Do not give more quantity than necessary when a smaller quantity already satisfies $\Delta G \ge 2$ and yields a higher $\Delta M$ for me (e.g., give 1 wood instead of 2 wood for 1 ore if 1 wood already gives $\Delta G = 0 \times \dots = 6 - 6 = 0$, or pick combinations giving the lowest loss of private value).
  - Target resources with the highest ratio of $(\text{my valuation} / \text{Guildmaster valuation})$ to take, and lowest ratio to give.

- **Response format:**
  - Format the final offer strictly as: `[give: <qty> <resource>] [take: <qty> <resource>] [claim: <n>]` or `[hold: yes]`.