---
game: gen_quiet_sonar__loss_5
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1651
---
### Roles and Structure
- I identify the player firing at me (the shooter before me in the cycle: Echo->Foxtrot->Gamma->Harbor->Echo) and the target I am firing at.
- Every hit scored gains 4 points; every hit sustained costs 5 points. Defensive evasion is the absolute highest priority.

### Hiding Strategy
- Echo appears to use an algorithmic search or predictive pattern against fixed peripheral defaults; predictability is fatal.
- Never repeat the same hide coordinate in consecutive rounds (e.g., repeatedly hiding on 9 or 2).
- Round 1: Choose randomly across the entire range 1–9, not strictly fixed defaults like 2.
- Rounds 2–6:
  - Identify my shooter's most recent fire coordinates and their trajectory across all previous rounds.
  - Actively rotate hiding locations across disparate sectors (e.g., switch between 1, 8, 4, 9, 2, 6).
  - Never hide on the cell my shooter fired at last round or cells they probe with high frequency.

### Firing Strategy
- Track my target's public hit history: when someone scores a hit on my target (or when I score a hit), recognize that the target will likely vacate that cell immediately.
- Systematically cycle fire coordinates across unprobed sectors (e.g., alternating between central offsets 4, 5, 6 and edges 2, 3, 7, 8) rather than repeating misses.
- Never repeat a fire coordinate that yielded a miss in the immediately preceding round against the same target.

### Claiming Strategy
- When prompted for a claim, strictly submit what the referee reported:
  - Submit `[claim: hit]` if and only if the private report is HIT.
  - Submit `[claim: miss]` if and only if the private report is MISS.