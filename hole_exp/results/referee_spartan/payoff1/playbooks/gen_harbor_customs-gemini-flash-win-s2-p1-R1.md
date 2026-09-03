---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1160
---
### Playbook: Harbor Customs

- **Stage 1 (Declare):**
  - Identify the exact value of the heaviest crate in the current hold ($C_{\max}$).
  - Always submit `[declare: n]` where $n = C_{\max}$.
  - Never declare below $C_{\max}$, as the penalty (-40 plus full true-hold duty) is ruinous.
  - Never declare above $C_{\max}$ to match table averages or peer declarations; excess declaration directly increases duty without providing any protection or benefit.

- **Stage 2 (Route):**
  - Compare the duty savings of `night` versus the cost of losing the smallest crate ($C_{\min}$):
    - Compute duty savings: $\lfloor 0.30 \times C_{\max} \rfloor - \lfloor 0.15 \times C_{\max} \rfloor \approx \lfloor 0.15 \times C_{\max} \rfloor$.
    - Since $C_{\max} \le 40$, the maximum duty savings is at most $6$ points ($0.15 \times 40$).
    - Since crates are worth at least 5 points, compare $C_{\min}$ to the duty savings:
      - If $C_{\min} < \lfloor 0.30 \times C_{\max} \rfloor - \lfloor 0.15 \times C_{\max} \rfloor$, reply `[route: night]`.
      - Otherwise (whenever $C_{\min} \ge \text{duty savings}$, which is almost always true), reply `[route: main]`.