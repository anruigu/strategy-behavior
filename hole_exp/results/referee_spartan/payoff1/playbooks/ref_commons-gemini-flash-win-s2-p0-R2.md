---
game: ref_commons
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1357
---
### Playbook: Multi-Season Shared Fishery

- In the final round of the game, take a large harvest to extract maximum value since future regrowth has zero value. Catch at least an equal share of the total remaining stock (e.g., stock / 3), or slightly more if stock permits without risking zeroing out unexpectedly.
- In Season 1, default to a competitive harvest rate slightly above the strict sustainable share if other players are expected to overshoot, or match the highest reasonable baseline immediately rather than starting timidly and lagging behind.
- When other boats consistently harvest above the sustainable baseline in early and middle rounds, match their harvest rate (e.g., 12.0) to avoid conceding cumulative share while stock remains healthy.
- Calculate the total depletion across remaining seasons before choosing catch size:
  - If current stock after a proposed catch round regrows sufficiently to support continued harvests for the remaining seasons without reaching zero, maintain the matched aggressive harvest.
  - If aggregate harvesting threatens to drop the stock dangerously close to zero before the final season, pull back toward the sustainable share to ensure the fishery survives.
- Do not voluntarily harvest below other players' established catches unless the stock is in imminent danger of complete collapse (zero stock).