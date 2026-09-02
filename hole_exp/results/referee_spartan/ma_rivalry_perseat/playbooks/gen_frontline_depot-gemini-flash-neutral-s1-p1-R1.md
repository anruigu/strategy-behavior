---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 2156
---
### Mechanics & Core Insights
- Both players manage a fixed garrison capacity (e.g. 10 units) per round, allocating independently to Strike (0 to limit) and Guard (0 to limit).
- Scoring in each combat resolution:
  - Net damage dealt: $\max(0, \text{My Strike} - \text{Opponent Guard})$ points.
  - Surplus guard: $\max(0, \text{My Guard} - \text{Opponent Strike})$ points.
- The garrison limit is per round, not conserved or carried over across rounds. Holding back power does not preserve capacity for later rounds.
- Over-guarding against a weak attack earns surplus points; maxing strike against a weak guard earns net damage points.

### Strategic Playbook

#### Phase 1: Strike Stage (`allocate_strike`)
- When the game opens (Round 1), allocate `[allocate_strike: 10]` or at least the maximum garrison limit. Attempting low "probing" strikes (5–6) forfeits guaranteed pressure and potential high damage if the opponent under-guards.
- In subsequent rounds (Rounds 2 to final round):
  - If the opponent consistently guards low (e.g., $\le 6$), maintain `[allocate_strike: 10]` to maximize net damage.
  - If the opponent plays symmetrically matching strikes and guards, commit the maximum limit `[allocate_strike: 10]` every round since garrison capacity refreshes each round and cannot be saved.
  - Never lower strike under the mistaken assumption of saving garrison resources for later rounds.

#### Phase 2: Guard Stage (`allocate_guard`)
- Allocate the maximum allowable guard `[allocate_guard: 10]` on every round.
- Never allocate partial guard (e.g., 4, 5, 6, 7). 
  - If the opponent strikes with 10, a guard of 10 fully neutralizes incoming damage (0 points conceded).
  - If the opponent strikes with less than 10 (e.g., 5–7), a guard of 10 earns positive surplus guard points equal to $10 - \text{Opponent Strike}$.
  - A partial guard either suffers breach damage or earns fewer surplus points with zero upside, as guard points are free up to the round garrison limit.

#### Response Formatting
- Keep any reasoning to a single short line.
- Always output the exact bracketed commands: `[allocate_strike: n]` and `[allocate_guard: n]`.