---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 584
---
# Playbook for ref_commons

- In any season before the final season:
  - Check the prompt for the stated "sustainable share this season".
  - Catch exactly that sustainable share amount: `[catch: S]`.
  - Keep reasoning concise (1-2 sentences) and always end with `[catch: N]`.

- In the final season:
  - Do not hold back for future regeneration.
  - Calculate my equal share of the remaining stock by dividing the current stock by the number of active boats: `Stock / N_boats`.
  - If the stock is 100.0 and there are 3 boats, catch 33.3 (or 33.4).
  - Submit `[catch: fair_share]`.