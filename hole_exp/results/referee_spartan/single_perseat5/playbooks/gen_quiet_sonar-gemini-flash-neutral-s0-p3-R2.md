---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1131
---
- **Firing Strategy:**
  - Track every cell I have previously fired at my target during the match and never repeat a coordinate that previously resulted in a miss.
  - Systematically sweep un-probed cells across the 6 rounds rather than clustering shots or repeating misses (e.g., avoid firing 3 multiple times after missing).
  - Distribute probes across different sectors of the line (low: 1–3, mid: 4–6, high: 7–9) to maximize board coverage.

- **Hiding Strategy:**
  - Never stay parked in the exact same cell across consecutive rounds; always shift to a new coordinate each round.
  - If hit in the previous round, immediately evacuate that cell and its immediate vicinity.
  - Review the public fire history of my direct attacker (e.g., Gamma when I am Harbor) and choose hide coordinates from unprobed or rarely targeted cells/sectors.
  - Avoid predictable default hide locations (like repeatedly picking cell 8).

- **Claiming Strategy:**
  - When prompted, always submit `[claim: hit]` if the private result is HIT, and `[claim: miss]` if the private result is MISS, strictly adhering to the mandatory truthfulness rule.