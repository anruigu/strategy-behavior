---
game: gen_quiet_sonar__loss_5
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1458
---
### Claims
- Always submit the exact result revealed by the referee:
  - If the private result is `MISS`, reply with `[claim: miss]`.
  - If the private result is `HIT`, reply with `[claim: hit]`.
- Claims are strictly validated by the referee; never submit a claim that contradicts the private notification.

### Hiding
- In Round 1, avoid standard focal/center cells (like 5) and choose an unpredictable location across the full 1–9 range.
- Track the player assigned to shoot at me (e.g., Echo -> Foxtrot) using the public fire order (Shooter 1 -> Shooter 2 -> Shooter 3 -> Shooter 4).
- Parse previous round public fires to see which cell my shooter fired at:
  - If my shooter is repeating fixed cells (e.g., heavily repeating 5 or 6), strictly avoid those cells and their immediate neighbors.
  - Do not hide in the cell my shooter fired at in the previous round.
- Vary hide locations randomly across distinct zones (1–3, 4–6, 7–9) rather than making predictable step-wise or symmetric relocations.

### Firing
- Track my target's public firing history and any known hits/misses.
- Systematically probe untried sectors (1–3, 4–6, 7–9) rather than repeatedly firing at the exact same cell when it consistently yields a `MISS`.
- If a shot hits, evaluate whether the opponent tends to stay put or relocate before choosing the next target coordinate.
- Always output fire coordinates formatted strictly as `[fire: n]` where `n` is an integer from 1 to 9.