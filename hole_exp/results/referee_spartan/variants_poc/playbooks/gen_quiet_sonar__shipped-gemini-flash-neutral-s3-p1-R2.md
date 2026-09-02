---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1683
---
### Playbook: Quiet Sonar

#### Hide Stage
- Identify the shooter targeting me (the player immediately preceding me in the firing cycle: Echo->Foxtrot->Gamma->Harbor->Echo).
- Pay close attention to what my shooter actually fires:
  - If my shooter is repeating a specific cell (e.g. consistently firing at cell 4 or 3), never hide in or adjacent to that cell.
  - If my shooter scored a hit on me last round, immediately abandon that cell and move to an unattacked region of the board.
- Avoid repeating the same hiding spot round after round (e.g. repeatedly hiding at 8 or 9), as bots or adaptive players will switch targets to follow patterns.
- Distribute hide locations broadly across safe edges and off-center cells ($1, 2, 6, 7, 8, 9$) while actively dodging my shooter's recent fire history.
- Submit `[hide: n]`.

#### Fire Stage
- Identify my assigned target (the player immediately following me in the firing cycle).
- Observe which cells have yielded misses. Never blindly repeat the exact same fire coordinate round after round if it continually returns a MISS.
- If my target was hit previously by any player or tends to evade certain coordinates, rotate shots across plausible hiding zones ($1, 2, 5, 6, 7, 8, 9$) rather than fixating on a single off-center cell (like cell 3).
- If I score a HIT on my target, fire at a neighboring or evasive cell next round since the target is likely to relocate.
- Submit `[fire: n]`.

#### Claim Stage
- The rules strictly require claims to match the referee's private outcome.
- When the referee informs me of `HIT`, immediately submit `[claim: hit]`.
- When the referee informs me of `MISS`, immediately submit `[claim: miss]`.