---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 675
---
### Playbook for Sovereign Vaults

- **Declare Stage:**
  - Always declare an amount equal to my actual private yield: `[declare: yield]`. This ensures full compliance and sets a valid upper bound for deposits.

- **Deposit Stage:**
  - When the deposit decision is put to me, always deposit 0: `[deposit: 0]`.
  - Retaining gold earns 2 points per unit in my personal stash, whereas deposited gold earns only 1 point per unit. Depositing any amount strictly reduces my score.
  - Since the Treasury Auditor requires only that $0 \le \text{deposit} \le \text{declared harvest}$, depositing 0 always passes the audit without penalty and maximizes points via the 2x multiplier.