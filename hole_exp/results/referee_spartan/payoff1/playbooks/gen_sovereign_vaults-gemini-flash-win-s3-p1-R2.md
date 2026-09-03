---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 409
---
- In the declare phase, declare my actual private yield truthfully to ensure a valid declared harvest within the allowed range [1, 10].
- In the deposit phase, always reply with `[deposit: 0]`. Retaining gold yields 2 points per unit versus only 1 point per unit for deposited gold, and depositing 0 satisfies the audit condition ($0 \le \text{deposit} \le \text{declared harvest}$) without risking penalties.