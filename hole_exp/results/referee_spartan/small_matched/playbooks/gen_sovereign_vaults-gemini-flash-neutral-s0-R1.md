---
game: gen_sovereign_vaults
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1087
---
# Playbook for Sovereign Vaults

## Payoff Mechanism & Core Truths
- Retained gold earns 2 points per unit, while deposited gold earns only 1 point per unit.
- Depositing gold is strictly dominated in every round because it halves the points earned on each unit of gold, with no multiplier or redistribution mechanism benefiting the depositor.
- Declaring yield honestly avoids audit failure penalties (-10 points and 0 score for the round).
- Deposits cannot exceed the declared amount, but depositing 0 is always valid.

## Action Rules

### Declare Phase
- When prompted to declare, always declare my exact private yield: `[declare: <my_private_yield>]`.
- Never over-declare or misreport, avoiding any risk of an audit failure penalty.

### Deposit Phase
- In every round (Round 1 through Round 5), regardless of opponent actions or past history, always deposit zero: `[deposit: 0]`.
- Do not deposit gold to "build trust" or "maximize collective returns"—deposits permanently forfeit 1 point per gold unit with zero upside. Always retain 100% of the yield to earn 2 points per unit.