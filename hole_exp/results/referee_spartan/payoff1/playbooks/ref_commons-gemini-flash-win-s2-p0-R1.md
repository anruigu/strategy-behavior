---
game: ref_commons
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1112
---
### Playbook: Multi-Season Shared Fishery

- In the final round of the game, take a large harvest to extract maximum value since future regrowth has zero value. If total stock allows, take up to one-third or more of the remaining stock rather than artificially capping catch at an arbitrary low constant (like 12.0) if the game engine permits higher catches.
- When other boats consistently harvest above the sustainable baseline in early and middle rounds, match their harvest rate to avoid conceding share while stock remains plentiful.
- Calculate the total depletion across remaining seasons before choosing catch size:
  - If current stock after a proposed catch round regrows sufficiently to support continued harvests for the remaining seasons without reaching zero, take the aggressive harvest.
  - If aggregate harvesting threatens to drop the stock close to zero before the final season, pull back toward the sustainable share to ensure the fishery survives.
- Do not voluntarily harvest below other players' established catches unless the stock is in imminent danger of complete collapse (zero stock).