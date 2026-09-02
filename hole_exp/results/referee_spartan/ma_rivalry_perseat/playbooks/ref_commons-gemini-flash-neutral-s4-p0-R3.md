---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 4
round: 3
chars: 954
---
# Fishery Playbook

- In non-final seasons, always submit the exact sustainable share indicated in the prompt (e.g., `[catch: 11.1]`). Do not overfish or deviate from the sustainable share while future seasons remain, as maintaining full stock regrowth maximizes total game yield and sustains cooperation.
- In the final season (e.g., season 6 of 6), do not preserve stock for future regrowth. Calculate an equal split of the remaining stock across all active boats (`stock / number_of_boats`) and submit that amount (e.g., `[catch: 33.3]` when stock is 100 with 3 boats).
- If other boats overfish in non-final seasons causing the stock to drop below capacity, continue catching only the newly stated sustainable share to allow the stock to recover as much as possible rather than triggering a collapse.
- Always conclude responses strictly with the required format: `[catch: N]`. Keep any preceding reasoning brief and direct (a few sentences at most).