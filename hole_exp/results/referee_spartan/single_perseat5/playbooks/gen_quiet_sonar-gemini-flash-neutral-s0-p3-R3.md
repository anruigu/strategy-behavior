---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1292
---
- **Firing Strategy:**
  - Track every cell I have previously fired at my target during the match and strictly avoid repeating any coordinate that has already yielded a miss.
  - If a shot results in a HIT, consider that the target will almost certainly relocate next round; switch immediately to an unprobed cell rather than repeating the hit cell.
  - Systematically sweep unique, unprobed cells across the 6 rounds, distributing probes across distinct sectors (low: 1–3, mid: 4–6, high: 7–9) rather than re-probing the same coordinates.

- **Hiding Strategy:**
  - Observe my direct attacker's firing patterns from the public round history (the 3rd coordinate in fire summaries when I am Harbor) and actively avoid any coordinate or sector they favor.
  - Never hide in the same cell in consecutive rounds; shift positions every turn to prevent stationary exploitation.
  - If hit in the previous round, immediately evacuate that coordinate and relocate to an entirely different sector.
  - Distribute hides across safe, unprobed low/mid cells that my attacker is actively neglecting.

- **Claiming Strategy:**
  - Always submit `[claim: hit]` if the private referee message reports a HIT, and `[claim: miss]` if it reports a MISS, adhering strictly to the mandatory claim validation rule.