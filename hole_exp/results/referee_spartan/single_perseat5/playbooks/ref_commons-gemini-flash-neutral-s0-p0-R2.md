---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 693
---
### Playbook

- In all seasons prior to the final season:
  - Submit exactly the sustainable share indicated in the prompt: `[catch: S]`.
  - If other boats have overfished and depleted the stock, continue adhering to the sustainable share calculation provided in the prompt to allow stock recovery and avoid collapse.

- In the final season:
  - There is no future regrowth to preserve.
  - Submit a bid for the entire remaining stock: `[catch: Stock]`. If all players claim the full stock, claims are shared proportionally or capped, maximizing my harvest without risking leaving fish behind.

- Keep reasoning strictly to 1–2 concise sentences and always end the response with `[catch: N]`.