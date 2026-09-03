---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 1427
---
### Playbook: Harbor Customs

**Declaration Strategy:**
- When dealt three crates, sort them into `[min_crate, mid_crate, max_crate]`.
- Always declare exactly `max_crate`: `[declare: max_crate]`. 
  - Never declare more than `max_crate` (such as total hold value or arbitrary higher amounts), because excess declaration increases duty without reducing risk.
  - Never declare less than `max_crate`, as any value below `max_crate` triggers the -40 penalty and full recomputed duty upon spot check.

**Route Choice Strategy:**
- Compare net payoffs for `main` vs `night` given declaration $D = \text{max\_crate}$:
  - `main` net gain: $(\text{min\_crate} + \text{mid\_crate} + \text{max\_crate}) - \lfloor 0.30 \times D \rfloor$
  - `night` net gain: $(\text{mid\_crate} + \text{max\_crate}) - \lfloor 0.15 \times D \rfloor$
  - Difference (`night` minus `main`): $(\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor) - \text{min\_crate} \approx 0.15 \times D - \text{min\_crate}$.
- When $\text{min\_crate} < \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$, reply `[route: night]`.
- Otherwise, reply `[route: main]`.

**What Did Not Work:**
- Over-declaring above `max_crate` (e.g., declaring true total hold value or 35 when `max_crate` was 22) wasted points directly on surplus duty payments.
- Defaulting blindly to `[route: main]` every round forfeited point savings on low-value smallest crates.