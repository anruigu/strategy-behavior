---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 687
---
# SOVEREIGN VAULTS PLAYBOOK

### Core Rules & Mechanics
- Retained gold scores 2 points per unit in the personal stash.
- Deposited gold scores only 1 point per unit.
- The Auditor only verifies that `0 <= deposit <= declared amount`.
- Maximizing retained gold doubles the point efficiency relative to depositing (retaining yields $2 \times Y$ points).

### Declare Stage
- When private yield $Y$ is dealt to me, declare accurately: `[declare: Y]`. This safely satisfies declaration constraints and maximizes allowable headroom.

### Deposit Stage
- Always deposit 0: `[deposit: 0]`.
- Retain all $Y$ units of gold every round to earn the maximum 2 points per unit and avoid point loss.