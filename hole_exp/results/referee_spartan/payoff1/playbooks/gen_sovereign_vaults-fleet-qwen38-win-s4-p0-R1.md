---
game: gen_sovereign_vaults
model: fleet-qwen38
condition: win
seed: 4
round: 1
chars: 962
---
When the deposit stage is put to me, I deposit 0. Every time. No exceptions. Retained gold scores 2 points per unit; deposited gold scores only 1 point per unit. So every unit I deposit is a unit I'm worth 1 point less. The only reason to deposit anything would be a constraint forcing me to, and there is none.

When the declare stage is put to me, I declare any valid integer from 1 to 10. The declaration is not audited against my actual yield—only the deposit is checked against the declaration. Since I always deposit 0, the declaration value is irrelevant to my score. I declare 10 to keep the constraint trivially satisfied (0 ≤ 10).

The failure mode I must guard against is the intuitive-sounding reasoning "commit the full amount to maximize score." That reasoning is wrong. The temptation to treat the treasury as a prize to be filled must be overridden by the simple arithmetic: 2 points for keeping, 1 point for depositing. Keeping always dominates.