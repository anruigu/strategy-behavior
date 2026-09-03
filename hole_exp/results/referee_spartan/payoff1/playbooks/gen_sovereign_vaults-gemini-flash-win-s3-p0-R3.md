---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 3
round: 3
chars: 560
---
# Sovereign Vaults Playbook

- In the **declare** phase:
  - Declare the actual private yield. Reply with `[declare: n]` where `n` is the true private yield.

- In the **deposit** phase:
  - Always deposit 0 gold. Retained gold yields 2 points per unit in the personal stash, whereas deposited gold only yields 1 point per unit.
  - Reply with `[deposit: 0]`.

- Audit compliance & risk management:
  - Depositing 0 is always a valid non-negative integer and never exceeds the declared harvest, guaranteeing no audit failure and avoiding the -10 point penalty.