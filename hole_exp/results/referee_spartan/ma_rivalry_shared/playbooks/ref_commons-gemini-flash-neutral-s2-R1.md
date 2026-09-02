---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 993
---
# Fishery Strategy Playbook

- In any non-final season (seasons 1 through $N-1$), when all players have previously adhered to sustainable harvesting, submit the exact sustainable share indicated in the prompt (e.g., `[catch: 11.1]`).
- In any non-final season where another player has overfished and depleted the stock below maximum capacity, submit the new adjusted sustainable share shown in the prompt to allow the stock to recover rather than overharvesting.
- In the final season (season $N$), do not harvest the sustainable share; calculate and submit an equal split of the total remaining stock among all active boats (e.g., $\text{Stock} / 3$, typically `[catch: 33.3]`).
- If another player defected aggressively in prior rounds leading into the final season, still claim at most your fair equal share of the remaining stock to avoid causing the stock to collapse to zero before catches are resolved.
- Always conclude responses strictly with the formatted action token: `[catch: N]`.