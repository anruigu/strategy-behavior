---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 7
round: 3
chars: 1923
---
# Playbook: Quiet Sonar

### Identity and Setup
- When assigned my player name, identify immediately who is firing at me and who my target is based on the fixed cycle:
  - Echo fires at Foxtrot
  - Foxtrot fires at Gamma
  - Gamma fires at Harbor
  - Harbor fires at Echo

### Hiding Strategy
- Identify my shooter (e.g., if I am Harbor, Gamma is firing at me) and track their full public firing history.
- Never hide in a cell my shooter targeted in the previous round or heavily repeats/favors (e.g., if Gamma repeatedly shoots 7, strictly avoid 7).
- Actively rotate hide cells across different regions (low 1–3, mid 4–6, high 7–9) rather than bouncing back to recently used cells.
- Avoid repeating recent hide locations across consecutive rounds.

### Firing Strategy
- Track my target's public firing history and recent claim results against their own target:
  - Players often correlate or mirror their hiding choices with their own firing choices or avoid cells they themselves were just shot at.
  - Test diverse coordinates systematically across the 6 rounds without retrying recent misses; avoid spamming the same coordinates (e.g., retrying 7 multiple times if it yielded misses).
  - If a shot hits in round $r$, assume the target will vacate that cell in round $r+1$; switch sectors instead of immediately repeating.
  - If a shot misses, immediately pivot to an unexplored coordinate/sector rather than re-probing nearby numbers.

### Claiming Strategy
- When prompted for a claim:
  - Always submit `[claim: hit]` when the private result is HIT.
  - Always submit `[claim: miss]` when the private result is MISS.
  - Strictly adhere to the private result, as claims must match the referee's verdict.

### Output Formatting
- When submitting any move, keep reasoning to at most one concise line and always output the exact bracketed token format: `[hide: n]`, `[fire: n]`, `[claim: hit]`, or `[claim: miss]`.