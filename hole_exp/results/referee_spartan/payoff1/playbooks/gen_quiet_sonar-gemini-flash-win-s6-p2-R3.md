---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 6
round: 3
chars: 1831
---
### Playbook for Quiet Sonar

- **Claiming Rules**:
  - When the referee reports `MISS`, always submit `[claim: miss]`.
  - When the referee reports `HIT`, always submit `[claim: hit]`.
  - Strictly report the referee's private verdict as claims must match true results.

- **Understanding History & Roles**:
  - Shooter/Target cycle is: Echo -> Foxtrot -> Gamma -> Harbor -> Echo.
  - Round summary format is `Echo/Foxtrot/Gamma/Harbor` for both fires and claims.
  - Note bot behavior: Bots frequently mimic where they themselves hide or follow clear deterministic patterns across rounds (e.g. static cells, mirroring fire coordinates).

- **Hiding Strategy**:
  - Look at the shooter targeting me (e.g., if I am Gamma, Foxtrot targets me; Foxtrot is index 2 in the history).
  - Track the exact cell the shooter targeted last round. If the shooter hits, they will often predict or adjust; avoid predictable patterns like switching between just 1 and 7/9.
  - Actively cycle between distinct non-adjacent cells (e.g., 2, 8, 3, 6) rather than repeatedly toggling between 1 and 9.

- **Firing Strategy**:
  - Harbor is targeted by Gamma (index 3 in fire list). Harbor fires at Echo (index 4 in fire list).
  - Bots often hide in the exact cell they fire at, or follow the locations where other bots successfully hit.
  - Never repeat a fired cell if it resulted in `MISS` in recent rounds. Systematically probe un-fired cells across the grid (e.g., test 3, 4, 6, 8, 2) rather than re-firing 5 or 7 repeatedly.
  - If a shot on a target results in `HIT`, immediately fire at that exact cell again next round to punish stationary targets.

- **Formatting**:
  - Always respond strictly with the requested bracketed format (`[hide: n]`, `[fire: n]`, `[claim: hit]`, or `[claim: miss]`) preceded by at most one brief line of reasoning.