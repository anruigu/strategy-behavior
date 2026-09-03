---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1442
---
### Playbook: Quiet Sonar

#### 1. Claim Stage
- When given the referee's private outcome at the claim stage:
  - Always claim the exact private result: `[claim: hit]` if the referee told me hit, and `[claim: miss]` if the referee told me miss.
  - Never falsely claim `[claim: hit]` when the referee reports a miss; claims must strictly match the private result.

#### 2. Hide Stage
- Identify the shooter targeting me from the game configuration (e.g., in Echo->Foxtrot->Gamma->Harbor->Echo, Gamma targets Harbor).
- Review public fire history to track the cells fired by my shooter in previous rounds.
- When selecting a hide cell:
  - Never choose cells frequently or recently targeted by my shooter.
  - Mix hiding locations unpredictably across safe, unprobed cells (including perimeter cells like 1, 2, 8, 9, or unvisited mid-range cells).
  - Actively migrate away from cells adjacent to my shooter's recent focus.

#### 3. Fire Stage
- Identify my designated target from the game configuration (e.g., Harbor targets Echo).
- Vary search locations across rounds:
  - Do not repeatedly spam the same cell across multiple rounds if it yields misses.
  - Systematically sweep or probe plausible unprobed cells across the line (1 through 9) to maximize the chance of discovering the target's position.
  - If a hit is achieved, expect the target to relocate in subsequent rounds; adjust aim accordingly rather than stubbornly staying put.