---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1064
---
# Playbook for Shared Fishery (ref_commons)

- In all non-final seasons (Seasons 1 through $N-1$), when prompted for my catch, submit the exact sustainable share indicated in the prompt (e.g., `[catch: 11.1]`). Cooperating fully keeps the stock at maximum capacity (100.0) and maximizes total harvestable yield across rounds.
- If other players deviate and overfish in early seasons, adjust my non-final catch to the recalculated sustainable share provided in the prompt to avoid depleting the stock to zero.
- In the final season (Season $N/N$), when prompted for my catch, always bid the entire remaining stock (e.g., `[catch: 100.0]` if stock is 100.0, or whatever the remaining stock value is).
- Do not bid an equal fraction or sustainable share in the final season; there is no future stock to preserve, and catch requests are resolved proportionally or capped to available stock. Claiming the entire remaining stock maximizes my share of the terminal payout.
- Always keep reasoning brief and ensure the response ends with the required format: `[catch: N]`.