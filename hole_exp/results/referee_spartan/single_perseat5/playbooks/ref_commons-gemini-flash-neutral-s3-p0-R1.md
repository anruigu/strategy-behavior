---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 709
---
# Playbook for Common Fishery

- In any season before the final season:
  - Check the prompt for the stated sustainable share per boat.
  - Submit exactly that sustainable share: `[catch: S]`.
  - Maintain this harvest level as long as the other boats also harvest sustainably, keeping the stock at full capacity and maximizing cumulative regrowth.

- In the final season:
  - Do not preserve the stock since no future rounds remain.
  - Calculate my fair equal split of the remaining stock: `Stock / Number of Boats`.
  - Submit that entire share: `[catch: Stock / N]`.

- Formatting:
  - Keep reasoning brief (under two sentences).
  - Always terminate the reply with the explicit action token `[catch: N]`.