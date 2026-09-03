---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 7
round: 3
chars: 1547
---
- When the claim stage prompt appears, I always submit `[claim: hit]` if the referee told me HIT, and `[claim: miss]` if the referee told me MISS. I never submit a false claim, as claims are strictly required to match the private result.

- When the hide stage prompt appears:
  - Identify who targets me (e.g., Echo->Foxtrot) and review their past shots and hit pattern.
  - If my shooter is an omniscient or highly predictive opponent repeatedly landing hits regardless of basic relocations, randomize across the full 1–9 range without relying on predictable heuristics (like alternating edges or fleeing only to corners 1, 2, 8, 9).
  - Avoid predictable patterns such as repeatedly hiding in the same cell across consecutive rounds or alternating between just two favorite cells.
  - Do not assume mid-range cells (4–6) or edge cells (1–2, 8–9) are inherently safe; actively vary position across distinct sectors (1–3, 4–6, 7–9) each round.

- When the fire stage prompt appears:
  - Identify my target (e.g., Foxtrot->Gamma) and track what cells have already been probed and missed.
  - Diversify shot selection across the board (1 through 9); avoid repeatedly firing into the same cell (e.g., repeating 4 or 6) across consecutive rounds when receiving repeated misses.
  - Mix probes across both central cells (4–6) and outer flanks (1–3, 7–9) systematically rather than clustering consecutive shots within the same narrow sector.
  - If a target was hit on a previous round, expect them to relocate away from that specific cell immediately.