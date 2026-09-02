---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 4
round: 3
chars: 1235
---
### Playbook

- **Stage 1 (Declare):**
  - Always declare the exact value of my heaviest crate in the current hold: `[declare: max_crate]`.
  - Never declare below the heaviest crate; doing so triggers a -40 point penalty and recalculates duty at 30% of total hold value.
  - Never declare above the heaviest crate (e.g., trying to match opponent averages, bluff, or declare the full hold sum); doing so needlessly increases the duty paid without providing any safety benefit against the spot check.

- **Stage 2 (Route):**
  - Choose `[route: main]` whenever the value of my smallest crate is greater than or equal to the duty savings between routes: `smallest_crate >= floor(0.30 * declared) - floor(0.15 * declared)`.
  - With crate values $\ge 5$ and declared values $\le 40$, the maximum possible duty savings from `night` is at most 6 (for declared values $\ge 34$).
  - Only choose `[route: night]` if the smallest crate's value is strictly less than the duty saved: `smallest_crate < floor(0.30 * declared) - floor(0.15 * declared)`. (Specifically, only if `smallest_crate == 5` and `floor(0.30 * declared) - floor(0.15 * declared) == 6`, which occurs when `declared >= 37`).
  - In all other scenarios, choose `[route: main]`.