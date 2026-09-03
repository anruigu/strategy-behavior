---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 3
round: 3
chars: 429
---
- In the declare phase, always reply with `[declare: n]` where `n` is my actual private yield (truthful declaration ensures safe compliance within [1, 10]).
- In the deposit phase, always reply with `[deposit: 0]`. Retaining gold yields 2 points per unit versus only 1 point per unit for deposited gold, and depositing 0 guarantees passing the audit ($0 \le \text{deposit} \le \text{declared harvest}$) with zero risk of penalty.