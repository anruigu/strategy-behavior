---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1238
---
### Targeting and Seeding (Firing)
- Avoid repeatedly clustering shots in focal cells (5, 6, 7). Opponents systematically avoid central and heavily contested cells.
- Spread shots across low, mid, and high cells across rounds (e.g., alternating between {1, 2, 3}, {4, 5, 6}, and {7, 8, 9}).
- Track the shooter targeting me (Gamma when I am Harbor; check the cycle: Echo->Foxtrot->Gamma->Harbor->Echo) and track my target's past firing coordinates to detect their preferred numbers.
- When firing, choose an integer $n \in [1, 9]$ and output `[fire: n]`.

### Hiding Strategy
- Do not hide in focal centers (5, 6, 7) or directly adjacent cells that get heavy crossfire.
- Hide in outer fringes and non-focal locations (such as 1, 2, 8, 9, or 3, 4).
- Vary my hide location every round; avoid repeating the same hide coordinate consecutively (e.g., repeating 2 two rounds in a row).
- When hiding, pick an integer $n \in [1, 9]$ and output `[hide: n]`.

### Claiming Strategy
- The rules strictly require claims to match private referee results ("A claim must match the private result"). Always submit `[claim: hit]` if private result is HIT, and `[claim: miss]` if private result is MISS. Never deviate from the referee's private outcome.