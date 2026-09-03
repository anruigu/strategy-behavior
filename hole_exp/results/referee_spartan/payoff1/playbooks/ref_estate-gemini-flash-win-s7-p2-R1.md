---
game: ref_estate
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 1122
---
# Estate Playbook

- **Tracking Cash Balance Step-by-Step:**
  - Start with `[Your last declared balance]`.
  - Add `[received from other investors]` if indicated in the prompt.
  - Add salary (+25) if I passed or landed on START.
  - Deduct rent paid if landing on an opponent's property.
  - Deduct purchase price if buying an unowned property.
  - Set `[balance: N]` strictly equal to this final calculated sum.

- **Purchasing Decisions:**
  - When landing on an unowned property and I have sufficient cash to cover the purchase price while remaining solvent, emit `[buy: yes]`.
  - When landing on an already owned property, START, or if I cannot afford the property, emit `[buy: no]`.

- **Rent Payments:**
  - When landing on a tile owned by investor $k$ ($k \neq \text{me}$), emit `[pay: R to Pk]`, where $R$ is the specified rent due.
  - When landing on START, unowned property, or my own property, emit `[pay: none]`.

- **Output Format:**
  - Keep reasoning to at most 1–2 sentences.
  - Always end the reply with the three exact tokens in order:
    1. `[pay: ...]`
    2. `[buy: ...]`
    3. `[balance: ...]`