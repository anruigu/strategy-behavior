---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 3
round: 3
chars: 1952
---
### Playbook for Quiet Sonar

- **Understanding Game Mechanics & Coordinate Tracking**:
  - Cell coordinates (1–9) are discrete spatial locations on a 1D line.
  - The firing ring is fixed: Echo->Foxtrot, Foxtrot->Gamma, Gamma->Harbor, Harbor->Echo.
  - The round summary format `fires A/B/C/D, claims a/b/c/d` lists actions strictly in player order (Echo, Foxtrot, Gamma, Harbor).
  - Every player whose shooter claimed a `hit` had their exact location revealed: the shooter's coordinate in that round is the exact cell where that player hid.
  - Every player whose shooter claimed a `miss` was definitively NOT at the fired coordinate.

- **Targeting Strategy (Fire Stage)**:
  - Check whether my target was hit in recent rounds. If their shooter hit them, note the exact cell they hid in.
  - Track target behavioral tendencies: do they stay static, oscillate between a few cells, step sequentially, or avoid previous hit locations?
  - If my target was not hit recently, deduce where they were NOT from past misses by their shooter (and my own past shots).
  - Never repeat a fired coordinate against a target if recent misses or target patterns show they are not there. Systematically probe untargeted candidate cells.

- **Hiding Strategy (Hide Stage)**:
  - Identify who shoots at me (e.g., Gamma shoots Harbor).
  - Analyze my shooter's firing pattern from the summary (e.g., repeating the same cell, shifting by +/-1, or scanning).
  - If my shooter repeatedly fires at a specific cell or region, actively hide far away in cells they have not touched.
  - If I was hit last round, immediately relocate to a different sector.
  - Avoid predictable stationary hides or repeating the same hide location in consecutive rounds.

- **Claim Stage**:
  - Submitting false claims is illegal. Always strictly match the referee's private verdict:
    - If the referee says HIT, reply `[claim: hit]`.
    - If the referee says MISS, reply `[claim: miss]`.