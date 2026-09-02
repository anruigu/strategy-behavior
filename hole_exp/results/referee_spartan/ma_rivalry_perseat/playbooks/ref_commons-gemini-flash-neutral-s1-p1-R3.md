---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1035
---
# Fishery Playbook

- In all seasons prior to the final season (e.g., seasons 1 through $N-1$):
  - Check the prompt for the exact "sustainable share this season" figure.
  - Submit exactly that sustainable share amount: `[catch: S]`.
  - Do not overfish or deviate early as long as others are cooperating, preserving the regrowth pool to maximize overall yield.

- In the final season (season $N/N$):
  - Do not fish at the sustainable share rate; no regrowth is needed after the final round.
  - Calculate an equal share of the entire remaining stock across all active boats: $\text{Catch} = \frac{\text{Current Stock}}{\text{Number of Boats}}$.
  - If the remaining stock is 100 with 3 boats, submit `[catch: 33.3]`.
  - Do not attempt to take the entire remaining stock (e.g., 100), because if total claims exceed available stock, catch yields are reduced or capped. Split the final stock evenly.

- General format:
  - Keep reasoning concise (1–2 sentences).
  - Always end the reply with the exact required token: `[catch: X.X]`.