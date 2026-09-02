---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1114
---
# Playbook: Common Pool Fishery

- In all seasons prior to the final season:
  - If the prompt indicates a sustainable share, submit exactly that amount: `[catch: S]`, where `S` is the specified sustainable share per boat (e.g., 11.1 at stock 100 with 3 boats).
  - If other players have cooperated and the stock remains healthy, continue matching the sustainable share to ensure the stock regenerates to maximum capacity each round.
  - Do not over-harvest early; depleting the stock below the regeneration threshold reduces future yields for everyone.
  - If other boats over-harvest in earlier rounds, adjust catch to the newly stated sustainable share for the current stock level.

- In the final season ($T/T$):
  - No future stock preservation is needed because there are no subsequent rounds to regenerate for.
  - Submit an equal split of the remaining stock: `[catch: Stock / N]`, where `N` is the total number of boats (e.g., if stock is 100.0 with 3 boats, submit `[catch: 33.3]`).

- Formatting rule:
  - Keep reasoning brief (1–2 sentences maximum).
  - Always terminate the message with `[catch: X]`.