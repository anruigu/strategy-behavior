---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1812
---
### Target Tracking & Firing
- Identify who targets whom from the game setup (e.g. Echo->Foxtrot, Foxtrot->Gamma, Gamma->Harbor, Harbor->Echo).
- Track the public firing history and claimed hits of all players to deduce opponents' hiding patterns:
  - When my target is hit by their shooter, that reveals their exact hiding location for that round.
  - Look at my target's own firing coordinate: many players hide in the exact cell they fire from, or stay within 1 cell of their own shot. If blind, probing the cell my target fired at in the previous round is a strong candidate.
  - Avoid repeatedly firing at central cells (like 4, 5, 6, 7) if they consistently miss; expand searches to outer cells (1, 2, 3, 8, 9) or track where other shooters are finding hits.
  - If my shot hits, assume the target will vacate that cell in the next round; shift fire to an adjacent or correlated position.

### Evasion & Hiding
- Identify who shoots at me from the cyclic targeting structure (e.g., Gamma shoots at Harbor).
- Track the firing coordinates of my direct shooter across previous rounds:
  - Never hide in cells my direct shooter targeted in recent rounds or cells they frequently re-probe (e.g., if they heavily fire at 7 and 8, stay in the low band like 1, 2, 3).
  - Vary my hiding spot between safe off-center and corner cells (e.g., 1, 2, 9) rather than camping indefinitely in a single cell (like repeatedly staying on 2), which risks being caught by a sweep.
  - If I am hit in round 1 or any subsequent round, immediately relocate to a distant, unprobed quadrant.

### Claiming
- When the referee returns `HIT`, always submit `[claim: hit]`.
- When the referee returns `MISS`, always submit `[claim: miss]`.
- Strictly match the referee's private outcome since claims are validated against ground truth.