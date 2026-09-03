---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1167
---
### Playbook for Quiet Sonar

- **Claim Stage**:
  - Always submit `[claim: hit]` if the private result is HIT, and `[claim: miss]` if the private result is MISS.
  - Never fabricate a hit when the referee reported a miss; invalid/false claims can invalidate scoring or carry penalties.

- **Hide Stage**:
  - Track the firing pattern of the player targeting me (the shooter directly targeting my seat).
  - Actively avoid cells and regions they frequently target.
  - Do not repeatedly hide in the exact same cell round after round if the shooter is varying their shots or closing in on that zone.
  - Mix hiding locations randomly across low (1–3), mid (4–6), and high (7–9) cells to remain unpredictable.

- **Fire Stage**:
  - Track where my target has previously been hit or missed, and vary my shots across the 1–9 range instead of repeatedly firing at the same high numbers (e.g., repeatedly firing at 8).
  - If a target consistently avoids high numbers, shift fire into the lower or middle register (1–4).
  - Use pseudo-random distribution across untested cells rather than relying on intuitive heuristics like "firing at maximum intensity" on high numbers.