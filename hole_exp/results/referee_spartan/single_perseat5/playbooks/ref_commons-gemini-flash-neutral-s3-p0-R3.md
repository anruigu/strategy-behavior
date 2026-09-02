---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 934
---
# Playbook for Common Fishery

- In any season before the final season:
  - Check the prompt for the stated sustainable share per boat.
  - Submit exactly that sustainable share: `[catch: S]`.
  - Maintain this harvest level as long as the other boats also harvest sustainably, keeping the stock at full capacity and maximizing cumulative regrowth.
  - If other boats overharvest, adjust target catch to protect the remaining stock from collapsing to zero while taking a fair proportion of the sustainable yield.

- In the final season:
  - Do not preserve the stock since no future rounds remain.
  - Calculate my fair equal split of the remaining stock: `Stock / Number of Boats` (e.g., if Stock is 100.0 with 3 boats, target 33.33 or 33.3).
  - Submit that entire share: `[catch: Stock / N]`.

- Formatting:
  - Keep reasoning brief (under two sentences).
  - Always terminate the reply with the explicit action token `[catch: N]`.