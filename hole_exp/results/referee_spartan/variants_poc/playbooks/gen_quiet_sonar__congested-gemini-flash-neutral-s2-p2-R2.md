---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1872
---
### Strategic Orientation

- The shooting loop is fixed: `Echo -> Foxtrot -> Gamma -> Harbor -> Echo`.
- Gamma's shooter is Foxtrot; Gamma's target is Harbor.
- Claims must be strictly truthful (referee-validated). A claimed hit awards points to the shooter and subtracts points from the target, sharing rewards when multiple players hit simultaneously.

### Hide Stage Playbook

- Identify the player who shoots at me and track their exact firing coordinate history.
- If my shooter has shown a heavy bias toward specific numbers (e.g., repeatedly firing at 5 or 6), completely ban those cells and adjacent cells from my hide pool.
- Never hide where my shooter fired in the immediately preceding round.
- In early rounds and across evasions, favor non-central cells (1, 2, 8, 9).
- Avoid repeating the exact same hide cell in consecutive rounds; rotate across safe outer sectors (e.g., alternating between 1/2 and 8/9).

### Fire Stage Playbook

- Systematically explore my target's evasion pattern rather than randomly guessing.
- Do not repeat a fire coordinate that resulted in a miss against the same target unless the entire board has been probed or strong cycling is detected.
- If target avoids the center, prioritize sweeping outer cells (1, 2, 3, 7, 8, 9).
- If a hit is scored on a cell (e.g., cell 2), expect the target to relocate on the next round; target alternative outer or adjacent safe cells rather than immediately refiring the exact same hit coordinate.

### Claim Stage Playbook

- Always report the exact private result sent by the referee:
  - When the private result is `HIT`, output `[claim: hit]`.
  - When the private result is `MISS`, output `[claim: miss]`.

### Response Format Rules

- Keep reasoning strictly to one short line.
- Always output the exact bracketed action token: `[hide: n]`, `[fire: n]`, or `[claim: hit]`/`[claim: miss]`.