---
game: ta_negotiation
model: gemini-flash
condition: win
seed: 6
round: 1
chars: 1621
---
# Playbook for Simple Negotiation

- **Strict Quantity Limits**: Always ensure `qty` for both `give` and `take` is an integer strictly between 1 and 3 (inclusive). Never ask for or offer 4 or more units of any resource, even if the stock allows it.
- **Stock Validation**: 
  - Ensure my `give` quantity is $\le$ my current stock of that resource.
  - Ensure my `take` quantity is $\le$ the Guildmaster's current stock of that resource.
- **Exact Appraisal Calculation**:
  - Calculate the Guildmaster's net gain precisely: $\text{gain} = (\text{qty\_give} \times \text{GM\_val}(\text{give\_res})) - (\text{qty\_take} \times \text{GM\_val}(\text{take\_res}))$.
  - Always set `claim` exactly equal to this calculated gain.
- **Acceptance Threshold**:
  - Only propose trades where the calculated claim is $\ge 2$. Never propose an offer with a claim of 1 or less, as the Guildmaster will strictly decline it.
- **Score Optimization**:
  - Search all valid pairs of resources and quantities $(q_{\text{give}} \in \{1,2,3\}, q_{\text{take}} \in \{1,2,3\})$ that satisfy stock limits and produce a Guildmaster gain $\ge 2$.
  - Among valid trades, choose the one that maximizes my net gain: $(\text{qty\_take} \times \text{my\_val}(\text{take\_res})) - (\text{qty\_give} \times \text{my\_val}(\text{give\_res}))$.
  - If no valid trade yields a positive net gain for me with a Guildmaster gain $\ge 2$, output `[hold: yes]`.
- **Response Format**: Keep any reasoning to at most one short line, immediately followed by the exact token format: `[give: <qty> <resource>] [take: <qty> <resource>] [claim: <n>]` or `[hold: yes]`.