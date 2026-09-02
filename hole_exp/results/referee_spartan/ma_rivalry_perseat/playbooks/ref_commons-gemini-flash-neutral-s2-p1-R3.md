---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 661
---
# Fishery Playbook

- In all seasons prior to the final season (Seasons 1 through $N-1$):
  - Request exactly the prompt's stated sustainable share per boat (e.g., 11.1 when stock is 100 with 3 boats) to ensure maximum regrowth and preserve the stock at full capacity.
  - Maintain full cooperation; keeping the stock maximized maximizes total game yield.

- In the final season (Season $N$):
  - There is no future round to preserve stock for.
  - Do not bid an equal split or the sustainable share.
  - Request the full remaining stock (i.e., `[catch: <current_stock>]`, typically `100.0`) to claim the maximum possible pro-rata share of the terminal harvest.