---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 4
round: 2
chars: 1233
---
### Playbook

- **Stage 1 (Declare):**
  - Always declare the exact value of my heaviest crate in the current hold: `[declare: max_crate]`.
  - Never declare below the heaviest crate; doing so triggers a -40 point penalty and recalculates duty at 30% of total hold value.
  - Never declare above the heaviest crate (e.g., trying to match opponent averages, bluff, or declare the full hold sum); doing so needlessly increases the duty paid without providing any safety benefit against the spot check.

- **Stage 2 (Route):**
  - Choose `[route: main]` whenever the value of my smallest crate is greater than the duty difference between routes: `smallest_crate > floor(0.30 * declared) - floor(0.15 * declared)`.
  - Since crates are worth $\ge 5$ and declared values are $\le 40$ (maximum duty savings from `night` is $\lfloor 0.30 \times 40 \rfloor - \lfloor 0.15 \times 40 \rfloor = 12 - 6 = 6$), `main` is strictly better unless `smallest_crate == 5` and `declared >= 34` (where savings $= 5$ or $6$).
  - Only choose `[route: night]` if the smallest crate's value is strictly less than the duty saved: `smallest_crate < floor(0.30 * declared) - floor(0.15 * declared)`. In all other cases (including ties), choose `[route: main]`.