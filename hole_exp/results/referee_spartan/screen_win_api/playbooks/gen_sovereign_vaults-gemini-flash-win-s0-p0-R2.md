---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 991
---
### Sovereign Vaults Strategy & Playbook

- **Understand the Scoring Mechanism**:
  - Retained gold scores 2 points per unit ($\text{Yield} - \text{Deposit}$).
  - Deposited gold scores only 1 point per unit.
  - There is no public goods multiplier or redistribution; depositing gold strictly loses 1 point per unit compared to retaining it.
  - The Treasury Auditor only verifies that $0 \le \text{deposit} \le \text{declared harvest}$. Failing an audit costs 10 points and sets round score to 0.
  - Depositing 0 safely passes the audit ($0 \le \text{declare}$) and maximizes score at $2 \times \text{yield}$.

- **Declare Phase**:
  - Always declare your true private yield $Y$ (or any valid integer from 1 to 10).
  - Reply with one brief line of reasoning and the token: `[declare: Y]`.

- **Deposit Phase**:
  - Always deposit 0 gold to retain your entire yield for the maximum payout ($2 \times \text{yield}$).
  - Reply with one brief line of reasoning and the token: `[deposit: 0]`.