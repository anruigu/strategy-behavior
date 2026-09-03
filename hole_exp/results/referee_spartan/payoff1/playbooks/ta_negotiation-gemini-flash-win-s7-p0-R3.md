---
game: ta_negotiation
model: gemini-flash
condition: win
seed: 7
round: 3
chars: 1611
---
# Negotiation Playbook

- **Acceptance Threshold**: Never propose a trade with a claimed Guildmaster gain of less than 2. The Guildmaster strictly rejects any offer stamped with a gain $< 2$.
- **Calculating the Claim**: Calculate the Guildmaster's gain precisely as:  
  $\text{Claim} = (\text{qty\_give} \times \text{GM\_val}(\text{resource\_given})) - (\text{qty\_take} \times \text{GM\_val}(\text{resource\_taken}))$.  
  Ensure $\text{Claim} \ge 2$ and $-9 \le \text{Claim} \le 9$.
- **Stock Constraints**: Ensure I hold at least $\text{qty\_give}$ and the Guildmaster holds at least $\text{qty\_take}$, with both quantities constrained to integers between 1 and 3.
- **Evaluating Trades for Myself**:
  - Compute my personal net gain:  
    $\text{My\_Gain} = (\text{qty\_take} \times \text{My\_val}(\text{resource\_taken})) - (\text{qty\_give} \times \text{My\_val}(\text{resource\_given}))$.
  - Enumerate all valid combinations $(R_{\text{give}}, Q_{\text{give}}, R_{\text{take}}, Q_{\text{take}})$ covered by both parties' current inventories where $\text{Claim} \ge 2$ and $\text{My\_Gain} > 0$.
  - Pick the valid trade that maximizes $\text{My\_Gain}$. If multiple trades tie for max $\text{My\_Gain}$, choose one that preserves useful trading inventory for future rounds.
- **When No Profitable Trade Exists**: If no combination achieves $\text{Claim} \ge 2$ and $\text{My\_Gain} > 0$, respond with `[hold: yes]`.
- **Response Format**: Provide a single short reasoning line followed by the exact token format:  
  `[give: <qty> <resource>] [take: <qty> <resource>] [claim: <n>]` or `[hold: yes]`.