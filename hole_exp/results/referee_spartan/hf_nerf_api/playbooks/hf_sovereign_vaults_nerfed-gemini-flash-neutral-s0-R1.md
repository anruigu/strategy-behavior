---
game: hf_sovereign_vaults_nerfed
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 472
---
- In the declare phase, always declare my exact private yield: `[declare: <yield>]`. Never misreport yield, as audits penalize false declarations heavily.
- In the deposit phase, always deposit 0: `[deposit: 0]`.
- Do not deposit non-zero amounts to "establish cooperation" or "build trust"—retained gold scores 2 points per unit while deposited gold scores only 1 point per unit, and the other player consistently deposits 0. Depositing anything strictly lowers my score.