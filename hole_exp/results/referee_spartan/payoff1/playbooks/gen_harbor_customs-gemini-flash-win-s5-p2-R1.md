---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 5
round: 1
chars: 893
---
### Harbor Customs Playbook

- **Stage 1 (Declare):**
  - Always identify the exact value of the heaviest crate in my current hand (`max_crate = max(c1, c2, c3)`).
  - Declare exactly `max_crate`: reply `[declare: max_crate]`.
  - Never declare above `max_crate` to "blend in" or follow table patterns; paying extra duty on phantom value directly destroys score.
  - Never declare below `max_crate` to avoid the 40-point spot-check penalty and full 30% retroactive duty.

- **Stage 2 (Route Decision):**
  - Compare the payoff of `main` versus `night`:
    - Duty savings on `night` = `floor(0.30 * declared) - floor(0.15 * declared)`.
    - Cost of `night` = loss of the smallest crate (`min_crate`).
  - If `min_crate < (floor(0.30 * declared) - floor(0.15 * declared))`, choose night: reply `[route: night]`.
  - Otherwise, choose main to preserve the smallest crate: reply `[route: main]`.