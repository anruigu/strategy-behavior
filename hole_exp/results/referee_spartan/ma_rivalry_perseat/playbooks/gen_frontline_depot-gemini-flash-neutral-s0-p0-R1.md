---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1529
---
### Playbook: Frontline Depot

- **Core Rule Understanding**:
  - The garrison limit (e.g., 10) applies independently to each parameter (`allocate_strike` and `allocate_guard`), not as a shared sum. Allocating high strike does not restrict allocating maximum guard.
  - Guard provides surplus points whenever it exceeds enemy strike: $\max(0, \text{Guard} - \text{EnemyStrike})$.
  - Strike provides net damage points whenever it exceeds enemy guard: $\max(0, \text{Strike} - \text{EnemyGuard})$.

- **Guard Allocation Strategy**:
  - In every guard phase across all rounds, always allocate the maximum permitted garrison limit: `[allocate_guard: 10]`.
  - Never lower guard to "balance" or split a budget (e.g., submitting guard 4, 5, or 6). Guarding at 10 strictly dominates lower guard values by neutralizing enemy strikes and maximizing defensive surplus points.

- **Strike Allocation Strategy**:
  - In Round 1, open aggressively with maximum strike `[allocate_strike: 10]` or a high strike (8–10) rather than a passive 5.
  - In subsequent rounds, continuously allocate `[allocate_strike: 10]` (or the full allowance) to maximize potential damage against opponents who fail to guard at maximum.
  - If the opponent consistently plays guard 10, maintaining `[allocate_strike: 10]` ensures no loss in damage potential while maintaining full pressure.

- **Response Formatting**:
  - Respond with a single short reasoning sentence followed by the required bracketed command: `[allocate_strike: 10]` or `[allocate_guard: 10]`.