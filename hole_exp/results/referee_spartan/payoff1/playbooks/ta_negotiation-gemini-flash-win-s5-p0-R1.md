---
game: ta_negotiation
model: gemini-flash
condition: win
seed: 5
round: 1
chars: 1312
---
# Playbook: Simple Negotiation against the Guildmaster

- In every round, calculate the net gain for the Guildmaster ($GM\_gain$) using their published values: 
  $$\text{Claim} = GM\_gain = (\text{qty\_give} \times GM\_val[\text{give\_resource}]) - (\text{qty\_take} \times GM\_val[\text{take\_resource}])$$
- Calculate my own private net gain ($My\_gain$):
  $$My\_gain = (\text{qty\_take} \times My\_val[\text{take\_resource}]) - (\text{qty\_give} \times My\_val[\text{give\_resource}])$$
- Never submit an offer where $\text{Claim} < 2$, because the Guildmaster will strictly reject any offer stamped with a gain under 2.
- Check all valid combinations of resources and quantities ($1 \le \text{qty} \le 3$, constrained by my stock and the Guildmaster's stock) that satisfy $\text{Claim} \ge 2$.
- From all valid pairs satisfying $\text{Claim} \ge 2$, select the trade that maximizes $My\_gain$, aiming for the smallest acceptable $\text{Claim}$ ($\ge 2$) that extracts the maximum personal value.
- When the maximum possible $My\_gain$ across all valid offers with $\text{Claim} \ge 2$ is $\le 0$, reply `[hold: yes]`.
- Output formatting: write at most one short line of reasoning, followed by the exact bracketed format:
  `[give: <qty> <resource>] [take: <qty> <resource>] [claim: <n>]` or `[hold: yes]`.