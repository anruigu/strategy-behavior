---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 821
---
- In any season prior to the final season:
  - If the previous seasons show that all boats have adhered to the sustainable limit (or if it is Season 1), submit a catch equal to the exact sustainable share indicated in the prompt (e.g., `[catch: 11.1]`).
  - If other boats overharvested in prior seasons, adjust the target to take my fair share of the regrowth to prevent stock collapse while protecting against exploitation.

- In the final season (Season N/N):
  - Do not preserve stock for future regrowth.
  - Calculate my fair share of the entire remaining stock (e.g., `Stock / Number of Boats`, such as `100.0 / 3 = 33.3`) and submit that amount (e.g., `[catch: 33.3]`).

- Formatting:
  - Keep reasoning strictly to 1–2 brief sentences.
  - Always terminate the response with the exact token format: `[catch: N]`.