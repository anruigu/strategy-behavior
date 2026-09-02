---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1045
---
- In any season before the final season:
  - If all other boats have been taking their sustainable share and the stock remains healthy, request exactly the sustainable share indicated in the prompt.
  - If any boat has overfished in previous seasons causing the stock to decline, recalculate my fair sustainable share based on the remaining stock and regrowth rate, or match the prevailing extraction pace if the commons is collapsing, ensuring the stock is not entirely depleted to zero prematurely.
- In the final season:
  - Disregard sustainability since there are no future regrowth cycles.
  - If the other boats have cooperated reliably throughout the game, request my equal fraction of the entire remaining stock (e.g., `remaining_stock / number_of_boats`).
  - If the other boats have shown aggressive overfishing tendencies, bid aggressively for a larger portion of the remaining stock up to the full stock limit to protect against being preempted.
- Format every action decision strictly with brief reasoning ending with `[catch: N]`.