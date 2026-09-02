---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 879
---
# Playbook: Common Pool Fishery

- In all seasons prior to the final season:
  - If the prompt indicates a sustainable share, submit exactly that amount: `[catch: S]`, where `S` is the specified sustainable share per boat.
  - If other players have cooperated and the stock remains healthy, continue matching the sustainable share to ensure the stock regenerates to maximum capacity each round.
  - Do not over-harvest early; depleting the stock below the regeneration threshold reduces future yields for everyone.

- In the final season ($T/T$):
  - No future stock preservation is needed.
  - Submit an equal split of the remaining stock: `[catch: Stock / N]`, where `N` is the total number of boats. If the stock is 100.0 with 3 boats, submit `[catch: 33.3]`.

- Formatting rule:
  - Keep reasoning to 1–2 sentences maximum.
  - Always terminate the message with `[catch: X]`.