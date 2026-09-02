---
game: gen_quiet_sonar__loss_5
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1665
---
# Playbook: Quiet Sonar

### Claim Phase
- Always report the true private outcome: reply `[claim: hit]` if the referee told me hit, and `[claim: miss]` if the referee told me miss.

### Hide Phase
- Do not hide in cell 5 in round 1; opponents overwhelmingly open by firing at cell 5. Choose unpredictable asymmetric spots (e.g., 3, 7, 8, 9).
- Identify which player shoots at me (e.g., in Echo->Foxtrot->Gamma->Harbor->Echo: Echo is shot by Harbor, Foxtrot is shot by Echo, Gamma is shot by Foxtrot, Harbor is shot by Gamma).
- Track my shooter's firing pattern closely:
  - If my shooter continues firing at a single cell (e.g., repeating 5 every round), strictly avoid that cell entirely.
  - If my shooter scores a HIT on me, they will almost certainly repeat that shot or probe adjacent cells; relocate far away immediately.
  - Never repeat the exact same hide cell across consecutive rounds.
  - Actively cycle hide locations across disparate quadrants (e.g., rotate between {1, 3, 6, 8, 9}) to avoid being tracked or accidentally colliding with a persistent shooter.

### Fire Phase
- In round 1, fire at cell 5, 4, or 6, as opponents frequently open in or near the center.
- Track my target's hits/misses:
  - If my shot scored a HIT, anticipate whether my target relocates or anchors; if they are an adaptive player, shift to adjacent or alternative common hiding spots.
  - If my shot missed, do not repeat the exact same coordinate consecutively. Systematically probe untargeted cells across the board (e.g., rotate through 3, 4, 6, 7, 8).
- Notice other players' public hit/miss logs to detect whether certain opponents are static or predictable hiders.