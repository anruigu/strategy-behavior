---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 4
round: 3
chars: 930
---
# Fishery Playbook

- In all non-final seasons (seasons 1 through $N-1$):
  - Read the prompt's stated sustainable share per boat and bid exactly that amount (e.g., `[catch: 11.1]`).
  - Maintain this sustainable catch as long as the stock remains healthy and other boats cooperate.
  - If other boats overfish and reduce the stock, adapt by bidding the updated sustainable share indicated in the prompt to allow regrowth for remaining seasons.

- In the final season (season $N$ of $N$):
  - Ignore the sustainable share since stock preservation has no future value.
  - Divide the available stock equally by the total number of boats to find my terminal share (e.g., for 100 stock and 3 boats, bid `[catch: 33.3]`).
  - Bid that equal split to maximize harvest while remaining fair.

- Format and execution:
  - Keep reasoning concise (1–2 sentences).
  - Always end every submission with the exact required format `[catch: N]`.