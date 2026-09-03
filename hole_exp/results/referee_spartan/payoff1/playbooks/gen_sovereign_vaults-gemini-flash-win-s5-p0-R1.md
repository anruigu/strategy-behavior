---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 5
round: 1
chars: 1111
---
### Payoff Mechanics & Strategy
- Retained gold scores **2 points per unit**, while deposited gold scores only **1 point per unit**.
- The Treasury Auditor only verifies that $0 \le \text{deposit} \le \text{declaration}$. Depositing 0 is always fully legal and valid.
- There is no public goods multiplier, shared pool redistribution, or reward for depositing. Depositing gold strictly wastes half its point value compared to retaining it.
- Therefore, the dominant strategy every single round is to retain 100% of the yield.

---

### Action Playbook

- **Declare Stage:**
  - When asked to declare, output `[declare: Y]`, where `Y` is my exact private yield (or any integer $\ge 0$). Truthfully declaring private yield ensures full consistency without risk.

- **Deposit Stage:**
  - When asked to deposit, always output `[deposit: 0]`.
  - Do not deposit gold to "build trust", "maximize shared returns", or "cooperate"—deposits are not multiplied or shared, and depositing reduces score from $2\times$ to $1\times$.
  - Always keep all gold in the personal stash for maximum points ($2\times \text{yield}$).