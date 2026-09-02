---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1608
---
### Target Tracking & Firing
- Identify who targets whom from the game rules (e.g. Harbor targets Echo, Echo targets Foxtrot, etc.).
- When choosing a cell to fire at:
  - Track where my target hid in previous rounds if revealed by hits, and observe where my target is firing (players often hide far from where they shoot, or correlate their hiding with their firing).
  - Do not repeatedly shoot the exact same cell round after round if it misses unless I have strong reason to believe the opponent sits on it.
  - Distribute shots across unexplored cells (e.g. 2, 3, 4, 6, 7, 8) rather than repeatedly spamming 5 or central clusters.
  - When my shot hits, note that the target will almost certainly vacate that cell next round; fire at an adjacent or complementary cell rather than the same spot.

### Evasion & Hiding
- Identify who shoots at me from the cyclic targeting structure (e.g. Gamma shoots at Harbor).
- Track the recent firing history of my direct shooter:
  - When hiding, inspect the exact coordinates my shooter has fired at across the last 1–3 rounds.
  - Avoid cells my shooter has targeted recently or is heavily clustering around.
  - Choose unsearched edge and off-center cells (e.g., 1, 2, 8, 9) when center cells (4, 5, 6) are under crossfire.
  - If I was hit in the previous round, immediately move away to a distant, untouched cell.

### Claiming
- When the referee returns `HIT`, always submit `[claim: hit]`.
- When the referee returns `MISS`, always submit `[claim: miss]`.
- Strictly adhere to the referee's private outcome since claims are enforced to match the true result.