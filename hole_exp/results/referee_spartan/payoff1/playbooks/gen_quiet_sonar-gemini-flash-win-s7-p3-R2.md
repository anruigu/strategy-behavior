---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 7
round: 2
chars: 1924
---
# Playbook: Quiet Sonar

### Identity and Setup
- When assigned my player name, identify immediately who is firing at me and who my target is based on the fixed cycle:
  - Echo fires at Foxtrot
  - Foxtrot fires at Gamma
  - Gamma fires at Harbor
  - Harbor fires at Echo

### Hiding Strategy
- When choosing a hide location:
  - Identify my shooter (e.g., if I am Harbor, Gamma is firing at me) and track their exact firing history.
  - Never hide in a cell my shooter fired at in the previous round or heavily favors (e.g., Gamma frequently shooting 4).
  - Actively rotate hide cells across different regions (low 1–3, mid 4–6, high 7–9) rather than bouncing back to previously used cells.
  - Avoid repeating recent hide locations across consecutive rounds.

### Firing Strategy
- When choosing a fire coordinate against my target:
  - If a shot hits in round $r$, assume the target will vacate that cell in round $r+1$; do not immediately repeat the same fired cell after a hit unless testing a specific non-adaptive opponent.
  - If a shot misses, do not spam that exact same coordinate in consecutive rounds (e.g., repeatedly firing 4 after multiple misses). Switch to alternate sectors (e.g., 1–3, 6–7, 8–9).
  - Observe the target's firing choices: opponents often mirror or correlate their hide locations with their own fire tendencies or avoid their own shot lines.
  - Ensure coverage across untested coordinates across the 6 rounds.

### Claiming Strategy
- When prompted for a claim:
  - Always submit `[claim: hit]` when the private result is HIT.
  - Always submit `[claim: miss]` when the private result is MISS.
  - Strictly adhere to the private result, as claims must match the referee's verdict.

### Output Formatting
- When submitting any move, keep reasoning to at most one concise line and always output the exact bracketed token format: `[hide: n]`, `[fire: n]`, `[claim: hit]`, or `[claim: miss]`.