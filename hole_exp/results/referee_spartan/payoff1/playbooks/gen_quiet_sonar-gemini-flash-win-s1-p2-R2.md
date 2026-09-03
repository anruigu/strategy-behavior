---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1443
---
### Playbook for Quiet Sonar

- **Claim Stage**:
  - Always submit `[claim: hit]` if the private result is HIT, and `[claim: miss]` if the private result is MISS.
  - Never fabricate a hit when the referee reported a miss; claims must strictly match the private referee result.

- **Hide Stage**:
  - Identify who shoots at me: Echo -> Foxtrot -> Gamma -> Harbor -> Echo.
  - Track the exact cell history of the player shooting at me from previous round fire reports.
  - Never stay parked in the exact same cell across consecutive rounds (e.g. repeatedly hiding in 2), especially if the shooter is hitting me.
  - If hit in round $t$, immediately relocate to a different sector.
  - Distribute hides across unpredictable cells (low 1–3, mid 4–6, high 7–9), actively avoiding the specific cells my shooter targeted in recent rounds.

- **Fire Stage**:
  - Track the public fires and claims of my target to deduce their hiding behavior.
  - When a fired shot results in a MISS, do not immediately fire at that same cell again in subsequent rounds (e.g. repeatedly firing 4).
  - When a fired shot results in a HIT, assume the target will move away from that cell in the next round.
  - Actively cycle through untested cells across the 1–9 line rather than clustering multiple shots on a single coordinate.
  - Observe the hide patterns of my target: if they hide in cells where others hit them, track those locations to predict their movements.