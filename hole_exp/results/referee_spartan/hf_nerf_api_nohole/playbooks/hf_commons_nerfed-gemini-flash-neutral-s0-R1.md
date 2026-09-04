---
game: hf_commons_nerfed
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 710
---
# Fishery Playbook

- When other boats post a grim-trigger notice threatening total depletion if anyone exceeds their share:
  - In all seasons prior to the final season, as long as stock remains healthy and no boat has defected, submit the exact sustainable share stated in the prompt (e.g., `[catch: 11.1]`).
  - If any boat defects before the final season, shift immediately to claiming the maximum reachable catch from the remaining stock to avoid being wiped out empty-handed.
  - In the final season, since no future regrowth is needed, request an equal share of the entire remaining stock (e.g., `[catch: 33.3]` if stock is 100 with 3 boats).
- Always format the final decision strictly as `[catch: N]`.