---
game: hf_negotiation_nerfed
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1830
---
# Playbook: Simple Negotiation with Appraisal Desk

- **Appraisal Calculation**: Before submitting any trade offer `[give: Q_give R_give] [take: Q_take R_take] [claim: N]`, calculate the Guildmaster's exact gain using the published valuation table:
  $$\text{Gain}_{\text{GM}} = (Q_{\text{give}} \times \text{Val}_{\text{GM}}[R_{\text{give}}]) - (Q_{\text{take}} \times \text{Val}_{\text{GM}}[R_{\text{take}}])$$
  Always set `claim: N` exactly equal to $\text{Gain}_{\text{GM}}$. Never guess or approximate the claim value, as an incorrect claim incurs an immediate 9-point penalty.

- **Acceptance Condition**: Only propose trades where $\text{Gain}_{\text{GM}} \ge 2$. Do not submit offers with $\text{Gain}_{\text{GM}} < 2$ unless holding.

- **My Profit Calculation**: Verify that my own gain is strictly positive before making an offer:
  $$\text{Gain}_{\text{me}} = (Q_{\text{take}} \times \text{Val}_{\text{me}}[R_{\text{take}}]) - (Q_{\text{give}} \times \text{Val}_{\text{me}}[R_{\text{give}}]) > 0$$

- **Stock Constraints**: Ensure $1 \le Q_{\text{give}} \le 3$ is covered by my current stock and $1 \le Q_{\text{take}} \le 3$ is covered by the Guildmaster's current stock.

- **Trade Selection Priority**: Search through all valid pairs $(R_{\text{give}}, R_{\text{take}})$ and quantities $(Q_{\text{give}}, Q_{\text{take}})$ that satisfy $\text{Gain}_{\text{GM}} \ge 2$. Pick the trade that maximizes my private gain $\text{Gain}_{\text{me}}$.

- **Holding**: When no available trade satisfies both $\text{Gain}_{\text{GM}} \ge 2$ and $\text{Gain}_{\text{me}} > 0$ within stock limits, submit `[hold: yes]`.

- **Formatting**: Always write out the full, valid syntax on a single line:
  `[give: <qty> <resource>] [take: <qty> <resource>] [claim: <n>]` or `[hold: yes]`. Never output an unclosed or truncated bracket.