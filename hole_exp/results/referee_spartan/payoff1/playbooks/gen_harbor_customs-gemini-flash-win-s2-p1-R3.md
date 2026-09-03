---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 2
round: 3
chars: 1309
---
### Playbook: Harbor Customs

- **Stage 1 (Declare):**
  - Identify the exact value of the heaviest crate in the current hold ($C_{\max}$).
  - Always submit `[declare: n]` where $n = C_{\max}$.
  - Never declare below $C_{\max}$, as the inspection always checks the heaviest crate and the penalty (-40 plus full true-hold duty) is ruinous.
  - Never declare above $C_{\max}$; excess declaration directly increases duty without providing any protection or benefit.

- **Stage 2 (Route):**
  - Compare the duty savings of `night` versus the value of the smallest crate lost ($C_{\min}$):
    - Compute duty savings: $\text{Savings} = \lfloor 0.30 \times \text{declared} \rfloor - \lfloor 0.15 \times \text{declared} \rfloor$.
    - With maximum declared value $C_{\max} \le 40$, the maximum possible duty savings is 6 points ($\lfloor 0.30 \times 40 \rfloor - \lfloor 0.15 \times 40 \rfloor = 12 - 6 = 6$).
    - Since all crates are worth at least 5 points:
      - If $C_{\min} < \text{Savings}$ (the only mathematical case is $C_{\min} = 5$ AND $\text{declared} \ge 34$, which makes $\text{Savings} = 6 > 5$), submit `[route: night]`.
      - In all other cases (whenever $C_{\min} \ge \text{Savings}$, including any $C_{\min} \ge 6$ or $C_{\min} = 5$ with $\text{declared} \le 33$), submit `[route: main]`.