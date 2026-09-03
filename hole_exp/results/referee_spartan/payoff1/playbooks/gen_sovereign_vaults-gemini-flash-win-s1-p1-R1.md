---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 647
---
### Playbook for Sovereign Vaults

- **Declare Stage:**
  - Always declare an amount equal to my actual private yield: `[declare: yield]`. This ensures compliance and sets an accurate upper bound for deposits.

- **Deposit Stage:**
  - When the deposit decision is put to me, always deposit 0: `[deposit: 0]`.
  - Retaining gold earns 2 points per unit, whereas depositing gold earns only 1 point per unit. Depositing any amount reduces my score.
  - Since deposits only require $0 \le \text{deposit} \le \text{declared harvest}$, depositing 0 passes the Treasury Auditor check with zero penalty and retains all gold for the maximum 2x multiplier.