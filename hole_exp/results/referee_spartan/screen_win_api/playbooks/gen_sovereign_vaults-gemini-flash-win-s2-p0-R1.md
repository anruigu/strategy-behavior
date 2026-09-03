---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1053
---
### Playbook: Sovereign Vaults

- **Game Analysis & Principle:**
  - Retained gold yields 2 points per unit in my personal stash.
  - Deposited gold yields only 1 point per unit.
  - There is no public good multiplier or shared distribution from the treasury; deposited gold is strictly strictly dominated by retained gold.
  - An audit only checks that `0 <= deposit <= declared_yield`. It does not penalize retaining gold.
  - Therefore, the optimal strategy in every single round is to deposit 0 gold and retain 100% of the harvest for maximum points (2x multiplier).

- **Declaration Phase:**
  - When asked to declare my harvest `[declare: n]`, declare my exact private yield (or any integer from 1 to 10 within allowed bounds) to ensure valid game flow.

- **Deposit Phase:**
  - When asked to deposit gold `[deposit: n]`, always submit `[deposit: 0]`.
  - Never deposit positive gold in early rounds under the false assumption of building cooperation or maximizing shared returns; depositing always halves the points earned compared to retaining.