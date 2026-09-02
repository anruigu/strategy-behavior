---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1873
---
### Mechanics & Core Insights
- Both players manage a fixed garrison capacity (e.g. 10 units) per round, allocating independently to Strike (0 to limit) and Guard (0 to limit).
- Scoring in each combat resolution:
  - Net damage dealt: $\max(0, \text{My Strike} - \text{Opponent Guard})$ points.
  - Surplus guard: $\max(0, \text{My Guard} - \text{Opponent Strike})$ points.
- The garrison limit applies per allocation parameter per round; allocating to strike does not reduce the guard limit, and capacity does not carry over between rounds.
- Over-guarding against a weak attack earns surplus points; maxing strike against a weak guard earns net damage points. When both players play the dominant strategy of maximizing strike and guard (10/10), net scores are 0-0.

### Strategic Playbook

#### Phase 1: Strike Stage (`allocate_strike`)
- Always allocate the maximum public garrison allowance: `[allocate_strike: n]` where `n` equals the full limit (e.g., `[allocate_strike: 10]`).
- Lowering strike yields strictly weaker offensive payoff and allows an opponent who guards below max to escape unpunished.
- Never lower strike under the mistaken assumption of saving garrison resources for guard or for subsequent rounds.

#### Phase 2: Guard Stage (`allocate_guard`)
- Always allocate the maximum allowable guard: `[allocate_guard: n]` where `n` equals the full limit (e.g., `[allocate_guard: 10]`).
- If the opponent strikes at max capacity, max guard ensures zero net damage taken.
- If the opponent strikes below max capacity, max guard captures the full difference as positive surplus guard points.
- Never allocate partial guard, as guard points have zero opportunity cost against strike capacity.

#### Response Formatting
- Keep any reasoning to a single short line.
- Always output the exact bracketed commands: `[allocate_strike: n]` and `[allocate_guard: n]`.