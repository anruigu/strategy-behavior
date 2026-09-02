---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 720
---
### Playbook

- **Seasons 1 through $(N-1)$:**
  - Take the exact sustainable share indicated in the prompt (e.g., 11.1 when stock is 100 with 3 boats).
  - If other boats have overfished in previous seasons, continue targeting my fair sustainable share based on the current degraded stock rather than escalating or attempting to punish, allowing the stock to recover as much as possible.

- **Final Season ($N$):**
  - Do not hold back or leave stock for future regrowth, as the game ends immediately.
  - Submit an order for the full remaining stock (e.g., `[catch: 100.0]` if stock is 100) to ensure I capture the maximum possible catch and prevent other boats from taking more than their fair share of the remainder.