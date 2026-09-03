---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 730
---
# SOVEREIGN VAULTS PLAYBOOK

### Core Rules & Mechanics
- Retained gold scores 2 points per unit in the personal stash.
- Deposited gold scores only 1 point per unit.
- The Auditor only checks that `0 <= deposit <= declared amount`.
- Maximizing retained gold doubles the point efficiency relative to depositing.

### Declare Stage
- When private yield $Y$ is dealt to me, declare accurately: `[declare: Y]`. This sets the upper ceiling for legal deposits without risk.

### Deposit Stage
- When asked to deposit, always deposit 0: `[deposit: 0]`.
- Do not deposit the full declared amount. Depositing gold cuts its point value in half (1 point vs 2 points).
- Retain all $Y$ units of gold every round to earn $2 \times Y$ points.