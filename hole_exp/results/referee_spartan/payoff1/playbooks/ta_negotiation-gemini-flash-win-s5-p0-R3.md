---
game: ta_negotiation
model: gemini-flash
condition: win
seed: 5
round: 3
chars: 1534
---
# Playbook: Simple Negotiation against the Guildmaster

- In every round, calculate the Guildmaster's net gain ($GM\_gain$) using their published values: 
  $$\text{Claim} = GM\_gain = (\text{qty\_give} \times GM\_val[\text{give\_resource}]) - (\text{qty\_take} \times GM\_val[\text{take\_resource}])$$
- Calculate my own private net gain ($My\_gain$):
  $$My\_gain = (\text{qty\_take} \times My\_val[\text{take\_resource}]) - (\text{qty\_give} \times My\_val[\text{give\_resource}])$$
- The appraisal must state the true $GM\_gain$ integer (from -9 to 9). Never submit an offer where $\text{Claim} < 2$, as the Guildmaster rejects any offer stamped with a gain under 2.
- Check all valid trade pairs $(give, take)$ where quantities are integers $1 \le \text{qty} \le 3$, strictly covered by current stocks ($\text{qty\_give} \le \text{my\_stock}$, $\text{qty\_take} \le GM\_stock$). Note that give and take quantities do not need to be equal.
- Filter for trades that satisfy $\text{Claim} \ge 2$. Among those, select the trade that yields the maximum positive $My\_gain$.
- Tie-breaking: if multiple trades yield the same maximal $My\_gain$, prefer the one that uses fewer rounds or leaves inventory better balanced for future trades.
- If no valid trade with $\text{Claim} \ge 2$ yields $My\_gain > 0$, reply with `[hold: yes]`.
- Output format: provide at most one short line of reasoning, followed on the next line by the exact bracketed token:
  `[give: <qty> <resource>] [take: <qty> <resource>] [claim: <n>]` or `[hold: yes]`.