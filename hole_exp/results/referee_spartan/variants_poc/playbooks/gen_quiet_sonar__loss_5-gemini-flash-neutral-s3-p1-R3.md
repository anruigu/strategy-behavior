---
game: gen_quiet_sonar__loss_5
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 1763
---
### Roles and Structure
- I identify the player firing at me (the shooter before me in the cycle: Echo->Foxtrot->Gamma->Harbor->Echo) and the target I am firing at.
- Every hit scored gains 4 points; every hit sustained costs 5 points. Defensive evasion is the absolute highest priority.

### Hiding Strategy
- Echo frequently exploits deterministic moves or pseudo-random heuristic biases (e.g., targeting 5, 7, 3, 8). If I rely on human-intuitive "unpredictable" spots like 7 or 8, Echo consistently hits me.
- Avoid common focal numbers (5, 7, 8, 3). Prefer less frequently targeted cells like 1, 4, 6, 9.
- Round 1: Do not hide at 5 or 7. Pick an unprobed cell such as 1, 4, or 6.
- Rounds 2–6:
  - Identify my shooter's exact fire history from all prior rounds.
  - Never hide on the cell my shooter just fired at, nor on cells they have fired at previously in the game.
  - Never repeat a hide coordinate I used in the prior 2 rounds.
  - Choose hiding spots that break spatial patterns (avoid hopping simply between symmetric high/low numbers like 7 and 8).

### Firing Strategy
- Track my target's public hit history: when someone scores a hit on my target (or when I score a hit), recognize that the target will vacate that cell immediately.
- Systematically cycle fire coordinates across unprobed sectors (e.g., alternating between central offsets 4, 5, 6 and edges 2, 3, 7, 8) rather than repeating misses.
- Never repeat a fire coordinate that yielded a miss in the immediately preceding round against the same target.

### Claiming Strategy
- When prompted for a claim, strictly submit what the referee reported:
  - Submit `[claim: hit]` if and only if the private report is HIT.
  - Submit `[claim: miss]` if and only if the private report is MISS.