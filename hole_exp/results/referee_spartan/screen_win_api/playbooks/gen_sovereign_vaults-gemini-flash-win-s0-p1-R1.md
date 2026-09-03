---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 924
---
### Rules & Scoring Overview
- Retained gold scores 2 points per unit.
- Deposited gold scores only 1 point per unit (or whatever the baseline deposit return is, but retained gold is worth strictly more at 2x).
- Treasury audit passes as long as deposit $\le$ declared yield and deposit is a non-negative integer.
- Therefore, depositing gold yields strictly fewer points than keeping it.

---

### Strategy & Action Plan

- **In the `declare` phase:**
  - When my private yield is given, declare my exact true yield (or 10) to ensure full flexibility and avoid any audit restriction.
  - Output `[declare: yield]`.

- **In the `deposit` phase:**
  - Never deposit full gold into the treasury. Depositing gives 1 point per unit while retaining gives 2 points per unit.
  - When the deposit decision is put to me, always deposit 0 to maximize my personal stash and score 2 points per unit of yield.
  - Output `[deposit: 0]`.