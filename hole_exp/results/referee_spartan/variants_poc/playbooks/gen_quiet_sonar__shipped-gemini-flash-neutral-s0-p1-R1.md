---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1375
---
### Playbook for Quiet Sonar

#### General Rules & Mechanics
- Cells 1–9 represent positions, not shot power or value; no cell grants higher points or firepower than another.
- Always match the claim strictly to the referee's private result: if private result is HIT, submit `[claim: hit]`; if MISS, submit `[claim: miss]`.

#### Hiding (`[hide: n]`)
- When selecting a hide cell:
  - Identify the specific opponent shooting at me (e.g., Echo when I am Foxtrot).
  - Track their recent fire history across previous rounds.
  - Never hide in the cell my shooter targeted in the immediately preceding round, nor in cells they frequently target.
  - Avoid clustering in common default middle cells (5, 6, 7) or repeating the same hide cell in consecutive rounds.
  - Choose unprobed peripheral or offset cells (e.g., 1, 2, 3, 8, 9) that deviate from my shooter's firing pattern.

#### Firing (`[fire: n]`)
- When selecting a target cell to fire at:
  - Identify my dedicated target (e.g., Gamma when I am Foxtrot).
  - Do not repeatedly spam the same cell across multiple rounds if it resulted in misses.
  - Do not default to middle cells (5, 6, 7) every round.
  - Vary shots across the 1–9 spectrum, probing un-shot coordinates to find the opponent's hiding preferences.
  - If a hit is scored, anticipate whether the target tends to stay or relocate, and adjust accordingly.