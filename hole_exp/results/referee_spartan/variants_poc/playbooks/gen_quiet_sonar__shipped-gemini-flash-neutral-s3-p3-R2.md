---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1768
---
### Targeting and Seeding (Firing)
- Avoid repeatedly clustering shots in focal cells (5, 6, 7). Opponents systematically avoid central and heavily contested cells.
- Actively sample across low, mid, and high cells across rounds (e.g., alternating between {1, 2, 3}, {4, 5, 6}, and {7, 8, 9}). Do not repeat the exact same fired cell consecutively if it returned a miss.
- Look at the target's firing choices: opponents often use their own favorite hide numbers when choosing fire targets, or vice versa.
- Track my target's past firing coordinates to detect their preferred numbers and probe those cells.
- When firing, choose an integer $n \in [1, 9]$ and output `[fire: n]`.

### Hiding Strategy
- Track the shooter targeting me (Gamma when I am Harbor; check the cycle: Echo->Foxtrot->Gamma->Harbor->Echo).
- Identify the shooter targeting me from the public history (the 3rd coordinate in the public fire summary when I am Harbor) and avoid cells they have recently fired at or frequently target (e.g., if Gamma repeatedly shoots 3, 4, 6, stay away from 3, 4, 6).
- Do not hide in focal centers (5, 6, 7) or directly adjacent cells that get heavy crossfire.
- Hide in outer fringes and non-focal locations (such as 1, 2, 8, 9).
- Vary my hide location across rounds; avoid repeating the exact same hide coordinate consecutively unless historical fire from my attacker never touches that coordinate.
- When hiding, pick an integer $n \in [1, 9]$ and output `[hide: n]`.

### Claiming Strategy
- The rules strictly require claims to match private referee results ("A claim must match the private result"). Always submit `[claim: hit]` if the private result is HIT, and `[claim: miss]` if the private result is MISS. Never deviate from the referee's private outcome.