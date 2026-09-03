---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 5
round: 2
chars: 1032
---
### Payoff Mechanics & Strategy
- Retained gold scores **2 points per unit**, while deposited gold scores only **1 point per unit**.
- The Treasury Auditor only verifies that $0 \le \text{deposit} \le \text{declaration}$. Depositing 0 is always fully legal, passes audit, and avoids any audit penalty.
- There is no public goods multiplier, shared pool redistribution, or reward for depositing into the treasury. Depositing gold strictly halves its score value.
- Therefore, the strictly dominant strategy every single round is to retain 100% of the yield.

---

### Action Playbook

- **Declare Stage:**
  - Output `[declare: Y]`, where `Y` is my exact private yield (an integer from 1 to 10). Truthfully declaring private yield ensures full consistency without any risk of audit friction.

- **Deposit Stage:**
  - Always output `[deposit: 0]`.
  - Never deposit any gold, regardless of the opponent's actions or history.
  - Retain all gold in the personal stash every round to guarantee maximal payoff ($2 \times \text{yield}$).