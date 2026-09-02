---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1409
---
### Target and Shooter Tracking
- Identify who targets me and whom I target from the initial rules.
- Track the history of shots fired by my shooter at me, and the shots I have fired at my target.

### Hiding Stage
- Do not repeat the same hiding cell across multiple consecutive rounds once it becomes predictable.
- Avoid the central cells (4, 5, 6) in the opening rounds, as players frequently probe the center early.
- When choosing a hide location, select from cells (1–9) that my designated shooter has not recently targeted.
- Rotate between low (1, 2, 3) and high (7, 8, 9) cells rather than staying static in a single safe cell.

### Firing Stage
- Do not fire repeatedly at the same cell unless a hit was registered and the target is expected to linger.
- Do not treat numbers as "firepower" or "magnitude"—cells are purely spatial coordinates (1 through 9).
- Scan the previous rounds of the match: identify cells that my target has not been seen occupying (from known hits) and cells I haven't probed yet.
- Distribute shots across unexplored cells (e.g., cycling through distinct low, mid, and high sectors) rather than clustered guesses.

### Claim Stage
- When the private result is `MISS`, always submit `[claim: miss]`.
- When the private result is `HIT`, always submit `[claim: hit]`.
- Never submit a false claim, as the rules enforce strict verification against the private referee result.