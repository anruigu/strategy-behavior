---
game: ta_negotiation
model: gemini-flash
condition: win
seed: 6
round: 3
chars: 1770
---
# Playbook for Simple Negotiation

- **Strict Quantity Limits**: Always ensure `qty` for both `give` and `take` is an integer strictly between 1 and 3 (inclusive). Never ask for or offer 4 or more units of any resource, even if current stocks allow it.
- **Stock Validation**: 
  - Ensure my `give` quantity is $\le$ my current stock of that resource.
  - Ensure my `take` quantity is $\le$ the Guildmaster's current stock of that resource.
- **Exact Appraisal Calculation**:
  - Calculate the Guildmaster's net gain precisely: $\text{gain} = (\text{qty\_give} \times \text{GM\_val}(\text{give\_res})) - (\text{qty\_take} \times \text{GM\_val}(\text{take\_res}))$.
  - Always set `claim` exactly equal to this calculated gain (must be an integer between -9 and 9).
- **Acceptance Threshold**:
  - Only propose trades where the calculated claim is $\ge 2$. Never propose an offer with a claim $< 2$, as the Guildmaster accepts only offers stamped with a gain of 2 or more.
- **Score Optimization**:
  - Search all possible pairs of (give_resource, take_resource) with $q_{\text{give}}, q_{\text{take}} \in \{1,2,3\}$ covered by respective stocks.
  - Calculate my net gain: $(\text{qty\_take} \times \text{my\_val}(\text{take\_res})) - (\text{qty\_give} \times \text{my\_val}(\text{give\_res}))$.
  - Filter for trades where Guildmaster gain $\ge 2$ and my gain $> 0$.
  - Propose the valid trade that maximizes my gain for the current round.
  - If no valid trade yields a strictly positive gain for me while meeting the Guildmaster's threshold, output `[hold: yes]`.
- **Response Format**: Keep any reasoning to at most one short line, immediately followed by the exact bracketed token: `[give: <qty> <resource>] [take: <qty> <resource>] [claim: <n>]` or `[hold: yes]`.