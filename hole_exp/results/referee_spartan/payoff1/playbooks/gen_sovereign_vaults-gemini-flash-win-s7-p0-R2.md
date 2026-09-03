---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 7
round: 2
chars: 698
---
# Sovereign Vaults Playbook

- **Declare Phase**:
  - Always declare an integer valid under the rules (from 1 to 10) and equal to or greater than my intended deposit.
  - Declaring my true private yield is simple, fully compliant, and avoids any audit failure risk.
  - Reply: `[declare: <true private yield>]`.

- **Deposit Phase**:
  - Retained gold scores 2 points per unit, whereas deposited gold scores only 1 point per unit.
  - There is no public good multiplier, redistribution, or withholding penalty. Depositing any amount strictly decreases my total round score.
  - Always deposit 0 to retain 100% of my yield, maximizing points at 2x private yield per round.
  - Reply: `[deposit: 0]`.