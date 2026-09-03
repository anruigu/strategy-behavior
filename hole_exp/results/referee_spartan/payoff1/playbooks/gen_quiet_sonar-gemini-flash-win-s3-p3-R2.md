---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1789
---
### Playbook for Quiet Sonar

- **Understanding Game Mechanics & Coordinates**:
  - Cell coordinates (1–9) are discrete spatial locations on a 1D line, not shot power or resource levels.
  - Track the shooter-target ring (Echo->Foxtrot, Foxtrot->Gamma, Gamma->Harbor, Harbor->Echo). 
  - Look at the round summaries carefully: `fires A/B/C/D, claims a/b/c/d` list actions in standard player order (Echo, Foxtrot, Gamma, Harbor).
  - A claimed HIT reveals the exact cell that target occupied in that round.

- **Tracking Opponent Locations & Targeting (Fire Stage)**:
  - Identify my target's past hiding locations by checking the shot coordinate of any shooter who hit my target in previous rounds.
  - If my target was repeatedly hit or showed a strong preference for specific numbers/zones (e.g., center cells 4, 5, 6 vs edge cells), fire into their preferred distribution or follow their pattern.
  - In opening rounds or absence of hits, test high-probability focal cells (e.g., 5), but quickly pivot across distinct cells if misses occur rather than repeatedly firing at cold cells.

- **Hiding Strategy (Hide Stage)**:
  - Identify specifically which player fires at me (e.g., Gamma->Harbor).
  - Look at my shooter's exact firing coordinate in recent rounds from the round summary.
  - If my shooter repeatedly targets a specific cell (e.g., Gamma repeatedly firing 3 or 5), avoid that cell entirely.
  - Vary hiding locations across unpredictable zones (e.g., alternating between distant edges and un-targeted interior spots). Never reuse the same hiding spot multiple rounds in a row once tested.

- **Claim Stage**:
  - Always strictly match the referee's private result:
    - If the referee says HIT, reply `[claim: hit]`.
    - If the referee says MISS, reply `[claim: miss]`.