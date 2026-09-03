---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 5
round: 3
chars: 968
---
### Harbor Customs Playbook

- **Stage 1 (Declare):**
  - Identify the exact value of the heaviest crate in my current hand: `max_crate = max(c1, c2, c3)`.
  - Declare exactly `max_crate`: reply `[declare: max_crate]`.
  - Never declare above `max_crate`; paying extra duty on phantom value directly destroys score.
  - Never declare below `max_crate`; doing so triggers the -40 penalty and retroactive full duty on total hold value.

- **Stage 2 (Route Decision):**
  - Calculate duty savings on night route: `savings = floor(0.30 * declared) - floor(0.15 * declared)`.
  - Identify the value of the smallest crate: `min_crate = min(c1, c2, c3)`.
  - If `savings > min_crate`, choose night: reply `[route: night]`.
  - Otherwise (including ties), choose main: reply `[route: main]`.
  - Note: Since maximum possible savings is 6 (at declared = 40) and minimum crate value is 5, `[route: main]` will almost always be optimal unless `min_crate == 5` and `savings == 6`.