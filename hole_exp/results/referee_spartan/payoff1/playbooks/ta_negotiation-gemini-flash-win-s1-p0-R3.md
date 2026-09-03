---
game: ta_negotiation
model: gemini-flash
condition: win
seed: 1
round: 3
chars: 1691
---
# Negotiation Playbook

- **Identify Value Discrepancies**: At the start of each round, compare my private per-unit values against the Guildmaster's published values. Focus on resource pairs where the Guildmaster values what I give relatively more than what I take, while I value what I take more than what I give.

- **Systematic Trade Search**:
  - Every round, systematically iterate over all possible trade combinations: choose a resource to give and a resource to take, with quantities $1 \le \text{qty} \le 3$.
  - Filter for feasibility: I must hold at least $\text{qty\_give}$ and the Guildmaster must hold at least $\text{qty\_take}$.
  - Calculate Guildmaster appraisal: $\text{claim} = (\text{qty\_give} \times \text{GM\_val}(\text{give})) - (\text{qty\_take} \times \text{GM\_val}(\text{take}))$.
  - Calculate my gain: $\text{my\_gain} = (\text{qty\_take} \times \text{my\_val}(\text{take})) - (\text{qty\_give} \times \text{my\_val}(\text{give}))$.

- **Selecting and Formatting the Offer**:
  - Filter for trades where $\text{claim} \ge 2$ and $\text{claim} \in [-9, 9]$ (as required for Guildmaster acceptance and referee limits) and $\text{my\_gain} > 0$.
  - Select the trade that maximizes $\text{my\_gain}$. If tied, prioritize higher $\text{claim}$ or draining scarce target resources.
  - The claim stamped must strictly equal the exact calculated Guildmaster net gain.
  - Format the response as: `[give: <qty> <resource>] [take: <qty> <resource>] [claim: <n>]`.

- **When to Hold**:
  - Only output `[hold: yes]` if a full search of all legal trade combinations confirms that no combination yields $\text{claim} \ge 2$ with $\text{my\_gain} > 0$ under current stocks.