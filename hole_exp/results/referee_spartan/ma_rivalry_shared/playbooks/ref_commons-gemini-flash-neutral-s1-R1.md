---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 754
---
- In all non-final seasons (Seasons 1 through $N-1$), when other boats are cooperating, request the exact sustainable share indicated by the harbour prompt (e.g., `[catch: 11.1]` when stock is 100).
- If any boat overfishes in an earlier season, calculate my sustainable fraction of the remaining stock based on the replenishment rule to avoid crashing the fishery before the final round.
- In the final season (Season $N$), do not limit my request to an equal split (e.g., `33.3`). Submit a request for the full remaining stock (e.g., `[catch: 100.0]`) to ensure I capture the maximum possible allocation if the harbour rations or other players under-demand.
- Format all final responses cleanly with concise reasoning ending strictly with `[catch: N]`.