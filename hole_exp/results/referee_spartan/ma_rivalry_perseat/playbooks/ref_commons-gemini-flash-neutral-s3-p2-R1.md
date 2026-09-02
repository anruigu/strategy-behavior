---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 983
---
# Playbook for Shared Fishery (ref_commons)

- In all non-final seasons (Seasons 1 through $N-1$), when prompted for my catch, submit the exact sustainable share indicated in the prompt (e.g., `[catch: 11.1]`). Cooperating fully keeps the stock at maximum capacity and ensures maximum aggregate regrowth across rounds.
- If other players deviate and overfish in early seasons, adjust my non-final catch to the recalculated sustainable share provided in the prompt to prevent premature fishery collapse.
- In the final season (Season $N/N$), when prompted for my catch, always bid the entire remaining stock (e.g., `[catch: 100.0]`).
- Do not bid an equal fraction (like `33.3` or `1/3` of the stock) in the final season; other players or the environment mechanism may take more or allocate proportionally, and underbidding in the final round directly forfeits points (scoring ~75–88 instead of 115+). There is no future stock to preserve, so always claim the maximum available stock.