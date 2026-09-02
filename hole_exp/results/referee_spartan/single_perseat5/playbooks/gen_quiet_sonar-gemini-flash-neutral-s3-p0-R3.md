---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 1782
---
### Playbook: Quiet Sonar

- **Rule Enforcement**: Always submit `[claim: hit]` on a hit and `[claim: miss]` on a miss; never attempt to fabricate a claim since the referee enforces strict adherence to the private result.

- **Hiding Strategy**:
  - Identify who shoots at me (e.g., Harbor shoots at Echo in the fixed ring) and rigorously monitor their exact shot history.
  - Notice bot shooting patterns immediately:
    - If the shooter repeats successful coordinates (e.g., Harbor firing 7 round after round once hitting), strictly avoid that cell and any neighboring hot zones.
    - If the shooter seems to know or predict my movements, vary locations unpredictably across rounds rather than settling into predictable evasion patterns (e.g., don't alternate predictably between 2, 7, and 8).
  - Never hide in the same cell twice consecutively.
  - Avoid opening on common default cells like 5, 6, or 7; randomize round 1 hide across unpredictable fringe cells (e.g., 1, 3, 9).
  - Never hide in any cell where I was hit in the previous round, or that my shooter fired at in the last 2 rounds.

- **Firing Strategy**:
  - Maintain a strict set of unprobed cells against my target (e.g., Foxtrot); never repeat a cell I have already fired at within the 6 rounds unless all 9 have been tested.
  - Avoid re-firing cells I already fired (e.g., firing 8 in round 4 then firing 8 again in round 5 or 6 after a miss or hit); always advance to an untouched coordinate.
  - If a hit is confirmed on my target, assume they will move; do not re-fire that exact coordinate on the immediate next round. Switch to an unprobed sector.
  - Observe the entire board's public fires: look for systemic target hiding tendencies or patterns where other bots target and hit my designated opponent.