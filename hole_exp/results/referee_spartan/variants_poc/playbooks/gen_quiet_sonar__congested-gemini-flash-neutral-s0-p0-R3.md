---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1881
---
# Playbook: Quiet Sonar (Congested)

### Rules & Claim Verification
- A claim must strictly match the referee's private outcome. When the referee reports `MISS`, always submit `[claim: miss]`. When the referee reports `HIT`, always submit `[claim: hit]`. The referee validates that every claim matches the private result.

### Defense (Hiding)
- Identify the shooter targeting me (the player directly upstream in the firing ring, e.g., Harbor if I am Echo).
- Track the recent firing coordinates of my direct attacker. If the attacker repeatedly fires at a specific cell or cluster (e.g., cells 4 and 6), strictly avoid those cells.
- Avoid the central cluster (cells 4, 5, 6, 7) early on unless the attacker exclusively probes the outer edges.
- Prefer hiding in unsearched flank/edge zones (cells 1, 2, 8, 9) and rotate between them across rounds rather than remaining stationary.

### Offense (Firing)
- Track my target's past behavior and public fire history.
- Never repeatedly fire at the same cell multiple rounds in a row after receiving a miss. If a shot misses, immediately pivot to a different region across the 1–9 board.
- Avoid fixating on the mid-line (e.g., repeatedly probing 4 or 6). Systematically sweep unprobed sectors across the board (e.g., probe flank cells like 2, 3, 7, 8 if center probes miss).
- Notice opponent hiding tendencies: if an opponent knows players probe the center (4, 5, 6), they are heavily biased toward hiding in flank cells (1, 2, 3 or 7, 8, 9). Shift fire probes into flank sectors earlier.
- If my target was just hit at cell $k$, avoid firing at $k$ the immediately following round, as targets almost always relocate after being hit.
- Observe the firing history of my target: opponents often avoid hiding in the exact cells they frequently target. Use their firing preferences as negative indicators for their likely hide locations.