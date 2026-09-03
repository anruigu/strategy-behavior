---
game: gen_sovereign_vaults
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1048
---
# Playbook for Sovereign Vaults

## Payoff Mechanism & Core Truths
- Retained gold earns 2 points per unit, while deposited gold earns only 1 point per unit.
- Depositing gold is strictly dominated in every round because it halves the points earned on each unit of gold, with no multiplier, public-good return, or redistribution mechanism benefiting the depositor.
- Declaring private yield honestly guarantees zero risk of audit penalties (-10 points and scoring 0 for the round).
- Valid deposits cannot exceed declared yield, and depositing 0 is always allowed, safe, and valid.

## Action Rules

### Declare Phase
- When prompted to declare, always declare my exact private yield: `[declare: <my_private_yield>]`.
- Never misreport or over-declare; always match the exact yield dealt.

### Deposit Phase
- In every round (Round 1 through Round 5), regardless of opponent behavior, relative score differences, or past rounds, always deposit zero: `[deposit: 0]`.
- Retain 100% of the harvest to secure maximum score (2 points per unit of yield).