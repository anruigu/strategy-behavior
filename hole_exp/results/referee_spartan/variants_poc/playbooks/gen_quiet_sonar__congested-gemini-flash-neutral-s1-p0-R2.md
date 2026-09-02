---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1717
---
# PLAYBOOK: Quiet Sonar (Congested)

### Rules and Mandatory Actions
- When the claim stage prompt appears, always submit the exact private result: `[claim: hit]` if hit, `[claim: miss]` if miss. Never attempt to deviate or bluff on claims.

### Hiding Strategy
- Track the player targeting me (the shooter preceding me in the ring, e.g., Harbor if I am Echo).
- If the shooter targeting me scores a hit, immediately vacate that cell and do not hide in adjacent cells the following round.
- Never camp in the same cell on consecutive turns, but also avoid predictable alternating patterns (e.g., alternating strictly between 1, 2, and 8).
- Avoid cells that my direct shooter has fired upon in the last 2 rounds.
- Distribute hides unpredictably across all non-threatened cells (both interior and edges), rather than overly concentrating on cells 1, 2, and 8.

### Firing Strategy
- Track all cells I have fired at against my target:
  - If a shot results in a **MISS**, strictly eliminate that cell and do not fire at it again in subsequent rounds until all other plausible cells are probed. Never spam the same missed coordinate (e.g., repeating cell 8 repeatedly across rounds 4–6).
  - If a shot results in a **HIT**, evaluate whether the target is likely to stay or flee; if fleeing, shift fire to adjacent or alternate sectors rather than blindly refiring the exact same cell unless target behavior demonstrates stubborn camping.
- Systematically search across distinct sectors (e.g., test 3, 7, 5, 2, 9, 4) to maximize coverage rather than lingering on a single failed quadrant.

### Formatting
- Submit moves immediately using the bracketed tokens `[hide: n]`, `[fire: n]`, `[claim: hit]`, or `[claim: miss]`.