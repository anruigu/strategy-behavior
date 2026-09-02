---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 617
---
### Playbook

- In all seasons prior to the final season:
  - Submit exactly the sustainable share indicated in the prompt: `[catch: S]`.
  - If other boats have overfished and depleted the stock, continue adhering strictly to the sustainable share calculation provided in the prompt to allow stock recovery and avoid fishery collapse.

- In the final season:
  - There is no future regrowth to preserve.
  - Submit a bid for the entire remaining stock: `[catch: Stock]`.

- Format requirements:
  - Keep reasoning strictly brief (1–2 sentences).
  - Always end the reply with the required token format: `[catch: N]`.