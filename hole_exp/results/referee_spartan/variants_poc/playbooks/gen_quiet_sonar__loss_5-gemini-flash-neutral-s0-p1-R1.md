---
game: gen_quiet_sonar__loss_5
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1247
---
### Claims
- Always submit the exact result revealed by the referee:
  - If the private result is `MISS`, reply with `[claim: miss]`.
  - If the private result is `HIT`, reply with `[claim: hit]`.
- Never claim `hit` when the private result is `MISS`; false claims are illegal per game rules and lead to direct score penalties.

### Hiding
- Vary hide locations across rounds to remain unpredictable.
- Avoid repeatedly camping in a single cell (e.g., cell 2) round after round.
- Check the recent firing history of the player shooting at me. Do not hide in cells they have recently targeted, especially cells where they previously scored a hit against me.
- Mix hiding across edges (1, 9), intermediate cells (2, 3, 7, 8), and center cells (4, 5, 6) pseudo-randomly.

### Firing
- Coordinate numbers represent grid cells (1 to 9), not fire power or damage magnitude. Do not fire 8 or 9 under the assumption of higher impact.
- Avoid firing repeatedly into known empty cells if the target is likely moving.
- Track my target’s historical hiding patterns and firing history to probe plausible unvisited locations.
- Mix fire coordinates across the 1–9 range to search the line systematically rather than clustering purely in high or middle numbers.