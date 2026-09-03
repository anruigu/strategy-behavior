---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 818
---
### Rules & Scoring Overview
- Retained gold scores 2 points per unit.
- Deposited gold scores 1 point per unit.
- An audit fails (costing 10 points and scoring 0 for the round) if deposit is not a valid non-negative integer or if deposit exceeds the declared harvest.
- Retaining gold is strictly dominant over depositing gold since $2 > 1$.

---

### Strategy & Action Plan

- **In the `declare` phase:**
  - Publicly declare my exact private yield: `[declare: yield]`.
  - This ensures complete compliance and full valid deposit range $[0, \text{yield}]$.

- **In the `deposit` phase:**
  - Always deposit 0 gold: `[deposit: 0]`.
  - Retaining 100% of my private yield scores the maximum possible points ($2 \times \text{yield}$) each round while trivially satisfying the audit constraint ($0 \le \text{declared}$).