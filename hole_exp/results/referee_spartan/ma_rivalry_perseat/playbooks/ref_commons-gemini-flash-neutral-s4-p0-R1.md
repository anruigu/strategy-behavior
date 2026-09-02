---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 4
round: 1
chars: 738
---
# Fishery Playbook

- In non-final seasons, always submit the exact sustainable share indicated in the prompt (e.g., `[catch: 11.1]`). Do not overfish or deviate from the sustainable share while future seasons remain, as maintaining full stock regrowth maximizes total game yield and keeps other players aligned.
- In the final season, calculate an equal split of the remaining stock among all active boats (`stock / number_of_boats`) and submit that amount (e.g., `[catch: 33.3]` when stock is 100 with 3 boats). There is no future round to preserve stock for, so harvesting the full equal share maximizes final score.
- Always conclude responses strictly with the required format: `[catch: N]`. Keep any preceding text brief and direct.