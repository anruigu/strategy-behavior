---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 1
round: 3
chars: 1723
---
### Playbook for Quiet Sonar

- **Claim Stage**:
  - Always submit `[claim: hit]` if the private result is HIT, and `[claim: miss]` if the private result is MISS.
  - Never misreport; claims must strictly match the private referee result.

- **Hide Stage**:
  - Identify who shoots at me from the fixed target cycle (Echo -> Foxtrot -> Gamma -> Harbor -> Echo).
  - Understand the round report format: `Round k: fires e/f/g/h, claims ...` lists the fires of Echo, Foxtrot, Gamma, Harbor in exact player order.
  - Pay attention to whether the shooter hit me last round: if their claim was `hit`, they fired into my exact hide cell.
  - If hit, immediately change hide cells; never repeat the cell where I was just hit.
  - Never camp in the same cell across consecutive rounds (e.g. repeatedly hiding in 2), even if believing it is safe.
  - Actively cycle hides across disparate sectors (low 1–3, mid 4–6, high 7–9), avoiding cells recently targeted by my shooter.

- **Fire Stage**:
  - Track public fire histories and hit claims across the table to deduce player hide locations.
    - If a player was hit by their shooter, their hide location in that round is revealed as that shooter's fired coordinate.
    - Harbor's hide location is revealed whenever Foxtrot's or Echo's firing reports indicate known movement patterns, or when my own shot hits.
  - When my shot results in a MISS, do not repeat that coordinate on the next round. Move to an unexplored cell or predict target movement.
  - If my shot results in a HIT, expect the target to relocate away from that cell in the following round.
  - Actively cycle through untested cells across the 1–9 line rather than clustering multiple shots on the same coordinate.