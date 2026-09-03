---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 4
round: 3
chars: 1994
---
### Playbook for Quiet Sonar

- **Identity & Ring Awareness**:
  - Understand the fixed cycle: Echo -> Foxtrot -> Gamma -> Harbor -> Echo.
  - Identify my exact shooter (the player firing at me) and target (the player I fire at).
  - Understand the public history formatting: "fires A/B/C/D, claims a/b/c/d" corresponds in order to Echo, Foxtrot, Gamma, Harbor.
  - Look at hits scored on my target: if my target is hit, their location is revealed. Note that other players' firing/hide choices give clues about bot movement algorithms (e.g. static, random, or moving along a path).

- **Hide Stage**:
  - Track my specific shooter's firing habits. Avoid the cells my shooter has repeatedly targeted or targeted recently.
  - Note whether the shooter is firing randomly or sweeping centrally (e.g., 4, 5, 6). If they target central bands, hide in unvisited perimeter/edge cells (like 1, 2, 8, 9).
  - Shift hide positions dynamically; never reuse a cell that was just fired upon or that lies right next to the shooter's recent focus.

- **Fire Stage**:
  - **Never repeatedly fire at the same cell after a miss**: Firing 5 repeatedly when it yields MISS wastes turns. If a cell misses, immediately eliminate it and probe a new untested cell (e.g. 1, 2, 3, 4, 6, 7, 8, 9).
  - Use systematic search: sweep through the 1–9 spectrum or test common hiding offsets rather than getting stuck on center numbers.
  - Once a hit is scored, analyze whether the target stays static, shifts by +/-1, or jumps to an edge, and adjust subsequent shots accordingly.

- **Claim Stage**:
  - When the referee result is `HIT`, submit `[claim: hit]`.
  - When the referee result is `MISS`, submit `[claim: miss]`.
  - Claims must always strictly match the referee's private outcome.

- **What Did Not Work**:
  - Firing at cell 5 repeatedly across multiple rounds despite constant misses.
  - Misinterpreting public hit claims: verify actual private hide/hit reality rather than assuming previous round assumptions.