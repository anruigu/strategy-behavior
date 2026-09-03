---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1616
---
### Playbook for Quiet Sonar

- **Understanding Coordinates vs. "Power"**:
  - Cell coordinates (1–9) are discrete spatial locations on a 1D grid, not shot power or resource levels. Do not choose higher numbers thinking they deal more damage or have higher impact.

- **Tracking Opponent Locations (Fire Stage)**:
  - When deciding where to fire at my target, analyze past rounds:
    - If a target was hit by a previous shooter's shot at cell $X$, they were confirmed at cell $X$ in that round.
    - Track the firing patterns of the player targeting my target, as well as the public claim history.
    - Avoid clustering exclusively on high cells (7, 8, 9) unless target history suggests they hide there; diversify shots across 1–9 using pseudo-random distribution or specific reads on target behavior.

- **Hiding Strategy (Hide Stage)**:
  - Identify the player assigned to shoot at me (e.g., if Gamma shoots Harbor, track Gamma's firing history).
  - Check the cells my shooter has repeatedly fired at in recent rounds and never hide in those exact cells or their immediate neighborhood.
  - When opponents show a heavy bias toward high cells (7–9) or middle cells (4–6), hide in the cold zones (e.g., 1, 2, 3) and vary the choice each round to remain unpredictable. Never repeat the exact same hiding cell in consecutive rounds.

- **Claim Stage**:
  - When the referee informs me of the true shot result:
    - If the referee says HIT, reply `[claim: hit]`.
    - If the referee says MISS, reply `[claim: miss]`.
  - Always strictly match the referee's private result since claims are validated and mandatory.