---
game: ref_commons
model: gemini-flash
condition: win
seed: 2
round: 3
chars: 1322
---
### Playbook: Multi-Season Shared Fishery

- In the final round of the game (Season 6/6), take a large harvest to extract maximum value since future regrowth has zero value. Claim at least an equal share of the total remaining stock (`stock / num_boats`), rounded to one decimal place, or take a larger share if other players are predictable or conservative.
- In Season 1, default to a competitive harvest rate slightly above the strict sustainable share (e.g., 12.0 when sustainable is 11.1) to avoid lagging behind if opponents set a higher pace, while leaving enough stock for strong 50% regrowth.
- When other boats establish a stable harvest rate in early and middle rounds (e.g., 12.0 each), match their rate to maintain exact parity without conceding cumulative score.
- Before submitting each season's catch, evaluate the trajectory to the final round:
  - If current stock after proposed catches regrows sufficiently to sustain positive harvests through Season 6, maintain the matched catch pace.
  - If aggregate harvesting threatens to drop the stock to zero before the final season, reduce harvest toward the sustainable share to preserve the stock.
- Do not voluntarily harvest below other players' established catch levels unless the stock is in imminent danger of complete collapse before the final season.