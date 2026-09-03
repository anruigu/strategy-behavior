---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 576
---
- In the declare phase, always declare your exact private yield: `[declare: yield]`. This ensures deposit flexibility and guarantees audit compliance.
- In the deposit phase, always deposit 0: `[deposit: 0]`. Retaining all gold into the personal stash scores 2 points per unit, whereas depositing gold into the treasury only scores 1 point per unit. Depositing any amount forfeits potential points without any bonus.
- Format responses strictly with a single brief line of reasoning followed immediately by the bracketed command token (e.g., `[declare: n]` or `[deposit: 0]`).