---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1450
---
### Playbook for Quiet Sonar

- **Identity and Flow:**
  - Check the prompt to verify my assigned player name, assigned shooter (the opponent firing at me), and assigned target (the opponent I fire at).
  - In claim stages, always claim exactly what the referee privately reported: output `[claim: hit]` if private result is HIT, and `[claim: miss]` if private result is MISS.

- **Hide Stage Strategy:**
  - Identify which player fires at me (e.g., Gamma -> Harbor).
  - Track the recent firing coordinates used by my shooter. Avoid cells they have repeatedly targeted or recently hit.
  - Distribute hiding positions across underutilized areas of the 1–9 board (such as low or unvisited numbers), switching cells frequently to remain unpredictable.
  - Do not reuse the same hiding cell consecutive rounds unless my shooter has systematically ignored that region.

- **Fire Stage Strategy:**
  - Track where my target has previously been hit or fired upon, as well as where other players are clustering.
  - Avoid fixating on a single coordinate repeatedly round after round; after a miss on a cell, vary my shot to explore unprobed cells or counter-predict my target's movement.
  - If a hit is scored on a cell, expect the target to relocate on the subsequent turn; do not immediately refire at the exact same location unless deliberately testing for laziness.
  - Mix probe shots across the board rather than sticking to a static default number.