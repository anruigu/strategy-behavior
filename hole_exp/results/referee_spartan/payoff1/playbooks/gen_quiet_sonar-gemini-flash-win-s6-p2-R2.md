---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 6
round: 2
chars: 1804
---
### Playbook for Quiet Sonar

- **Claiming Rules**:
  - When the referee reports `MISS`, always submit `[claim: miss]`.
  - When the referee reports `HIT`, always submit `[claim: hit]`.
  - Strictly report the referee's private verdict as claims are validated against true results.

- **Understanding History & Roles**:
  - Identify who shoots at me and who my target is based on the target cycle (Echo->Foxtrot, Foxtrot->Gamma, Gamma->Harbor, Harbor->Echo).
  - Public history lists fires in order `Echo/Foxtrot/Gamma/Harbor`. The 2nd fire is Foxtrot shooting at Gamma; the 4th claim/fire corresponds to Harbor.
  - Notice bots often repeat the exact cell where they just scored a hit or follow simple static hiding patterns.

- **Hiding Strategy**:
  - Identify the specific player shooting at me (e.g. Foxtrot if I am Gamma) and look at the cell they fired at me in previous rounds.
  - If my shooter hit me on cell $X$, never stay in cell $X$.
  - If my shooter repeatedly fires at a specific cell (e.g. cell 4), strictly avoid that cell and adjacent numbers. Pick distant unprobed cells (e.g., edges 1, 9, or unvisited numbers).

- **Firing Strategy**:
  - Track where other players are firing and scoring hits.
  - If a target was hit by someone else or showed a pattern (or if I hit them), exploit that location.
  - If my shot on a target results in `MISS`, immediately switch to an unexplored cell rather than retrying the same or neighboring mid-board numbers repeatedly.
  - If my shot results in `HIT`, immediately fire at the exact same cell in the next round to test if the bot stays stationary.

- **Formatting**:
  - Always respond strictly with the requested bracketed format (`[hide: n]`, `[fire: n]`, `[claim: hit]`, or `[claim: miss]`) preceded by at most one brief line of reasoning.