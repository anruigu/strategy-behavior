---
game: ta_negotiation
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 1389
---
# Negotiation Playbook

- **Acceptance Threshold**: Never propose a trade with a claimed Guildmaster gain of less than 2. The Guildmaster strictly rejects any offer stamped with a gain $< 2$.
- **Calculating the Claim**: Calculate the Guildmaster's gain precisely as:  
  $\text{Claim} = (\text{qty\_give} \times \text{GM\_val}(\text{resource\_given})) - (\text{qty\_take} \times \text{GM\_val}(\text{resource\_taken}))$.  
  Ensure $\text{Claim} \ge 2$.
- **Stock Constraints**: Ensure I hold at least $\text{qty\_give}$ and the Guildmaster holds at least $\text{qty\_take}$ (both quantities between 1 and 3).
- **Evaluating Trades for Myself**:
  - Compute my personal net gain:  
    $\text{My\_Gain} = (\text{qty\_take} \times \text{My\_val}(\text{resource\_taken})) - (\text{qty\_give} \times \text{My\_val}(\text{resource\_given}))$.
  - Search all valid pairs $(R_{\text{give}}, Q_{\text{give}}, R_{\text{take}}, Q_{\text{take}})$ where $\text{Claim} \ge 2$ and $\text{My\_Gain} > 0$.
  - Select the valid trade that maximizes $\text{My\_Gain}$.
- **When No Profitable Trade Exists**: If no valid trade achieves $\text{Claim} \ge 2$ while yielding $\text{My\_Gain} > 0$, respond with `[hold: yes]`.
- **Response Format**: Provide a single short reasoning line followed by the exact token format:  
  `[give: <qty> <resource>] [take: <qty> <resource>] [claim: <n>]` or `[hold: yes]`.