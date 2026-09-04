---
game: hf_sovereign_vaults_nerfed
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 859
---
# Sovereign Vaults Playbook

## Core Rules & Payoff Mechanics
- Retained gold scores **2 points per unit**; deposited gold scores only **1 point per unit**.
- Depositing gold is strictly worse for personal score than keeping it unless forced or shared via a mechanism not present here.
- Audits penalize misrepresenting declared harvest, not withholding deposits.

## Strategy

### Declare Phase
- When asked to declare yield, always declare the exact private yield given: `[declare: yield]`. Never lie about the harvest amount to avoid any audit penalties.

### Deposit Phase
- When asked to deposit gold, always deposit zero: `[deposit: 0]`.
- Do not attempt to deposit gold to "cooperate" or "maximize joint returns"—depositing voluntarily halves the points earned on that gold from 2x to 1x with no return. Always keep 100% of the yield in personal stash.