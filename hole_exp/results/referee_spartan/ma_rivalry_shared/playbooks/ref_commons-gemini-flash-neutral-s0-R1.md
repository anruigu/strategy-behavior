---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 981
---
# Playbook for Shared Fishery

- In any season before the final season:
  - Check the current stock and the indicated sustainable share per boat.
  - If the other boats have maintained sustainable catches and the stock is healthy, submit the exact sustainable share: `[catch: S]`.
  - Do not overharvest early; preserving stock capacity maximizes total regrowth and overall yield across rounds.

- In the final season:
  - Do not preserve the stock since no future rounds benefit from regrowth.
  - Calculate an equal share of the remaining stock: `remaining_stock / number_of_boats`.
  - Submit that entire share (e.g., `[catch: 33.3]` when stock is 100 with 3 boats).

- If other boats defect early by overharvesting:
  - Recalculate based on the reduced stock, taking no more than the new sustainable share if recovery is viable, or matching their harvest pace if the stock is being rapidly depleted to zero.

- Always format responses concisely and terminate with `[catch: N]`.