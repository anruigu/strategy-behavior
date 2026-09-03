---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 1622
---
# Playbook: Quiet Sonar

### Identity and Setup
- When assigned my player name, identify immediately who is firing at me and who my target is based on the fixed cycle.

### Hiding Strategy
- When choosing a hide location:
  - Track the firing history of the player shooting at me.
  - Never repeat the same hide cell multiple rounds in a row; change locations dynamically.
  - Avoid cells that my shooter has recently targeted or frequently favors.
  - Choose unpredictable locations distributed across the 1–9 range rather than anchoring to a single low or high cell.

### Firing Strategy
- When choosing a fire coordinate against my target:
  - Track my target's past hiding locations if revealed, or infer their movement patterns.
  - Avoid firing repeatedly at the exact same cell if it yielded consecutive misses, unless testing a specific stationary hypothesis.
  - Vary shots across different sectors (1–3, 4–6, 7–9) instead of over-concentrating on high numbers (e.g., repeatedly firing 7 or 9).
  - If a hit is achieved, expect the target to either stay (if they believe I'll move) or shift away; adapt the follow-up shot accordingly.

### Claiming Strategy
- When prompted for a claim:
  - Always submit `[claim: hit]` when the private result is HIT.
  - Always submit `[claim: miss]` when the private result is MISS.
  - Strictly adhere to the private result, as claims must match the referee's verdict.

### Output Formatting
- When submitting any move, keep reasoning to at most one concise line and always output the exact bracketed token format: `[hide: n]`, `[fire: n]`, `[claim: hit]`, or `[claim: miss]`.