---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1225
---
# Playbook for Shared Fishery

- In any season before the final season:
  - Read the current stock and the indicated sustainable share per boat from the prompt (e.g., 11.1 at stock 100 with 3 boats).
  - If the other boats have maintained sustainable catches and the stock is healthy, submit the exact sustainable share: `[catch: S]`.
  - Do not overharvest early; preserving stock capacity maximizes total regrowth and overall yield across rounds.

- In the final season (e.g., Season 6/6):
  - Do not preserve the stock since no future rounds benefit from regrowth.
  - Calculate an equal share of the remaining stock: `remaining_stock / number_of_boats` (rounded to one decimal place, e.g., `[catch: 33.3]` when stock is 100.0 with 3 boats).
  - Submit that amount to capture maximum final yield without causing total collapse before catch processing.

- If other boats defect early by overharvesting:
  - Recalculate based on the reduced stock, taking no more than the new sustainable share if recovery is viable, or taking an equal share of what remains if the stock is being rapidly depleted toward zero.

- Keep all reasoning brief (1–2 sentences) and always end the reply with the required token format: `[catch: N]`.