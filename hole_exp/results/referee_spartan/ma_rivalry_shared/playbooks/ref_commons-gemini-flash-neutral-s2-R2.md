---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 746
---
# Fishery Strategy Playbook

- In any non-final season (seasons 1 through $N-1$), submit the exact sustainable share indicated in the prompt (e.g., `[catch: 11.1]` when stock is 100.0 across 3 boats).
- If the stock has been depleted below maximum capacity due to prior overfishing, continue to harvest only the adjusted sustainable share shown in the prompt to allow stock recovery.
- In the final season (season $N$), do not harvest the sustainable share; harvest an equal split of the total current stock across all active boats (i.e., $\text{Stock} / B$, which is `[catch: 33.3]` when stock is 100.0 with 3 boats).
- Keep reasoning brief (1–2 sentences) and always conclude the response strictly with the required action format: `[catch: N]`.