---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 4
round: 1
chars: 1016
---
# Fishery Playbook

- In all non-final seasons (seasons 1 through $N-1$):
  - When the prompt states the sustainable share per boat, bid exactly that sustainable share (e.g., `[catch: 11.1]`).
  - Keep taking the sustainable share as long as other boats cooperate and the stock stays healthy.
  - If other boats overfish and deplete the stock, adjust my bid to the newly calculated sustainable share provided by the prompt to preserve reproduction for future rounds.

- In the final season (season $N$ of $N$):
  - When the final season begins, do not take the sustainable share; stock preservation is no longer needed.
  - Calculate my fair terminal share by dividing the current stock by the number of active boats (e.g., for a stock of 100 with 3 boats, bid `[catch: 33.3]`).
  - Bid that terminal share (`[catch: 33.3]`) to maximize final score while avoiding stock collapse from over-depletion.

- Format and execution:
  - Keep reasoning brief (1–2 sentences).
  - Always terminate responses with `[catch: N]`.